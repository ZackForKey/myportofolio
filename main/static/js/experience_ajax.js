(() => {
    const section = document.getElementById('experience');
    if (!section) return;

    const list = document.getElementById('experience-list');
    const loading = document.getElementById('experience-loading');
    const empty = document.getElementById('experience-empty');
    const error = document.getElementById('experience-error');
    const searchForm = document.getElementById('experience-search-form');
    const searchInput = document.getElementById('experience-search-input');
    const retryButton = document.getElementById('retry-experience-load');
    const modal = document.getElementById('experience-modal');
    const addForm = document.getElementById('experience-form');
    const formErrors = document.getElementById('experience-form-errors');
    let debounceTimer;
    let requestController;

    function setState(state) {
        loading.classList.toggle('hide', state !== 'loading');
        empty.classList.toggle('hide', state !== 'empty');
        error.classList.toggle('hide', state !== 'error');
        list.classList.toggle('hide', state !== 'list');
    }

    function makeTextElement(tag, className, value) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        element.textContent = value ?? '';
        return element;
    }

    function buildCard(item) {
        const card = document.createElement('details');
        card.className = 'exp-card';

        const summary = document.createElement('summary');
        summary.className = 'exp-header';
        const titleGroup = document.createElement('div');
        titleGroup.className = 'exp-title-group';
        titleGroup.appendChild(makeTextElement('h3', '', item.title));
        const status = item.is_active ? 'Sedang berlangsung' : 'Selesai';
        const date = new Date(`${item.start_date}T00:00:00`).toLocaleDateString('id-ID', {
            day: '2-digit', month: 'short', year: 'numeric'
        });
        titleGroup.appendChild(makeTextElement('p', 'exp-sub', `${item.company} • Mulai: ${date} • ${status}`));
        summary.append(titleGroup, makeTextElement('span', 'exp-arrow', '▼'));
        card.appendChild(summary);

        const details = document.createElement('div');
        details.className = 'exp-details';
        details.appendChild(makeTextElement('p', '', item.description));

        const actions = document.createElement('div');
        actions.className = 'experience-card-actions';
        const updateUrl = section.dataset.updateUrlTemplate.replace('/0/update/', `/${item.id}/update/`);
        const deleteUrl = section.dataset.deleteUrlTemplate.replace('/0/delete/', `/${item.id}/delete/`);
        if (section.dataset.canEdit === 'true') {
            const editLink = makeTextElement('a', 'button button-secondary', 'Edit');
            editLink.href = updateUrl;
            actions.appendChild(editLink);
        }
        if (section.dataset.canDelete === 'true') {
            const deleteForm = document.createElement('form');
            deleteForm.method = 'post';
            deleteForm.action = deleteUrl;
            deleteForm.className = 'experience-delete-form';
            const csrf = document.createElement('input');
            csrf.type = 'hidden';
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = window.getCookie?.('csrftoken') || '';
            const deleteButton = makeTextElement('button', 'button button-delete', 'Hapus');
            deleteButton.type = 'submit';
            deleteForm.append(csrf, deleteButton);
            deleteForm.addEventListener('submit', event => {
                if (!window.confirm('Yakin ingin menghapus pengalaman ini?')) event.preventDefault();
            });
            actions.appendChild(deleteForm);
        }
        const star = document.createElement('button');
        star.type = 'button';
        star.className = `button button-star${item.is_starred ? ' is-starred' : ''}`;
        star.setAttribute('aria-pressed', String(Boolean(item.is_starred)));
        star.dataset.id = item.id;
        star.append('★ ', item.is_starred ? 'Unstar ' : 'Star ');
        const count = makeTextElement('span', 'star-count', item.star_count);
        star.appendChild(count);
        actions.appendChild(star);
        details.appendChild(actions);
        card.appendChild(details);
        return card;
    }

    async function loadExperiences(query = '') {
        if (requestController) requestController.abort();
        requestController = new AbortController();
        setState('loading');
        const url = new URL(section.dataset.listUrl, window.location.origin);
        if (query) url.searchParams.set('search', query);
        try {
            const response = await fetch(url, {
                headers: { Accept: 'application/json' },
                signal: requestController.signal,
            });
            if (!response.ok) throw new Error(`Request gagal (${response.status})`);
            const items = await response.json();
            list.replaceChildren();
            if (!items.length) {
                setState('empty');
                return;
            }
            items.forEach(item => list.appendChild(buildCard(item)));
            setState('list');
        } catch (fetchError) {
            if (fetchError.name === 'AbortError') return;
            setState('error');
            if (typeof window.showToast === 'function') {
                window.showToast('Gagal memuat pengalaman', 'Periksa koneksi lalu coba lagi.', 'error');
            }
        }
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => loadExperiences(searchInput.value.trim()), 300);
        });
    }
    if (searchForm) {
        searchForm.addEventListener('submit', event => {
            event.preventDefault();
            clearTimeout(debounceTimer);
            loadExperiences(searchInput ? searchInput.value.trim() : '');
        });
    }
    if (retryButton) retryButton.addEventListener('click', () => loadExperiences(searchInput?.value.trim() ?? ''));

    const closeModal = () => {
        if (modal?.open) modal.close();
        if (formErrors) formErrors.textContent = '';
    };
    const openButton = document.getElementById('open-experience-modal');
    const closeButton = document.getElementById('close-experience-modal');
    const cancelButton = document.getElementById('cancel-experience-modal');
    if (openButton && modal) openButton.addEventListener('click', () => modal.showModal());
    if (closeButton) closeButton.addEventListener('click', closeModal);
    if (cancelButton) cancelButton.addEventListener('click', closeModal);
    if (modal) modal.addEventListener('click', event => {
        if (event.target === modal) closeModal();
    });

    if (addForm) {
        addForm.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = addForm.querySelector('button[type="submit"]');
            if (submit) submit.disabled = true;
            if (formErrors) formErrors.textContent = '';
            try {
                const response = await fetch(addForm.action, {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'X-CSRFToken': window.getCookie ? window.getCookie('csrftoken') : '',
                    },
                    body: new FormData(addForm),
                });
                const result = await response.json().catch(() => ({}));
                if (response.status === 201) {
                    addForm.reset();
                    closeModal();
                    await loadExperiences(searchInput?.value.trim() ?? '');
                    window.showToast?.('Berhasil', result.message || 'Pengalaman berhasil ditambahkan.', 'success');
                    return;
                }
                const messages = result.errors
                    ? Object.values(result.errors).flat().map(item => item.message)
                    : [result.message || `Terjadi kesalahan (status ${response.status}).`];
                if (formErrors) formErrors.textContent = messages.join(' ');
                window.showToast?.('Gagal menambahkan pengalaman', messages.join(' '), 'error');
            } catch (submitError) {
                if (formErrors) formErrors.textContent = 'Tidak dapat terhubung ke server. Silakan coba lagi.';
                window.showToast?.('Gagal menambahkan pengalaman', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
            } finally {
                if (submit) submit.disabled = false;
            }
        });
    }

    list.addEventListener('click', async event => {
        const button = event.target.closest('button[data-id]');
        if (!button) return;
        button.disabled = true;
        const url = section.dataset.starUrlTemplate.replace('/0/star/', `/${button.dataset.id}/star/`);
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { Accept: 'application/json', 'X-CSRFToken': window.getCookie?.('csrftoken') || '' },
            });
            const result = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(result.message || 'Star tidak dapat diperbarui.');
            const starred = Boolean(result.is_starred);
            button.classList.toggle('is-starred', starred);
            button.setAttribute('aria-pressed', String(starred));
            button.firstChild.textContent = starred ? '★ Unstar ' : '★ Star ';
            button.querySelector('.star-count').textContent = result.star_count;
            window.showToast?.(starred ? 'Star ditambahkan' : 'Star dihapus', '', 'success');
        } catch (starError) {
            window.showToast?.('Star gagal diperbarui', starError.message, 'error');
        } finally {
            button.disabled = false;
        }
    });

    loadExperiences();
})();
