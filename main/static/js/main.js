document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("api-experience-container");
    
    // Biar nggak error kalau file JS ini diload di halaman lain yang nggak ada edu-container
    if (!container) return; 

    fetch("/api/experiences/")
        .then(response => {
            if (!response.ok) throw new Error("Gagal mengambil data API");
            return response.json();
        })
        .then(data => {
            container.innerHTML = "";
            
            if (data.length === 0) {
                container.innerHTML = "<p style='text-align: center; color: #64748b;'>Belum ada pengalaman yang ditambahkan.</p>";
                return;
            }

            data.forEach(exp => {
                const startDate = new Date(exp.start_date).toLocaleDateString('id-ID', { year: 'numeric', month: 'long' });
                const statusText = exp.is_active ? "Sekarang" : "Selesai";

                const cardHTML = `
                <div class="edu-card">
                    <div class="edu-header">
                        <div class="edu-logo" style="background: #e2e8f0; display:flex; align-items:center; justify-content:center; border-radius:8px; font-weight:bold; color:#475569; width: 50px; height: 50px; flex-shrink: 0;">
                            ${exp.company.charAt(0).toUpperCase()}
                        </div>
                        
                        <div class="edu-title-group">
                            <h3>${exp.company}</h3>
                            <p class="edu-sub">${exp.title} &bull; ${startDate} - ${statusText}</p>
                        </div>
                        
                        <details class="edu-dropdown">
                            <summary class="arrow-btn" title="Lihat detail kegiatan">&#9660;</summary>
                            <div class="edu-details" style="padding-top: 10px;">
                                <p style="white-space: pre-wrap; font-size: 0.9rem; color: #475569; margin: 0;">${exp.description}</p>
                            </div>
                        </details>
                    </div>
                    
                    <div style="padding: 10px 20px; border-top: 1px solid #e2e8f0; display: flex; align-items: center; gap: 8px;">
                        <button onclick="toggleStarExperience('${exp.id}', this)" style="background: none; border: none; cursor: pointer; font-size: 1.2rem; padding: 0;">
                            ${exp.is_starred ? '⭐' : '☆'}
                        </button>
                        <span class="star-count" style="font-size: 0.9rem; color: #64748b;">${exp.star_count} stars</span>
                    </div>
                </div>
                `;
                container.innerHTML += cardHTML;
            });
        })
        .catch(error => {
            console.error("Error:", error);
            container.innerHTML = "<p style='text-align: center; color: #ef4444;'>Gagal memuat data pengalaman.</p>";
        });
});

window.toggleStarExperience = function(experienceId, buttonElement) {
    const csrfTokenMatch = document.cookie.match(/csrftoken=([^;]+)/);
    const csrfToken = csrfTokenMatch ? csrfTokenMatch[1] : '';

    fetch(`/api/experiences/${experienceId}/star/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 403) {
            alert("Lu harus login dulu buat ngasih star!");
            throw new Error("Not authenticated");
        }
        return response.json();
    })
    .then(updatedData => {
        buttonElement.innerHTML = updatedData.is_starred ? '⭐' : '☆';
        buttonElement.nextElementSibling.innerText = `${updatedData.star_count} stars`;
    })
    .catch(err => console.log(err));
};
// --- SCRIPT UNTUK FORM CONTACT ---
const contactForm = document.getElementById("api-contact-form");
if (contactForm) {
    contactForm.addEventListener("submit", function(e) {
        e.preventDefault(); // Mencegah halaman reload pas disubmit
        
        const name = document.getElementById("contact-name").value;
        const email = document.getElementById("contact-email").value;
        
        // Ambil CSRF token
        const csrfTokenMatch = document.cookie.match(/csrftoken=([^;]+)/);
        const csrfToken = csrfTokenMatch ? csrfTokenMatch[1] : '';

        fetch("/api/contacts/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name, email: email })
        })
        .then(response => {
            if (!response.ok) throw new Error("Gagal mengirim pesan");
            return response.json();
        })
        .then(data => {
            // Munculin notifikasi sukses
            const alertBox = document.getElementById("contact-alert");
            alertBox.style.display = "block";
            
            // Kosongin form setelah sukses
            contactForm.reset();
            
            // Ilangin notifikasi setelah 3 detik
            setTimeout(() => {
                alertBox.style.display = "none";
            }, 3000);
        })
        .catch(err => {
            console.error(err);
            alert("Terjadi kesalahan saat mengirim pesan.");
        });
    });
}