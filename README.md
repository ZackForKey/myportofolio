Nama : ZackForKey PBP B

Status: Latihan Branching
deployyyy
2 september 2026 Sudah berhasi deploy
3 september 2026 Masukin Database Done.
4 dan 5 spt adding html and css

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti <section> untuk memisahkan bagian utama halaman serta <header> dan <footer> di dalam web. Penggunaan elemen ini membantu membuat kode HTML jauh lebih terstruktur. Selain itu, elemen semantik mempermudah proses styling CSS dan membantu screen reader memahami konteks bagian halaman dengan lebih akurat.

2. Tantangan terbesar dalam menjaga responsivitas adalah menyesuaikan tata letak kartu riwayat pendidikan dan logo Sekolah yang awalnya melebar secara horizontal di layar desktop agar bisa bertumpuk secara vertikal dan rapi di layar mobile. Saya mengevaluasinya dengan memanfaatkan properti Flexbox (flex-wrap) serta CSS Media Queries.

3. Batasan utama yang dirasakan pada web statis murni ini adalah kerumitan saat mengatur tata letak visual secara manual menggunakan CSS murni—seperti menyelaraskan posisi logo instansi, merapikan elemen interaktif tambahan, serta menjaga agar transisi tampilannya tetap mulus. Selain itu, konten informasi masih kaku karena belum menggunakan database. Pada iterasi proyek selanjutnya, fungsionalitas dinamis yang paling ingin dipersiapkan adalah pemanfaatan arsitektur MVT Django dan database untuk pengelolaan data, serta eksplorasi efek visual tingkat lanjut seperti animasi pop-up yang lebih smooth dan estetis untuk meningkatkan pengalaman pengguna (UI/UX).

**AI Disclosure:**
Dalam pengerjaan tugas ini, saya menggunakan bantuan AI sebagai rekan diskusi dan sparring partner untuk merumuskan struktur kode CSS khusus section pendidikan, merapikan tata letak flexbox, serta membantu menyusun kalimat refleksi agar lebih terstruktur. Seluruh implementasi kode akhir, penyesuaian desain, dan integrasi ke repositori tetap saya lakukan dan uji secara mandiri.

### Tugas 2
1. **Alur Permintaan (Request-Response Cycle) Django MVT:**
   * **`urls.py` Proyek:** Menerima *HTTP request* pertama kali dari pengguna/browser. File ini bertindak sebagai (*router*) yang mengarahkan jalur URL tertentu ke `urls.py` milik aplikasi terkait menggunakan fungsi `include()`.
   * **`urls.py` Aplikasi:** Memetakan URL spesifik aplikasi ke fungsi atau kelas *view* tertentu yang bertanggung jawab menangani permintaan tersebut.
   * **View (`views.py`):** Bertindak sebagai otak. View menerima permintaan, lalu meminta/mengambil data yang dibutuhkan dari **Model**.
   * **Model (`models.py`):** Mewakili struktur data dan berinteraksi langsung dengan database melalui Django ORM untuk mengambil, menyimpan, atau memperbarui data (misalnya data proyek portofolio). Data ini kemudian dikembalikan ke *view*.
   * **Template (`.html`):** *View* mengirimkan data dari *Model* ke *Template*. *Template* menggabungkan struktur HTML dengan data tersebut menggunakan Django Template Language (DTL), lalu mengompilasinya menjadi tampilan HTML utuh.
   * **Tampilan Browser:** *View* mengirimkan hasil *render* HTML tersebut sebagai *HTTP Response* kembali ke browser pengguna untuk ditampilkan.

2. **Alasan Menyimpan Data di Model dibanding Hardcode di Template:**
   * **Pemisahan Tanggung Jawab (*Separation of Concerns*):** *Template* hanya berfokus pada UI/UX, sedangkan data dan logika dikelola terpisah di database (*Model*).
   * **Kemudahan Pemeliharaan (*Maintainability*):** Jika ada perubahan data portofolio (misalnya menambah item baru atau mengubah deskripsi), perubahan cukup dilakukan melalui database/Django Admin tanpa perlu menyentuh atau merubah kode HTML di *template*.
   * **Skalabilitas dan Efisiensi:** Data di *Model* dapat ditampilkan secara dinamis menggunakan *looping* (`{% for %}`) di *template*. Jika ditulis langsung di *template*, kode HTML akan menjadi sangat panjang, repetitif, dan sulit dikelola seiring bertambahnya isi portofolio.
   * **Pengolahan Data:** Data yang tersimpan di *Model* dapat dengan mudah difilter, diurutkan, dicari, atau diekspor ke format lain (seperti API JSON) di kemudian hari.

3. **Perbedaan `makemigrations` dan `migrate` serta Contohnya:**
   * **`makemigrations`:** Perintah untuk mendeteksi perubahan yang terjadi pada skema model di file `models.py`, lalu membuatkan file racikan/cetak biru (*blueprint*) migrasi di dalam folder `migrations/`. Perintah ini belum menerapkan perubahan ke database.
   * **`migrate`:** Perintah untuk mengeksekusi file cetak biru migrasi yang telah dibuat oleh `makemigrations` dan menerapkannya secara nyata ke tabel-tabel di dalam database.
   
   **Contoh Perubahan Model:**  
   Misalnya kita menambahkan *field* baru `description` pada model `Portfolio` di `models.py`:
   ```python
   # main/models.py
   from django.db import models

   class Portfolio(models.Model):
       title = models.CharField(max_length=100)
       # Perubahan baru: menambahkan field description
       description = models.TextField()

### AI Disclosure & Declaration

Dalam proses pengerjaan proyek web portofolio ini, saya menggunakan AI Gemini sebagai sarana pembelajaran dan asisten pengembangan. 

Bantuan AI pemanfaatannya mencakup:
* **Perintah Terminal & Lingkungan Kerja:** Membantu verifikasi *command line* (seperti perintah manajemen Django, perintah Git, dan pemecahan masalah *environment*).
* **Pemecahan Masalah (Debugging):** Membantu melacak *error* pada kode dan memberikan panduan perbaikan *syntax*.
* **Pemahaman Konsep & Arsitektur:** Membantu memahami alur kerja MVT Django serta penyusunan logika dasar aplikasi.

### Tugas 3

1. Kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual karena ModelForm dapat menghasilkan elemen form secara otomatis langsung dari model database yang sudah ada, serta mempermudah validasi data dan proses penyimpanan ke database. Selain itu, kita wajib menambahkan `{% csrf_token %}` pada form untuk mencegah serangan Cross-Site Request Forgery (CSRF) dengan memastikan request POST yang masuk benar-benar berasal dari pengguna yang sah.

2. JSON lebih disukai dalam pengembangan web modern dibandingkan XML karena formatnya jauh lebih ringan, ringkas, dan tidak memiliki tag pembuka serta penutup yang panjang. Karena berbasis struktur objek JavaScript (key-value), data JSON dapat langsung di-parsing oleh browser dan bahasa pemrograman modern dengan sangat cepat serta efisien untuk komunikasi API.

3. Alur saat view mengembalikan data dalam bentuk JSON dimulai dari client yang melakukan request ke endpoint URL, lalu Django memanggil fungsi view yang melakukan query database untuk mengambil objek model. Objek tersebut kemudian melalui proses serialization untuk diubah ke format string JSON sebelum dikembalikan sebagai HttpResponse dengan content-type application/json. Serialization diperlukan karena objek model Django berupa objek Python kompleks yang terikat database dan tidak bisa dikirim secara mentah melalui protokol HTTP.

**AI Disclosure:**
Dalam pengerjaan tugas ini, saya menggunakan bantuan AI dengan pendekatan vibe coding untuk membantu menyusun logika CRUD entitas Experience, mengatasi error namespace URL, menyusun styling CSS Obsidian, serta merapikan format jawaban reflektif Tugas 3 agar selaras dengan tugas sebelumnya. Seluruh pengujian dan penerapan akhir dilakukan secara mandiri.