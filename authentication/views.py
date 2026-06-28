from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

# LoginAPIView endpoint gets created
class LoginAPIView(APIView):
    # In permissions everyone who can access the endpoint can login
    permission_classes = [permissions.AllowAny]
    # used post for in login the user send sensitive information
    def post(self, request):
        # creation of the serializer
        # request.data comes from the client.
        # request comes from us.
        serializer = LoginSerializer(
            data=request.data,
            context={
                "request": request
            }
        
        )
        # after finding the validation is valid, authenticate()
        serializer.is_valid(raise_exception=True)
        #  it is same as opening the backpack "attrs" and taking out the authenticated school.
        school = serializer.validated_data["school"]
        # Authentication is already finished.
        # We are simply creating identity cards.
        refresh = RefreshToken.for_user(school)
        # below we now return the response of two tokens
        # The refresh token owns the access token.
        # str(refresh) converts the token into the compact JWT string that can be sent over HTTP.
        # remember refresh tokens are always python objects 
        return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                      "school": {
                            "id": school.id,
                            "name": school.name,
                            "email": school.email,
                        },
                },
                status=status.HTTP_200_OK,
        )
        