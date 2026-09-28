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
from django.core.management import call_command

from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm

# ==========================================
# HELPER OTORISASI
# ==========================================
def is_editor(user):
    return user.is_authenticated and user.groups.filter(name='Editor').exists()

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
    
    # --- AUTO MIGRATE & AUTO SUPERUSER UNTUK PWS ---
    try:
        call_command('migrate', interactive=False)
        if not User.objects.filter(username="adminpws").exists():
            User.objects.create_superuser("adminpws", "admin@pws.com", "zaky12345")
    except Exception as e:
        print("Migrate error:", e)
    # -----------------------------------------------

    return render(request, "main.html", context)

# ==========================================
# VIEWS UNTUK EXPERIENCE
# ==========================================
def show_experience(request):
    experiences = Experience.objects.all()
    context = {
        'name': 'Mohammad Zaky Prastio',
        'experience_list': experiences,
    }
    return render(request, 'experience.html', context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_experience(request, id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def delete_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Mohammad Zaky Prastio",
        "form": form,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
        
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

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
        "is_editor": is_editor(request.user),
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
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
    # MUST BE AT THE VERY TOP (sebelum AuthenticationForm dibikin!)
    try:
        call_command('migrate', interactive=False)
        if not User.objects.filter(username="adminpws").exists():
            User.objects.create_superuser("adminpws", "admin@pws.com", "zaky12345")
    except Exception as e:
        print("Auto-migrate error on login:", e)

    # Baru setelah database di-migrate, aman bikin form ini
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
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
    response.delete_cookie('last_login')
    return response