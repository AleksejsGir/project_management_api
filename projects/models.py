from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Project(models.Model):
    """
    Project model for managing development projects
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Project Title",
        help_text="Maximum 200 characters"
    )
    description = models.TextField(
        verbose_name="Project Description",
        help_text="Detailed project description"
    )
    technologies = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Technologies",
        help_text="List of technologies used (e.g., ['Python', 'Django', 'React'])"
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Budget",
        help_text="Project budget in currency"
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name="Deadline",
        help_text="Expected project completion date"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="Project Owner"
    )

    # Flexible field for future extensions (e.g., Figma data)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Additional Data",
        help_text="JSON field for storing additional information"
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']  # Latest projects first

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

    @property
    def technologies_count(self):
        """Number of technologies used in the project"""
        return len(self.technologies) if self.technologies else 0

    @property
    def is_overdue(self):
        """Check if project is overdue"""
        if self.deadline:
            from django.utils import timezone
            return timezone.now().date() > self.deadline
        return False


class Vacancy(models.Model):
    """
    Vacancy model for project job openings
    """

    EMPLOYMENT_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Vacancy Title"
    )
    description = models.TextField(
        verbose_name="Job Description"
    )
    requirements = models.TextField(
        verbose_name="Requirements"
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Minimum Salary"
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Maximum Salary"
    )
    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_CHOICES,
        default='full-time',
        verbose_name="Employment Type"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name="Project"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Whether the vacancy is visible in search"
    )

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.project.title}"

    @property
    def salary_range(self):
        """Salary range in readable format"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_min} - {self.salary_max}"
        elif self.salary_min:
            return f"from {self.salary_min}"
        elif self.salary_max:
            return f"up to {self.salary_max}"
        return "Negotiable"