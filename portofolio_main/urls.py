from django.urls import path
from portofolio_main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_project, 
    delete_project, 
    get_projects_json,
    suntik_data
)

app_name = 'portofolio_main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    path('projects/', show_projects, name='show_projects'),              # <--- Tambahkan ini
    path('projects/add/', create_project, name='create_project'),        # <--- Tambahkan ini
    path('projects/<uuid:project_id>/delete/', delete_project, name='delete_project'), # <--- Tambahkan ini
    path('api/projects/', get_projects_json, name='get_projects_json'),  # <--- Tambahkan ini
    path('suntik-data-zaky/', suntik_data, name='suntik_data'), 
]