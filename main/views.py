import datetime
from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.management import call_command
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods
from .models import Contact
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
@ensure_csrf_cookie
def show_experience(request):
    context = {
        'name': 'Mohammad Zaky Prastio',
        'form': ExperienceForm(),
        'can_edit_experience': request.user.is_superuser or is_editor(request.user),
        'can_delete_experience': request.user.is_superuser,
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
    search_query = request.GET.get("search", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()
    if search_query:
        experiences = experiences.filter(
            models.Q(title__icontains=search_query)
            | models.Q(company__icontains=search_query)
            | models.Q(description__icontains=search_query)
        )

    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        data.append({
            "id": experience.id,
            "title": experience.title,
            "company": experience.company,
            "start_date": experience.start_date.isoformat(),
            "is_active": experience.is_active,
            "description": experience.description,
            "star_count": len(starred_users),
            "is_starred": request.user.is_authenticated and any(
                user.pk == request.user.pk for user in starred_users
            ),
        })
    return JsonResponse(data, safe=False)


def create_experience_ajax(request):
    if request.method != "POST":
        return JsonResponse({"message": "Metode tidak diizinkan."}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Silakan login untuk menambahkan pengalaman."}, status=403)
    if not request.user.is_superuser:
        return JsonResponse({"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."}, status=403)

    form = ExperienceForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    experience = form.save()
    return JsonResponse({
        "message": "Pengalaman berhasil ditambahkan.",
        "experience": {
            "id": experience.id,
            "title": experience.title,
            "company": experience.company,
            "start_date": experience.start_date.isoformat(),
            "is_active": experience.is_active,
            "description": experience.description,
            "star_count": 0,
            "is_starred": False,
        },
    }, status=201)


def toggle_experience_star(request, experience_id):
    if request.method != "POST":
        return JsonResponse({"message": "Metode tidak diizinkan."}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Silakan login untuk memberi star."}, status=403)

    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
        is_starred = False
    else:
        experience.starred_by.add(request.user)
        is_starred = True
    return JsonResponse({
        "star_count": experience.starred_by.count(),
        "is_starred": is_starred,
    })

# ==========================================
# VIEWS UNTUK PROJECT (TUTORIAL 05 UPDATE)
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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

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
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)

@ensure_csrf_cookie
def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Mohammad Zaky Prastio",
        "title_query": title_query,
        "form": ProjectForm(),
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
    try:
        call_command('migrate', interactive=False)
        if not User.objects.filter(username="adminpws").exists():
            User.objects.create_superuser("adminpws", "admin@pws.com", "zaky12345")
    except Exception as e:
        print("Auto-migrate error on login:", e)

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

# ==========================================
# TUTOR 6
# ==========================================

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "index.html", {"contacts": contacts})

def contact_add(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
        )
    contacts = Contact.objects.all()
    return render(request, "_contact_rows.html", {"contacts": contacts})

@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return HttpResponse("")

def contact_search(request):
    query = request.GET.get("q", "")
    contacts = Contact.objects.filter(name__icontains=query) if query else Contact.objects.all()
    return render(request, "_contact_rows.html", {"contacts": contacts})

def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "_contact_edit_row.html", {"contact": contact})

def contact_row(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "_contact_row.html", {"contact": contact})

@require_http_methods(["PUT"])
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = QueryDict(request.body)
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    contact.save()
    return render(request, "_contact_row.html", {"contact": contact})