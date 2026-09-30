let toastTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
  const toastComponent = document.getElementById('toast-component');
  const toastTitle = document.getElementById('toast-title');
  const toastMessage = document.getElementById('toast-message');

  if (!toastComponent) return;

  // Hapus class tipe sebelumnya
  toastComponent.classList.remove('toast-success', 'toast-error', 'toast-normal');

  // Terapkan class baru berdasarkan tipe
  if (type === 'success') {
      toastComponent.classList.add('toast-success');
  } else if (type === 'error') {
      toastComponent.classList.add('toast-error');
  } else {
      toastComponent.classList.add('toast-normal');
  }

  // Perbarui konten teks
  toastTitle.textContent = title;
  toastMessage.textContent = message;

  // Batalkan timer sebelumnya jika toast masih tampil
  clearTimeout(toastTimer);

  // Animasi muncul
  if (!toastComponent.matches(':popover-open')) {
      toastComponent.showPopover();
      void toastComponent.offsetHeight; // paksa browser menghitung style agar transisi berjalan
  }

  toastComponent.classList.remove('toast-hidden');
  toastComponent.classList.add('toast-show');

  // Animasi hilang otomatis
  toastTimer = setTimeout(() => {
      toastComponent.classList.remove('toast-show');
      toastComponent.classList.add('toast-hidden');
      toastTimer = setTimeout(() => toastComponent.hidePopover(), 300);
  }, duration);
}
// Konfigurasi Endpoint
const BASE_PROJECTS_ENDPOINT = "/api/projects/"; // Sesuaikan endpoint JSON proyek lo jika beda
const CREATE_PROJECT_ENDPOINT = "/projects/add-ajax/";
let projectsAbortController;

// DOM Elements
const loadingState = document.getElementById('loading');
const errorState = document.getElementById('error');
const emptyState = document.getElementById('empty');
const gridContainer = document.getElementById('grid');
const searchForm = document.getElementById('project-search-form');
const searchInput = document.getElementById('search-input');
const projectForm = document.getElementById('project-form');

// Mengontrol section yang tampil
function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
    loadingState.classList.toggle('hide', !showLoading);
    errorState.classList.toggle('hide', !showError);
    emptyState.classList.toggle('hide', !showEmpty);
    gridContainer.classList.toggle('hide', !showGrid);
}

// Escaping XSS
function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function closeProjectModal() {
    const modal = document.getElementById("add-project-modal");
    if (modal) modal.hidePopover();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Merakit elemen Kartu Proyek (Client-side rendering)
function buildProjectCardElement(item) {
    const project = item.fields;
    const projectId = item.pk;
    const articleElement = document.createElement('article');
    articleElement.className = 'project-card';

    const imageHtml = project.project_image_url 
        ? `<img src="${escapeHtml(project.project_image_url)}" alt="Gambar ${escapeHtml(project.title)}" class="project-image">`
        : '';
        
    const urlHtml = project.project_url 
        ? `<a href="${escapeHtml(project.project_url)}" class="button button-white" target="_blank">Lihat Project</a>`
        : '';

    const deleteUrl = `/projects/delete/${projectId}/`;
    const updateUrl = `/projects/update/${projectId}/`;
    const starUrl = `/projects/star/${projectId}/`;

    const isStarredClass = project.is_starred ? " is-starred" : "";
    const starText = project.is_starred ? "Unstar" : "Star";
    const starTitle = project.star_count > 0 
        ? `Dibintangi oleh ${escapeHtml(project.starred_by_names)}` 
        : "Jadilah yang pertama memberi star";

    const completeCardHtml = `
        ${imageHtml}
        <h2>${escapeHtml(project.title)}</h2>
        <span class="project-category">${escapeHtml(project.tech_stack)}</span>
        <p class="project-description">${escapeHtml(project.description)}</p>
        <div class="project-card-actions">
            <div class="project-actions">
                ${urlHtml}
                <form method="post" action="${starUrl}" class="star-form">
                    <button type="submit" class="button button-star${isStarredClass}" title="${starTitle}">
                        <span aria-hidden="true">★</span>
                        ${starText}
                        <span class="star-count">${project.star_count}</span>
                    </button>
                </form>
            </div>
        </div>
    `;
    articleElement.innerHTML = completeCardHtml;
    return articleElement;
}

// Fetch Data Proyek via AJAX
async function fetchProjects(searchQuery = "") {
    if (projectsAbortController) projectsAbortController.abort();
    projectsAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });
        const url = searchQuery ? `${BASE_PROJECTS_ENDPOINT}?title=${encodeURIComponent(searchQuery)}` : BASE_PROJECTS_ENDPOINT;
        
        const response = await fetch(url, {
            headers: { 'Accept': 'application/json' },
            signal: projectsAbortController.signal,
        });

        if (!response.ok) throw new Error('Failed to fetch data');

        const projectData = await response.json();

        if (projectData.length === 0) {
            displayPageSection({ showEmpty: true });
        } else {
            gridContainer.innerHTML = '';
            projectData.forEach(item => {
                gridContainer.appendChild(buildProjectCardElement(item));
            });
            displayPageSection({ showGrid: true });
        }
    } catch (error) {
        if (error.name === 'AbortError') return;
        console.error('Error loading projects:', error);
        displayPageSection({ showError: true });
    }
}

// Search Debouncing (300ms)
const SEARCH_DEBOUNCE_DELAY = 300;
let searchDebounceTimer;

function searchProjects() {
    if (searchInput) fetchProjects(searchInput.value.trim());
}

if (searchInput) {
    searchInput.addEventListener("input", function() {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(function() {
            searchProjects();
        }, SEARCH_DEBOUNCE_DELAY);
    });
}

if (searchForm) {
    searchForm.addEventListener("submit", function(event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchProjects();
    });
}

// Submit Form Tambah Proyek via AJAX
async function addProject(event) {
    event.preventDefault();
    const submitButton = projectForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    try {
        const response = await fetch(CREATE_PROJECT_ENDPOINT, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: new FormData(projectForm),
        });
        const result = await response.json().catch(() => ({}));
        if (response.ok) {
            projectForm.reset();
            closeProjectModal();
            if (typeof showToast === 'function') {
                showToast('Berhasil', 'Proyek baru berhasil ditambahkan!', 'success');
            }
            fetchProjects(searchInput ? searchInput.value.trim() : "");
        } else {
            const errorMessages = result.errors 
                ? Object.values(result.errors).flat().map(error => error.message) 
                : [result.message || `Terjadi kesalahan (status ${response.status}).`];
            if (typeof showToast === 'function') {
                showToast('Gagal menambahkan proyek', errorMessages.join(' '), 'error');
            }
        }
    } catch (error) {
        console.error('Error adding project:', error);
        if (typeof showToast === 'function') {
            showToast('Gagal menambahkan proyek', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
        }
    } finally {
        submitButton.disabled = false;
    }
}

if (projectForm) {
    projectForm.addEventListener('submit', addProject);
}

// Initial Load
fetchProjects(searchInput ? searchInput.value.trim() : "");