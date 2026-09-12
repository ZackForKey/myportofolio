import uuid
from django.utils import timezone
from django.shortcuts import render
from portofolio_main.models import Experience

def show_main(request):
    context = {
        "name": "Mohammad Zaky Prastio",
        "npm": "240657011",
        "study_program": "S1 Ilmu Komputer",
        "bio": "Computer Science undergraduate at Universitas Indonesia with a keen interest in robotics technology, embedded systems, and software engineering, combining a strong foundation in digital logic and hardware simulation with practical Python development, computer vision projects, and full-stack technical problem solving.",
    }
    return render(request, "main.html", context)

def show_experience(request):
    exp1 = Experience(
        id=uuid.uuid4(),
        title="Staff Departemen Olahraga BEM Fasilkom UI",
        description="Aktif berkontribusi sebagai Staff Departemen Olahraga (Depor) BEM Fasilkom UI 2026. Menjadi Penanggung Jawab / Pemegang Unit Kegiatan Olahraga (UKOR) Voli serta terlibat langsung dalam perencanaan dan pelaksanaan program kerja Olimpiade Universitas Indonesia (Olim UI).",
        category="volunteer",
        thumbnail="",
        started_at=timezone.now(),
        ended_at=None  
    )
    
    exp2 = Experience(
        id=uuid.uuid4(),
        title="Koordinator Lapangan - Laskar Biru Merah (LBM)",
        description="Bergabung dalam Laskar Biru Merah (LBM), kelompok suporter Fasilkom UI yang memberikan semangat kepada kontingen CSUI dalam berbagai ajang kompetisi antar fakultas. Bertanggung jawab sebagai Koordinator Lapangan yang mengatur jalannya kegiatan suporteran, koordinasi massa, serta akomodasi dan peralatan.",
        category="volunteer",
        thumbnail="",
        started_at=timezone.now(),
        ended_at=None
    )

    context = {
        "name": "Mohammad Zaky Prastio",
        "experience_list": [exp1, exp2],
    }
    return render(request, "experience.html", context)