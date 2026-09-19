from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',    
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