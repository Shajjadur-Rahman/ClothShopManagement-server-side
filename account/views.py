import jwt
import random
import string
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from .models import User, Profile, Jwt
from .authentication import Authentication
from .serializers import (
    UserSerializer,
    LoginSerializer,
    ProfileSerializer,
    RefreshSerializer,
    CreateUserSerializer,
    ProfileImageSerializer,
    CreateProfileSerializer
)
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView
)
from django.utils.timezone import is_naive, make_aware, utc


# def make_utc(dt):
#     if settings.USE_TZ and is_naive(dt):
#         return make_aware(dt, timezone=utc)
#     return dt
#
# def aware_utcnow():
#     return make_utc(datetime.utcnow())


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=50), "user_id": payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.utcnow() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm='HS256'
    )


class LoginApiVew(APIView):
    def post(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if not user:
                return Response({'error': 'Invalid email or password !'}, status=status.HTTP_400_BAD_REQUEST)
            access = get_access_token(user.id)
            refresh = get_refresh_token()
            Jwt.objects.filter(user_id=user.id).delete()
            Jwt.objects.create(
                user_id=user.id,
                access=access,
                refresh=refresh
            )
            profile        = user.profile
            pro_serializer = ProfileImageSerializer(profile, context={'request': self.request}, many=False)
            serializer2    = UserSerializer(user, many=False)
            return Response({'user': serializer2.data, 'pro_image': pro_serializer.data, 'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)


class RefreshApiView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_iwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status=status.HTTP_404_NOT_FOUND)
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "token is invalid or as expired !"})
        access = get_access_token(active_iwt.user.id)
        active_iwt.access = access.encode()
        active_iwt.save()
        return Response({'access': access}, status=status.HTTP_200_OK)


class CreateEmployeeApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            profile = Profile.objects.all().first()
            employee_no = int(''.join(filter(lambda i: i.isdigit(), profile.employee_no)))
            employee_no = str(employee_no + 1)
        except Exception as e:
            employee_no = str(1)

        employee_no = "E-" + employee_no
        serializer = CreateUserSerializer(data=self.request.data)
        serializer2 = CreateProfileSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True) and serializer2.is_valid(raise_exception=True)
        user = serializer.save()
        serializer2.save(user_id=user.id, employee_no=employee_no)
        profile = Profile.objects.get(user_id=user.id)
        pro_serializer = ProfileSerializer(profile, context={'request': request}, many=False)
        return Response({"data": pro_serializer.data, "total_salary": serializer2.validated_data["salary"]}, status=status.HTTP_201_CREATED)



class EmployeeListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles       = Profile.objects.all()
        total_employee = profiles.count()
        total_salary   = sum(user.salary for user in profiles)
        serializer     = ProfileSerializer(profiles, context={'request': request}, many=True)
        return Response({"data": serializer.data, "total_salary": total_salary, 'total_employee': total_employee},
                        status=status.HTTP_200_OK)



class DeleteEmployeeApiView(DestroyAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = User.objects.all()
    serializer_class       = UserSerializer
    lookup_field           = "id"


class HoldEmployeeApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = UserSerializer

    def post(self, *args, **kwargs):
        user       = User.objects.get(id=kwargs["id"])
        serializer = self.serializer_class(instance=user, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Employee active status updated !"}, status=status.HTTP_200_OK)



class EmployeeDetailApiView(RetrieveAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Profile.objects.all()
    serializer_class       = ProfileSerializer
    lookup_field           = "id"



class ProfileApiView(RetrieveAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"



