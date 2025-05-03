export function getSession() {
    const userData = localStorage.getItem('userData');
    if (userData) {
        return JSON.parse(userData);
    }
    return null;
}

export function isLoggedIn() {
    return getSession() !== null;
}

export function clearSession() {
    localStorage.removeItem('userData');
    window.location.href = '/';
}

export function setSession(userData) {
    localStorage.setItem('userData', JSON.stringify(userData));
}

// Make logout function available globally
window.logout = clearSession;
