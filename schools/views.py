from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsSuperUser
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
    # http method post means create
    def post(self, request):
        # validation of the request using serializer
        serializer = SchoolRegistrationSerializer(
                data=request.data
            )
        # after finding the validation is valid
        serializer.is_valid()
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
    # Http method
    def get (self, request):
        # here the model talks to the database.
        schools = School.objects.all()
        #Validation of the request using serializer
        serializer = SchoolListSerializer(
            schools, many=True
        )
        # after finding the validation is valid
        serializer.is_valid()
        # save 
        serializer.save()
        
        # finally send back the data of the newly created school and the status code
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    