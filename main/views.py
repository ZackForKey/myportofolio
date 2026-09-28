import datetime
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm

# ==========================================
# VIEWS UNTUK HALAMAN UTAMA
# ==========================================
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',
        "last_login": last_login,
    }
    
    # --- KODE SEMENTARA UNTUK JADIKAN SUPERUSER & RESET PASSWORD ---
    try:
        user_to_fix = User.objects.get(username="Zakyprastio")
        user_to_fix.set_password("zaky12345") # Password baru kamu
        user_to_fix.is_superuser = True
        user_to_fix.is_staff = True
        user_to_fix.save()
    except User.DoesNotExist:
        pass
    if not User.objects.filter(username="adminpws").exists():
        User.objects.create_superuser("adminpws", "admin@pws.com", "zaky12345")
    # -------------------------------------------------------------

    return render(request, "main.html", context)

# ==========================================
# VIEWS UNTUK EXPERIENCE (TUGAS 3)
# ==========================================
def show_experience(request):
    experiences = Experience.objects.all()
    context = {
        'name': 'Mohammad Zaky Prastio',
        'experience_list': experiences,
    }
    return render(request, 'experience.html', context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")
    context = {
        "name": "Mohammad Zaky Prastio",
        "form": form,
    }
    return render(request, "create_experience.html", context)

def update_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Data pengalaman berhasil diupdate!")
        return redirect('main:show_experience')
    context = {
        'name': 'Mohammad Zaky Prastio',
        'form': form,
    }
    return render(request, 'update_experience.html', context)

def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect('main:show_experience')

def show_json_experience(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# ==========================================
# VIEWS UNTUK PROJECT
# ==========================================
@login_required(login_url="/login/")
def create_project(request):
    # Hanya superuser yang bisa menambah proyek
    if not request.user.is_superuser:
        raise PermissionDenied
        
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Mohammad Zaky Prastio",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # use_natural_foreign_keys ditambahkan agar tidak membocorkan ID internal saat mengekspos fitur Star
    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Mohammad Zaky Prastio",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    # Hanya superuser yang bisa menghapus proyek
    if not request.user.is_superuser:
        raise PermissionDenied
        
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")
    
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else: # Kalau belum, tambahkan star
            project.starred_by.add(request.user)
    return redirect("main:show_projects")

# ==========================================
# AUTHENTICATION
# ==========================================
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Mohammad Zaky Prastio",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        # Set cookie last_login
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    context = {
        "name": "Mohammad Zaky Prastio",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    # Hapus cookie saat logout
    response.delete_cookie('last_login')
    return response