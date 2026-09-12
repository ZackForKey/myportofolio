from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',     }

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
    return render(request, 'experience.html', context) # Sesuaikan nama template HTML kamu