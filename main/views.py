from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from main.models import Project
from main.forms import ProjectForm

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',    
    }
    return render(request, "main.html", context)

def show_experience(request):
    # Data manual jika belum diisi di database
    experience_list = [
        {
            'title': 'Staff Departemen Olahraga BEM Fasilkom UI',
            'get_category_display': 'Organization',
            'description': 'Aktif berkontribusi sebagai Staff Departemen Olahraga (Depor) BEM Fasilkom UI 2026. Menjadi Penanggung Jawab / Pemegang Unit Kegiatan Olahraga (UKOR) Voli serta terlibat langsung dalam perencanaan dan pelaksanaan program kerja Olimpiade Universitas Indonesia (Olim UI).',
            'is_ongoing': True,
        },
        {
            'title': 'Koordinator Lapangan - Laskar Biru Merah (LBM)',
            'get_category_display': 'Organization',
            'description': 'Bergabung dalam Laskar Biru Merah (LBM), kelompok suporter Fasilkom UI. Bertanggung jawab sebagai Koordinator Lapangan yang mengatur jalannya kegiatan suporteran, koordinasi massa, serta akomodasi dan peralatan.',
            'is_ongoing': True,
        }
    ]
    
    context = {
        'name': 'Mohammad Zaky Prastio',
        'experience_list': experience_list,
    }
    return render(request, 'experience.html', context)

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