from rest_framework import serializers
from .models import User, Profile



class ProfileSerializerForLoginUser(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField("get_profile_image_url")
    gender        = serializers.SerializerMethodField("get_gender")

    class Meta:
        model  = Profile
        fields = ["employee_no", "phone", "nid_no", "facebook_link", "profile_image", "profile_image_url",
                  "gender", "salary", "address"]

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            profile_image = obj.profile_image.url
            return request.build_absolute_uri(profile_image)
        return None

    def get_gender(self, obj):
        return obj.get_gender_display()




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_type', 'first_name', 'last_name', 'username', 'email', 'last_login', 'is_active']


    # def get_user_type(self, obj):
    #     return obj.get_user_type_display()




class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        first_name = attrs.get("first_name", None)
        last_name  = attrs.get("last_name", None)
        username   = attrs.get("username", None)
        email      = attrs.get("email", None)
        password   = attrs.get("password", None)
        password2  = attrs.get("password2", None)

        if not first_name:
            raise serializers.ValidationError('First name should not be empty !')
        if not last_name:
            raise serializers.ValidationError('Last name should not be empty !')
        if not username:
            raise serializers.ValidationError('Username should not be empty !')

        if not email:
            raise serializers.ValidationError('Email should not be empty !')
        if password != password2:
            raise serializers.ValidationError('Password mismatch !')
        return attrs
    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name  = validated_data.get('last_name')
        username   = validated_data.get('username')
        email      = validated_data.get('email')
        password   = validated_data.get('password')
        user       = User.objects._create_user(
            user_type='Employee',
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        return user



class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()




class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class RegisterSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()
    name     = serializers.CharField()



class ProfileSerializer(serializers.ModelSerializer):
    user          = UserSerializer()
    profile_image = serializers.SerializerMethodField("get_profile_image_url")

    class Meta:
        model = Profile
        fields = ["id", "user", "employee_no", "phone", "nid_no", "facebook_link", "profile_image", "profile_image_url",
                  "gender", "salary", "address"]

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            profile_image = obj.profile_image.url
            return request.build_absolute_uri(profile_image)
        return None

    # def get_gender(self, obj):
    #     return obj.get_gender_display()

class ProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField("get_profile_image_url")
    class Meta:
        model  = Profile
        fields = ["profile_image", "profile_image_url"]

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            profile_image = obj.profile_image.url
            return request.build_absolute_uri(profile_image)
        return None

class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone", "nid_no", "facebook_link", "profile_image", "profile_image_url", "gender", "salary", "address"]