from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Project

# Create your views here.
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',
        "last_login": last_login,
            
    }
    return render(request, "main.html", context)

# ==========================================
# VIEWS UNTUK EXPERIENCE (TUGAS 3)
# ==========================================
def show_experience(request):
    # Sekarang datanya kita ambil dari database, bukan hardcode lagi
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
# VIEWS UNTUK PROJECT (KODE LAMA)
# ==========================================
def create_project(request):
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

    projects_json = serializers.serialize("json", projects)
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

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")

# REGISTER
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Nama Kamu",
        "form": form,
    }
    return render(request, "register.html", context)

# LOGIN (Mengeset cookie last_login)
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    context = {
        "name": "Nama Kamu",
        "form": form,
    }
    return render(request, "login.html", context)

# LOGOUT (Mengehapus cookie last_login)
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# UPDATE SHOW_MAIN (Membaca cookie last_login)
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Mohammad Zaky Prastio",
        "npm": "2506657011",
        "study_program": "S1 Ilmu Komputer",
        "bio": "ah males",
        "last_login": last_login,
    }
    return render(request, "main.html", context)

def register(request):
  form = UserCreationForm(request.POST or None)
  if request.method == 'POST' and form.is_valid():
    form.save()
    messages.success(request, 'Akun berhasil dibuat. Silakan login.')
    return redirect('main:login')
  context = {
      'name': 'Mohammad Zaky Prastio',
      'form': form,
  }
  return render(request, 'register.html', context)


# 3. Login (Set Cookie last_login)
def login_user(request):
  form = AuthenticationForm(request, data=request.POST or None)
  if request.method == 'POST' and form.is_valid():
    user = form.get_user()
    login(request, user)
    response = redirect('main:show_main')
    response.set_cookie(
        'last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return response
  context = {
      'name': 'Mohammad Zaky Prastio',
      'form': form,
  }
  return render(request, 'login.html', context)


# 4. Logout (Delete Cookie last_login)
def logout_user(request):
  logout(request)
  response = redirect('main:show_main')
  response.delete_cookie('last_login')
  return response


# 5. Lock Tambah & Hapus Proyek (Hanya Superuser)
@login_required(login_url='/login/')
def create_project(request):
  if not request.user.is_superuser:
    raise PermissionDenied
  # ... (isi logika create_project kamu sebelumnya) ...


@login_required(login_url='/login/')
def delete_project(request, project_id):
  if not request.user.is_superuser:
    raise PermissionDenied
  # ... (isi logika delete_project kamu sebelumnya) ...


# 6. Fitur Star Proyek (Pengguna Terdaftar)
@login_required(login_url='/login/')
def toggle_star(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if request.method == 'POST':
    if request.user in project.starred_by.all():
      project.starred_by.remove(request.user)
    else:
      project.starred_by.add(request.user)
  return redirect('main:show_projects')