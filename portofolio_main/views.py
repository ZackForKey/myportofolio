from django.shortcuts import render
from portofolio_main.models import Experience

def show_main(request):
    context = {
        "name": "Mohammad Zaky Prastio",
        "npm": "2506657011",
        "study_program": "S1 Ilmu Komputer",
        "bio": "Computer Science undergraduate at Universitas Indonesia with a keen interest in robotics technology, embedded systems, and software engineering, combining a strong foundation in digital logic and hardware simulation with practical Python development, computer vision projects, and full-stack technical problem solving.",
    }
    return render(request, "main.html", context)

def show_experience(request):
    data_exp = Experience.objects.all()
    print("DATA DARI DATABASE:", data_exp) 
    
    context = {
        "name": "Mohammad Zaky Prastio",
        "experience_list": data_exp,
    }
    return render(request, "experience.html", context)