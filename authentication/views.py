from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    PasswordChangeSerializer
)


@extend_schema(
    summary="Register a new user",
    description="Create a new user account with username, email, and password",
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description="User successfully registered"
        ),
        400: OpenApiResponse(description="Validation errors")
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    Register a new user account

    Creates a new user with the provided credentials and returns
    an authentication token along with user information.
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        # Return user data and token
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'User registered successfully',
            'user': user_serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User login",
    description="Authenticate user with username/email and password to receive an auth token",
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description="Login successful"
        ),
        400: OpenApiResponse(description="Invalid credentials")
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Authenticate user and return auth token

    Accepts username or email along with password.
    Returns authentication token and user information.
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Return user data and token
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': user_serializer.data,
            'token': token.key
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User logout",
    description="Logout the authenticated user by deleting their auth token",
    responses={
        200: OpenApiResponse(description="Logout successful"),
        401: OpenApiResponse(description="Authentication required")
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by deleting their authentication token

    This effectively invalidates the token, requiring the user
    to login again to access protected endpoints.
    """
    try:
        # Delete the user's token
        token = Token.objects.get(user=request.user)
        token.delete()

        # Also logout from Django session (if using sessions)
        logout(request)

        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return Response({
            'message': 'No active session found'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Get user profile",
    description="Get the authenticated user's profile information",
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="Authentication required")
    },
    tags=['Authentication']
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    """
    Get authenticated user's profile information
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Update user profile",
    description="Update the authenticated user's profile information",
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description="Validation errors"),
        401: OpenApiResponse(description="Authentication required")
    },
    tags=['Authentication']
)
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def profile_update_view(request):
    """
    Update authenticated user's profile information
    """
    partial = request.method == 'PATCH'
    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=partial
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Change password",
    description="Change the authenticated user's password",
    request=PasswordChangeSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully"),
        400: OpenApiResponse(description="Validation errors"),
        401: OpenApiResponse(description="Authentication required")
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Change authenticated user's password

    Requires old password verification and creates a new token.
    """
    serializer = PasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        # Update password
        serializer.save()

        # Generate new token for security
        try:
            old_token = Token.objects.get(user=request.user)
            old_token.delete()
        except Token.DoesNotExist:
            pass

        new_token = Token.objects.create(user=request.user)

        return Response({
            'message': 'Password changed successfully',
            'token': new_token.key
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Verify token",
    description="Verify if the current authentication token is valid",
    responses={
        200: OpenApiResponse(description="Token is valid"),
        401: OpenApiResponse(description="Token is invalid")
    },
    tags=['Authentication']
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verify_token_view(request):
    """
    Verify if the current authentication token is valid
    """
    user_serializer = UserSerializer(request.user)
    return Response({
        'message': 'Token is valid',
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)