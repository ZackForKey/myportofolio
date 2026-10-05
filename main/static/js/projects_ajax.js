(() => {
    const grid = document.getElementById('grid');
    if (!grid) return;
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const empty = document.getElementById('empty');
    const searchForm = document.getElementById('project-search-form');
    const searchInput = document.getElementById('search-input');
    const projectForm = document.getElementById('project-form');
    let debounceTimer;
    let controller;

    function setState(state) {
        loading?.classList.toggle('hide', state !== 'loading');
        error?.classList.toggle('hide', state !== 'error');
        empty?.classList.toggle('hide', state !== 'empty');
        grid.classList.toggle('hide', state !== 'list');
    }

    function safeExternalUrl(value) {
        try {
            const url = new URL(value, window.location.origin);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch {
            return '';
        }
    }

    function textElement(tag, className, value) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        element.textContent = value ?? '';
        return element;
    }

    function buildCard(item) {
        const project = item.fields;
        const card = document.createElement('article');
        card.className = 'project-card';
        const imageUrl = safeExternalUrl(project.project_image_url);
        if (imageUrl) {
            const image = document.createElement('img');
            image.src = imageUrl;
            image.alt = `Gambar ${project.title ?? 'proyek'}`;
            image.className = 'project-image';
            card.appendChild(image);
        }
        card.append(
            textElement('h2', '', project.title),
            textElement('span', 'project-category', project.tech_stack),
            textElement('p', 'project-description', project.description),
        );
        const actions = document.createElement('div');
        actions.className = 'project-card-actions';
        const row = document.createElement('div');
        row.className = 'project-actions';
        const projectUrl = safeExternalUrl(project.project_url);
        if (projectUrl) {
            const link = textElement('a', 'button button-white', 'Lihat Project');
            link.href = projectUrl;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            row.appendChild(link);
        }
        const form = document.createElement('form');
        form.method = 'post';
        form.action = `/projects/${encodeURIComponent(item.pk)}/star/`;
        form.className = 'star-form';
        const csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = window.getCookie?.('csrftoken') || '';
        form.appendChild(csrf);
        const button = document.createElement('button');
        button.type = 'submit';
        button.className = `button button-star${project.is_starred ? ' is-starred' : ''}`;
        button.title = project.star_count ? `Star oleh ${project.starred_by_names}` : 'Jadilah yang pertama memberi star';
        button.append('★ ', project.is_starred ? 'Unstar ' : 'Star ');
        button.appendChild(textElement('span', 'star-count', project.star_count));
        form.appendChild(button);
        row.appendChild(form);
        actions.appendChild(row);
        card.appendChild(actions);
        return card;
    }

    async function loadProjects(query = '') {
        controller?.abort();
        controller = new AbortController();
        setState('loading');
        const url = new URL('/api/projects/', window.location.origin);
        if (query) url.searchParams.set('title', query);
        try {
            const response = await fetch(url, { headers: { Accept: 'application/json' }, signal: controller.signal });
            if (!response.ok) throw new Error(`Request gagal (${response.status})`);
            const projects = await response.json();
            grid.replaceChildren();
            if (!projects.length) return setState('empty');
            projects.forEach(project => grid.appendChild(buildCard(project)));
            setState('list');
        } catch (fetchError) {
            if (fetchError.name === 'AbortError') return;
            setState('error');
            window.showToast?.('Gagal memuat projects', 'Periksa koneksi lalu coba lagi.', 'error');
        }
    }

    searchInput?.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => loadProjects(searchInput.value.trim()), 300);
    });
    searchForm?.addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(debounceTimer);
        loadProjects(searchInput?.value.trim() || '');
    });

    if (projectForm) {
        projectForm.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = projectForm.querySelector('button[type="submit"]');
            if (submit) submit.disabled = true;
            try {
                const response = await fetch(projectForm.action, {
                    method: 'POST',
                    headers: { Accept: 'application/json', 'X-CSRFToken': window.getCookie?.('csrftoken') || '' },
                    body: new FormData(projectForm),
                });
                const result = await response.json().catch(() => ({}));
                if (response.status === 201) {
                    projectForm.reset();
                    document.getElementById('add-project-modal')?.hidePopover();
                    window.showToast?.('Berhasil', result.message || 'Proyek baru berhasil ditambahkan.', 'success');
                    await loadProjects(searchInput?.value.trim() || '');
                    return;
                }
                const messages = result.errors
                    ? Object.values(result.errors).flat().map(item => item.message)
                    : [result.message || `Terjadi kesalahan (status ${response.status}).`];
                window.showToast?.('Gagal menambahkan proyek', messages.join(' '), 'error');
            } catch {
                window.showToast?.('Gagal menambahkan proyek', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
            } finally {
                if (submit) submit.disabled = false;
            }
        });
    }

    loadProjects(searchInput?.value.trim() || '');
})();
