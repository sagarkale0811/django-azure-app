from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('services')  # after login go to service list
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def service_list(request):
    services = [
        {"name": "Azure App Service", "desc": "Host web apps and APIs"},
        {"name": "Azure Functions", "desc": "Serverless compute"},
        {"name": "Azure Kubernetes Service", "desc": "Managed Kubernetes"},
        {"name": "Azure Blob Storage", "desc": "Object storage for data"},
        {"name": "Azure SQL Database", "desc": "Managed SQL database"},
        {"name": "Azure AI Services", "desc": "Vision, speech, language AI"},
    ]
    return render(request, 'service_list.html', {"services": services})




# API Views (add at the bottom of your views.py)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, ServiceSerializer, UserSerializer
from .models import Service

# Register API
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def api_register(request):
    if request.method == 'GET':
        # This will show the form in browsable API
        serializer = RegisterSerializer()
        return Response(serializer.data)
    
    # Handle POST for registration
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User registered successfully",
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

