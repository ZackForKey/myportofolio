from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    # Project Endpoints
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    
    # Experience Endpoints
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<int:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<int:experience_id>/star/", api_views.experience_star, name="experience-star"),
    
    # Contact Endpoints
    path("contacts/", api_views.contact_list, name="contact-list"),
    path("contacts/<int:contact_id>/", api_views.contact_detail, name="contact-detail"),
]