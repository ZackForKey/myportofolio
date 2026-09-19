from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, CheckboxInput
from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/...",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "company",
            "start_date",
            "is_active",
            "description",
        ]

        labels = {
            "title": "Posisi / Peran",
            "company": "Perusahaan / Organisasi",
            "start_date": "Tanggal Mulai",
            "is_active": "Masih Aktif ?",
            "description": "Deskripsi Kegiatan",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Cth: Sales Representative, Wakil Pradana",
                    "maxlength": 255,
                }
            ),
            "company": TextInput(
                attrs={
                    "placeholder": "Cth: SMA Soekarno",
                    "maxlength": 255,
                }
            ),
            "start_date": DateInput(
                attrs={
                    "type": "date", #  biar muncul kalender di browser
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan tanggung jawab dan pencapaianmu...",
                    "rows": 3,
                }
            ),
            # CheckboxInput secara default dipertegas di sini
            "is_active": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }