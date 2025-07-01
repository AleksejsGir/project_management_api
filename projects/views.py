from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Project, Vacancy
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    VacancySerializer,
    VacancyCreateSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the project.
        return obj.owner == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing projects.

    Provides CRUD operations for projects:
    - list: Get all projects for the authenticated user
    - create: Create a new project
    - retrieve: Get a specific project by ID
    - update: Update a project (full update)
    - partial_update: Partially update a project
    - destroy: Delete a project
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Return projects owned by the current user only
        """
        return Project.objects.filter(owner=self.request.user).select_related('owner').prefetch_related('vacancies')

    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    @extend_schema(
        summary="List all projects",
        description="Get a list of all projects owned by the authenticated user",
        responses={200: ProjectListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List all projects for the authenticated user"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new project",
        description="Create a new project. The authenticated user will be set as the owner.",
        responses={201: ProjectSerializer}
    )
    def create(self, request, *args, **kwargs):
        """Create a new project"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Get project details",
        description="Retrieve detailed information about a specific project",
        responses={200: ProjectSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Get a specific project"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update project",
        description="Update all fields of a project",
        responses={200: ProjectSerializer}
    )
    def update(self, request, *args, **kwargs):
        """Update a project (full update)"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update project",
        description="Update specific fields of a project",
        responses={200: ProjectSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a project"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete project",
        description="Delete a project and all associated vacancies",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a project"""
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Get project vacancies",
        description="Get all vacancies for this project",
        responses={200: VacancySerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def vacancies(self, request, pk=None):
        """
        Get all vacancies for this project
        """
        project = self.get_object()
        vacancies = project.vacancies.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create project vacancy",
        description="Create a new vacancy for this project",
        request=VacancyCreateSerializer,
        responses={201: VacancySerializer}
    )
    @vacancies.mapping.post
    def create_vacancy(self, request, pk=None):
        """
        Create a new vacancy for this project
        """
        project = self.get_object()
        serializer = VacancyCreateSerializer(data=request.data)

        if serializer.is_valid():
            vacancy = serializer.save(project=project)
            response_serializer = VacancySerializer(vacancy)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get project statistics",
        description="Get project statistics including technology counts and vacancy statistics",
        responses={200: {
            'type': 'object',
            'properties': {
                'total_technologies': {'type': 'integer'},
                'total_vacancies': {'type': 'integer'},
                'active_vacancies': {'type': 'integer'},
                'is_overdue': {'type': 'boolean'},
                'days_until_deadline': {'type': 'integer', 'nullable': True}
            }
        }}
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get statistics for this project
        """
        project = self.get_object()
        vacancies = project.vacancies.all()

        stats_data = {
            'total_technologies': project.technologies_count,
            'total_vacancies': vacancies.count(),
            'active_vacancies': vacancies.filter(is_active=True).count(),
            'is_overdue': project.is_overdue,
            'days_until_deadline': None
        }

        # Calculate days until deadline
        if project.deadline:
            from django.utils import timezone
            delta = project.deadline - timezone.now().date()
            stats_data['days_until_deadline'] = delta.days

        return Response(stats_data)


class VacancyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing individual vacancies.

    Provides CRUD operations for vacancies:
    - list: Get all vacancies for projects owned by the user
    - retrieve: Get a specific vacancy by ID
    - update: Update a vacancy (full update)
    - partial_update: Partially update a vacancy
    - destroy: Delete a vacancy
    """
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return vacancies for projects owned by the current user only
        """
        return Vacancy.objects.filter(
            project__owner=self.request.user
        ).select_related('project')

    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only project owners can modify vacancies
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def check_object_permissions(self, request, obj):
        """
        Check object-level permissions for vacancy operations
        """
        # For vacancies, check if user owns the project
        if hasattr(obj, 'project'):
            if obj.project.owner != request.user:
                self.permission_denied(request, message="You can only access vacancies from your own projects.")
        return super().check_object_permissions(request, obj)

    @extend_schema(
        summary="List all vacancies",
        description="Get a list of all vacancies for projects owned by the authenticated user",
        parameters=[
            OpenApiParameter(
                name='project',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter vacancies by project ID'
            ),
            OpenApiParameter(
                name='employment_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by employment type (full-time, part-time, contract, freelance, internship)'
            ),
            OpenApiParameter(
                name='is_active',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter by active status'
            )
        ],
        responses={200: VacancySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List vacancies with optional filtering"""
        queryset = self.get_queryset()

        # Apply filters
        project_id = request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        employment_type = request.query_params.get('employment_type')
        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(is_active=is_active_bool)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get vacancy details",
        description="Retrieve detailed information about a specific vacancy",
        responses={200: VacancySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Get a specific vacancy"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update vacancy",
        description="Update all fields of a vacancy",
        responses={200: VacancySerializer}
    )
    def update(self, request, *args, **kwargs):
        """Update a vacancy (full update)"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update vacancy",
        description="Update specific fields of a vacancy",
        responses={200: VacancySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a vacancy"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete vacancy",
        description="Delete a vacancy",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a vacancy"""
        return super().destroy(request, *args, **kwargs)