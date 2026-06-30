# views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "SACC Backend API is running"
    })