from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Vacancy


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model with full CRUD support
    """
    owner = serializers.StringRelatedField(read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    technologies_count = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()

    # Nested field to show vacancy count
    vacancies_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'technologies',
            'budget',
            'deadline',
            'owner',
            'owner_id',
            'technologies_count',
            'is_overdue',
            'vacancies_count',
            'metadata',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'owner_id', 'created_at', 'updated_at']

    def get_vacancies_count(self, obj):
        """Get the number of vacancies for this project"""
        return obj.vacancies.count()

    def validate_technologies(self, value):
        """Validate technologies field"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Technologies must be a list.")

        # Ensure all items are strings
        for tech in value:
            if not isinstance(tech, str):
                raise serializers.ValidationError("All technologies must be strings.")
            if len(tech.strip()) == 0:
                raise serializers.ValidationError("Technology names cannot be empty.")

        return [tech.strip() for tech in value if tech.strip()]

    def validate_budget(self, value):
        """Validate budget field"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Budget must be greater than 0.")
        return value

    def validate_deadline(self, value):
        """Validate deadline field"""
        if value is not None:
            from django.utils import timezone
            if value < timezone.now().date():
                raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def create(self, validated_data):
        """Create a new project with the current user as owner"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for project lists (better performance)
    """
    owner = serializers.StringRelatedField(read_only=True)
    technologies_count = serializers.ReadOnlyField()
    vacancies_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'technologies_count',
            'budget',
            'deadline',
            'owner',
            'vacancies_count',
            'created_at',
            'updated_at'
        ]

    def get_vacancies_count(self, obj):
        return obj.vacancies.count()


class VacancySerializer(serializers.ModelSerializer):
    """
    Serializer for Vacancy model
    """
    project_title = serializers.CharField(source='project.title', read_only=True)
    salary_range = serializers.ReadOnlyField()

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'requirements',
            'salary_min',
            'salary_max',
            'salary_range',
            'employment_type',
            'project',
            'project_title',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'project_title', 'created_at', 'updated_at']

    def validate_salary_min(self, value):
        """Validate minimum salary"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Minimum salary must be greater than 0.")
        return value

    def validate_salary_max(self, value):
        """Validate maximum salary"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Maximum salary must be greater than 0.")
        return value

    def validate(self, data):
        """Cross-field validation"""
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if salary_min and salary_max:
            if salary_min > salary_max:
                raise serializers.ValidationError(
                    "Minimum salary cannot be greater than maximum salary."
                )

        return data


class VacancyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating vacancies within a project context
    """

    class Meta:
        model = Vacancy
        fields = [
            'title',
            'description',
            'requirements',
            'salary_min',
            'salary_max',
            'employment_type',
            'is_active'
        ]

    def validate_salary_min(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Minimum salary must be greater than 0.")
        return value

    def validate_salary_max(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Maximum salary must be greater than 0.")
        return value

    def validate(self, data):
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if salary_min and salary_max:
            if salary_min > salary_max:
                raise serializers.ValidationError(
                    "Minimum salary cannot be greater than maximum salary."
                )

        return data