# messaging_app/chats/auth.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend default TokenObtainPairSerializer so that the response
    includes the user’s UUID (user_id) and username along with tokens.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can put extra claims into the token here if needed:
        # token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include any extra user info in the response:
        data['user_id'] = str(self.user.user_id)
        data['username'] = self.user.username
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Use MyTokenObtainPairSerializer in place of the default.
    """
    serializer_class = MyTokenObtainPairSerializer


# We do not need to subclass TokenRefreshView unless customizing;
# the default behavior is sufficient:
class MyTokenRefreshView(TokenRefreshView):
    pass
