const BASE_URL = 'http://127.0.0.1:8000/api/v1'

function getToken() {
    return localStorage.getItem('access_token')
}

function saveTokens(access, refresh) {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
}

function clearTokens() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
}

function saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
}

function getUser() {
    const u = localStorage.getItem('user')
    return u ? JSON.parse(u) : null
}

function requireAuth() {
    if (!getToken()) window.location.href = '/login/'
}

async function api(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`

    const res = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers })

    if (res.status === 401) {
        const refreshed = await refreshToken()
        if (!refreshed) { clearTokens(); window.location.href = '/login/'; return }
        headers['Authorization'] = `Bearer ${getToken()}`
        return fetch(`${BASE_URL}${endpoint}`, { ...options, headers })
    }
    return res
}

async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) return false
    const res = await fetch(`${BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    })
    if (res.ok) {
        const data = await res.json()
        localStorage.setItem('access_token', data.access)
        return true
    }
    return false
}

async function apiForm(endpoint, formData, method = 'POST') {
    const token = getToken()
    const headers = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    return fetch(`${BASE_URL}${endpoint}`, { method, headers, body: formData })
}

function showToast(message, type = 'success') {
    const existing = document.getElementById('sc-toast')
    if (existing) existing.remove()
    const toast = document.createElement('div')
    toast.id = 'sc-toast'
    toast.className = `sc-toast sc-toast--${type}`
    toast.textContent = message
    document.body.appendChild(toast)
    setTimeout(() => toast.classList.add('sc-toast--show'), 10)
    setTimeout(() => { toast.classList.remove('sc-toast--show'); setTimeout(() => toast.remove(), 300) }, 3000)
}

function showError(fieldId, message) {
    const el = document.getElementById(fieldId)
    if (el) { el.textContent = message; el.style.display = 'block' }
}

function clearErrors() {
    document.querySelectorAll('.sc-error').forEach(e => { e.textContent = ''; e.style.display = 'none' })
}

function logout() {
    const refresh = localStorage.getItem('refresh_token')
    if (refresh) {
        api('/auth/logout/', { method: 'POST', body: JSON.stringify({ refresh }) })
    }
    clearTokens()
    window.location.href = '/'
}