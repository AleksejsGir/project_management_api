from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with password confirmation
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate_username(self, value):
        """Validate username uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        """Validate email uniqueness and format"""
        if not value:
            raise serializers.ValidationError("Email field is required.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        """Validate password using Django's built-in validators"""
        validate_password(value)
        return value

    def validate(self, data):
        """Cross-field validation for password confirmation"""
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': "Password confirmation doesn't match password."
            })

        return data

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm', None)

        # Create user with encrypted password
        user = User.objects.create_user(**validated_data)

        # Create authentication token for the user
        Token.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login with username/email and password
    """
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        """Authenticate user with username/email and password"""
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Try to authenticate with username first
            user = authenticate(username=username, password=password)

            # If username auth failed, try with email
            if not user:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid username/email or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")

        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    projects_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'projects_count'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'projects_count']

    def get_projects_count(self, obj):
        """Get the number of projects owned by this user"""
        return obj.projects.count()

    def validate_email(self, value):
        """Validate email uniqueness for updates"""
        if not value:
            raise serializers.ValidationError("Email field is required.")

        # Check if email is taken by another user
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password
    """
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate_old_password(self, value):
        """Validate that old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Validate new password using Django's built-in validators"""
        validate_password(value)
        return value

    def validate(self, data):
        """Cross-field validation for new password confirmation"""
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': "New password confirmation doesn't match new password."
            })

        return data

    def save(self):
        """Update user password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user