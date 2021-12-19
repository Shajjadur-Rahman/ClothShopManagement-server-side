from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from datetime import datetime

from account.authentication import Authentication
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskSerializer,
)

from .models import Task



class TaskCreateApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class = TaskCreateSerializer

    def post(self, request, *args, **kwargs):
        user       = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=user, task_creator=user.username)
        serializer2 = TaskSerializer(task, many=False)
        return Response(serializer2.data, status=status.HTTP_201_CREATED)



class TaskListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.filter(user=self.request.user)
        query    = self.request.GET.get("timestamp")
        if query:
            year     = int(query[0:4])
            month    = int(query[5:7])
            day      = int(query[8:12])
            queryset = queryset.filter(timestamp__year=year, timestamp__month=month, timestamp__day=day+1)
        return queryset

class AllEmployeeTaskListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.all().exclude(user=self.request.user)
        query    = self.request.GET.get("timestamp")
        if query:
            year     = int(query[0:4])
            month    = int(query[5:7])
            day      = int(query[8:12])
            queryset = queryset.filter(timestamp__year=year, timestamp__month=month, timestamp__day=day+1)
        return queryset


class TaskCompleteApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=kwargs["id"])
        except Exception:
            return Response({"error": "Query does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "Task updated !"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs["id"])
        serializer = TaskCreateSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        serializer2 = TaskSerializer(task, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)




class DeteTaskApiView(DestroyAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = TaskSerializer
    queryset               = Task.objects.all()
    lookup_field           = "id"
