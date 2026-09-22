import uuid
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)
    starred_by = models.ManyToManyField(
      User, related_name='starred_projects', blank=True)

    def __str__(self):
        return self.title

class Experience(models.Model):
    # Django otomatis membuat field 'id' bertipe AutoField (Integer) 
    title = models.CharField(max_length=255)            # Tipe 1: String (CharField)
    company = models.CharField(max_length=255)          # Tipe 1: String (CharField)
    start_date = models.DateField()                     # Tipe 2: Date (DateField)
    is_active = models.BooleanField(default=True)       # Tipe 3: Boolean (BooleanField)
    description = models.TextField()                    # Tipe 4: Text (TextField)

    def __str__(self):
        return f"{self.title} at {self.company}"