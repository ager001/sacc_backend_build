from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .permissions import IsSuperUser
from rest_framework import permissions,status
from .serializers import (
    SchoolRegistrationSerializer,
    SchoolListSerializer,
)
from .models import School

# creation of school registration API
class SchoolRegistrationAPIView(APIView):
    
    # who is allowed to make the request(any=everyone)
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=SchoolRegistrationSerializer,
        responses={
            201: SchoolListSerializer,
        },
        summary="Register a new school",
        description="Creates a new school account."
    )
    # http method post means create
    def post(self, request):
        # validation of the request using serializer
        serializer = SchoolRegistrationSerializer(
                data=request.data
            )
        # after finding the validation is valid
        serializer.is_valid(raise_exception=True)
        # save 
        serializer.save()
        
        # finally send back the data of the newly created school and the status code
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
        

class ListRegisteredSchoolsAPIView(APIView):
    # who is allowed to make the request
    # only SuperUser is allowed to make request
    # we have created custom permissions and imported it
    permission_classes = [IsSuperUser]
    
    @extend_schema(
        responses={
            200: SchoolListSerializer(many=True),
        },
        summary="List all schools",
        description="Returns all registered schools. Accessible only by superusers."
    )
    # Http method
    def get (self, request):
        # here the model talks to the database.
        schools = School.objects.all()
        #Validation of the request using serializer
        serializer = SchoolListSerializer(
            schools, many=True
        )
        
        # finally send back the data of the newly created school and the status code
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    