import jwt
from django.conf import settings
from datetime import datetime
from .models import User
from rest_framework.authentication import BaseAuthentication


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:

            return None, None
        return self.get_user(data["user_id"]), None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except Exception:
            return None

    def validate_request(self, headers):
        authorisation = headers.get("Authorization", None)
        if not authorisation:
            return None
        token = headers["Authorization"][7:]
        decoded_data = Authentication.verify_token(token)
        if not decoded_data:
            return None
        return decoded_data

    @staticmethod
    def verify_token(token):
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return None
        exp = decoded_data["exp"]
        # print("expired", datetime.now(), datetime.fromtimestamp(exp)) datetime.utcnow()
        # print("Now", datetime.utcnow(), "expired", datetime.fromtimestamp(exp))
        # if datetime.now().timestamp() > exp:
        if datetime.utcnow().timestamp() > exp:
            return None
        return decoded_data
