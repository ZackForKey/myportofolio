from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_project, 
    get_projects_json, 
    delete_project,
    # Tambahan views baru untuk CRUD Experience
    create_experience,
    update_experience,
    delete_experience,
    show_json_experience,
    create_project,
    delete_project,
    login_user,
    logout_user,
    register,
    toggle_star,
)
from main.views import register, login_user, logout_user

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    # --- PATH UNTUK PROJECT ---
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),

    # --- PATH BARU UNTUK EXPERIENCE (TUGAS 3) ---
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<int:id>/update/", update_experience, name="update_experience"),
    path("experience/<int:id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", show_json_experience, name="show_json_experience"),

    # --- TUTOR 4 ---!
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('projects/<uuid:project_id>/star/', toggle_star, name='toggle_star'),
    path('', show_main, name='show_main'),
]