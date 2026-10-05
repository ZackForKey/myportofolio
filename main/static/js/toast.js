let toastTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    if (!toast || !toastTitle || !toastMessage) return;

    toast.classList.remove('toast-success', 'toast-error', 'toast-normal');
    toast.classList.add(type === 'success' ? 'toast-success' : type === 'error' ? 'toast-error' : 'toast-normal');
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    clearTimeout(toastTimer);

    if (!toast.matches(':popover-open')) toast.showPopover();
    toast.classList.remove('toast-hidden');
    toast.classList.add('toast-show');
    toastTimer = setTimeout(() => {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hidden');
        setTimeout(() => toast.hidePopover(), 300);
    }, duration);
}

function getCookie(name) {
    const prefix = `${name}=`;
    const entry = document.cookie.split(';').map(value => value.trim()).find(value => value.startsWith(prefix));
    return entry ? decodeURIComponent(entry.slice(prefix.length)) : null;
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[character]);
}

window.showToast = showToast;
window.getCookie = getCookie;
window.escapeHtml = escapeHtml;
