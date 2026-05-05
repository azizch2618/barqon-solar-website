from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.permissions import IsOwnerOrAdmin

from .serializers import RegisterSerializer, StaffSerializer
from .models import User

@api_view(["GET", "POST"])
@permission_classes([IsOwnerOrAdmin])
def staff_list_create(request):
    if request.method == "POST":
        serializer = StaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    staff = User.objects.filter(is_staff=True)
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def register(request):
    if request.method == "GET":
        return Response({
            "message": "Use POST to register a new user, or visit the web registration page.",
            "web_registration_url": "/register/"
        })
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsOwnerOrAdmin])
def owner_profile(request):
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": getattr(user, "is_admin", False),
            "is_staff": user.is_staff,
        }
    )
