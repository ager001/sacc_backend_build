from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .services import authentication_service
from drf_spectacular.utils import extend_schema
from .serializers import LoginSerializer, LogoutSerializer, CurrentSchoolSerializer, VerifySchoolSerializer

# LoginAPIView endpoint gets created
class LoginAPIView(APIView):
    # In permissions everyone who can access the endpoint can login
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        # code below simply means the client must send data that matches this serializer
        # later we will create it in our serializers for the responses
            request=LoginSerializer,
            # description of what our API should return
            responses={
                200: {
                    "type": "object",
                    "properties": {
                        "refresh": {"type": "string"},
                        "access": {"type": "string"},
                        "school": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "email": {"type": "string"},
                            },
                        },
                    },
                },
            },
            # This text appears in Swagger below the endpoint.
            description="Authenticate a school administrator and return JWT access and refresh tokens."
        )
   
    
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
            # below we now return the response of two tokens; later on we will create it in the serializers field
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

# creation of the LogoutAPI
class LogoutAPIView(APIView):
    # only authenticated people
    permission_classes = [permissions.IsAuthenticated]
    # also here we extend the schema 
    @extend_schema(
                request=LogoutSerializer,
                responses={
                    200: {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string"
                            }
                        }
                    }
                },
                description="Blacklist the refresh token and log out the authenticated user."
            )
    # logout is a post method 
    # we're changing the server's state by blacklisting a token.
    def post(self, request):
        #The serializer performs validation
        serializer = LogoutSerializer(
         data=request.data
       ) 
        # if serializer is valid proceed 
        serializer.is_valid(
            raise_exception=True
        )
        # retrieval of the token
        refresh = serializer.validated_data["refresh"]    
        # Simple JWT opens the envelope and creates a Python object representing that token
        token = RefreshToken(refresh)    
        # Now we add the token to the blacklist app 
        token.blacklist()
        
        # we now send a response 
        return Response(
            {
                "message":"Logged out successfully."
            },
            status=status.HTTP_200_OK
        )
        
# this is the current user view that returns the details of the currently authenticated user        
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
# this is the get method that returns the details of the currently authenticated user
    def get(self, request):
        serializer = CurrentSchoolSerializer(request.user)

        return Response(serializer.data)
    
    
# verify school view that verifies the school credentials
class VerifySchoolView(APIView):
    # below means that anyone can access this endpoint without authentication
    permission_classes = [permissions.AllowAny]
    # below is the post method that verifies the school credentials
    @extend_schema(
    request=VerifySchoolSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string"
                },
                "school": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        },
                        "email": {
                            "type": "string"
                        },
                    },
                },
            },
        },
    },
    summary="Verify School",
    description="""
    Verify that the school exists and the supplied
    password is correct before proceeding to role
    authentication.
    """,
    tags=["Authentication"],
)
    def post(self, request):
        # here we verify the school credentials by using the VerifySchoolSerializer to validate the data sent from the frontend
        serializer = VerifySchoolSerializer(
            data=request.data
        )
        # we now verify if the serializer is valid, if not it will raise an exception
        serializer.is_valid(
            raise_exception=True
        )
        # we cross check the validated data with the AuthenticationService to verify the school credentials is in the database and if it is active, if not it will raise an exception
        school = authentication_service.verify_school(
            serializer.validated_data
        )
        # if the school is verified successfully, we return a response with a message and the school details
        return Response(
            {
                "message": "School verified successfully.",
                "school": {
                    "id": school.id,
                    "name": school.name,
                    "email": school.email,
                },
            },
            status=status.HTTP_200_OK,
        )