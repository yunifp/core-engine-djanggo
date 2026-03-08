from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions', null=True)
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.department.name if self.department else 'No Dept'})"