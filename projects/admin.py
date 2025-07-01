from django.contrib import admin
from .models import Project, Vacancy


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'budget', 'deadline', 'technologies_count', 'created_at')
    list_filter = ('created_at', 'deadline', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at', 'technologies_count', 'is_overdue')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'budget', 'deadline')
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'technologies_count', 'is_overdue'),
            'classes': ('collapse',)
        }),
    )

    def technologies_count(self, obj):
        return obj.technologies_count

    technologies_count.short_description = 'Tech Count'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'employment_type', 'salary_range', 'is_active', 'created_at')
    list_filter = ('employment_type', 'is_active', 'created_at', 'project__owner')
    search_fields = ('title', 'description', 'project__title')
    readonly_fields = ('created_at', 'updated_at', 'salary_range')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'project', 'employment_type', 'is_active')
        }),
        ('Description', {
            'fields': ('description', 'requirements')
        }),
        ('Salary', {
            'fields': ('salary_min', 'salary_max', 'salary_range')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )