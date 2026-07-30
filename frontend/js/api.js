const BASE_URL = '/api/v1'

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
function setUser(user) {
    saveUser(user)
}

function getUser() {
    const u = localStorage.getItem('user')
    return u ? JSON.parse(u) : null
}

async function fetchCurrentUser() {
    const token = getToken()
    if (!token) return null
    try {
        const res = await api('/auth/me/')
        if (res && res.ok) {
            const data = await res.json()
            saveUser(data)
            return data
        }
    } catch (e) {}
    return getUser()
}

function requireAuth() {
    if (!getToken()) window.location.href = '/login/'
}


async function api(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    if (options.body instanceof FormData) {
        delete headers['Content-Type']
    }
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

// Apply saved theme automatically on script load
(function applySavedTheme() {
    const theme = localStorage.getItem('swipe_theme') || 'default'
    const root = document.documentElement
    if (theme === 'oled') {
        root.style.setProperty('--bg', '#000000')
        root.style.setProperty('--bg2', '#0a0a0a')
        root.style.setProperty('--bg3', '#141414')
        root.style.setProperty('--accent', '#3b82f6')
    } else if (theme === 'cyber') {
        root.style.setProperty('--bg', '#09090e')
        root.style.setProperty('--bg2', '#12111a')
        root.style.setProperty('--bg3', '#1c1b26')
        root.style.setProperty('--accent', '#f43f5e')
    } else if (theme === 'emerald') {
        root.style.setProperty('--bg', '#061712')
        root.style.setProperty('--bg2', '#0d2820')
        root.style.setProperty('--bg3', '#16382e')
        root.style.setProperty('--accent', '#10b981')
    } else {
        root.style.removeProperty('--bg')
        root.style.removeProperty('--bg2')
        root.style.removeProperty('--bg3')
        root.style.removeProperty('--accent')
    }
})()

async function initNotifications() {
    if (!getToken()) return
    const navLinks = document.querySelector('.nav-links')
    if (!navLinks || document.getElementById('notif-bell-wrap')) return

    const wrap = document.createElement('div')
    wrap.className = 'nav-notif-wrap'
    wrap.id = 'notif-bell-wrap'
    wrap.innerHTML = `
        <button class="notif-bell-btn" id="notif-bell-btn" onclick="toggleNotifDropdown(event)" title="Notifications">
            🔔 <span class="notif-badge-count" id="notif-badge" style="display:none;">0</span>
        </button>
        <div class="notif-dropdown" id="notif-dropdown" onclick="event.stopPropagation()">
            <div class="notif-header">
                <h4>Notifications</h4>
                <button class="notif-mark-all" onclick="markAllNotificationsRead()">Mark all read</button>
            </div>
            <div class="notif-list" id="notif-list">
                <div style="padding:1.5rem;text-align:center;color:var(--text3);font-size:0.85rem;">Loading notifications...</div>
            </div>
        </div>`

    navLinks.insertBefore(wrap, navLinks.firstChild)

    document.addEventListener('click', () => {
        const drop = document.getElementById('notif-dropdown')
        if (drop) drop.classList.remove('active')
    })

    await fetchNotifications()
    setInterval(fetchNotifications, 15000)
}

function toggleNotifDropdown(e) {
    e.stopPropagation()
    const drop = document.getElementById('notif-dropdown')
    if (drop) drop.classList.toggle('active')
}

async function fetchNotifications() {
    try {
        const res = await api('/notifications/')
        if (res && res.ok) {
            const data = await res.json()
            const badge = document.getElementById('notif-badge')
            const list = document.getElementById('notif-list')

            if (data.unread_count > 0) {
                badge.style.display = 'inline-block'
                badge.textContent = data.unread_count > 99 ? '99+' : data.unread_count
            } else {
                badge.style.display = 'none'
            }

            const notifs = data.notifications || []
            if (notifs.length === 0) {
                list.innerHTML = `<div style="padding:1.5rem;text-align:center;color:var(--text3);font-size:0.85rem;">No notifications yet!</div>`
            } else {
                list.innerHTML = notifs.map(n => `
                    <div class="notif-item ${n.is_read ? '' : 'unread'}" onclick="handleNotifClick('${n.id}', '${n.link || ''}')">
                        <div style="flex:1;">
                            <div class="notif-item-title">${n.title}</div>
                            <div class="notif-item-msg">${n.message}</div>
                            <div class="notif-item-time">${new Date(n.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</div>
                        </div>
                    </div>`).join('')
            }
        }
    } catch {}
}

async function handleNotifClick(id, link) {
    try {
        await api(`/notifications/${id}/read/`, { method: 'PATCH' })
    } catch {}
    if (link && link !== 'null') {
        window.location.href = link
    } else {
        await fetchNotifications()
    }
}

async function markAllNotificationsRead() {
    try {
        const res = await api('/notifications/mark-all-read/', { method: 'POST' })
        if (res && res.ok) {
            showToast('All notifications marked as read.')
            await fetchNotifications()
        }
    } catch {}
}

function initMobileNav() {
    const nav = document.querySelector('.nav')
    const navLinks = document.querySelector('.nav-links')
    if (!nav || !navLinks || document.getElementById('nav-toggle-btn')) return

    const toggleBtn = document.createElement('button')
    toggleBtn.className = 'nav-toggle-btn'
    toggleBtn.id = 'nav-toggle-btn'
    toggleBtn.setAttribute('aria-label', 'Toggle menu')
    toggleBtn.innerHTML = '☰'
    
    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation()
        const isOpen = navLinks.classList.toggle('open')
        toggleBtn.innerHTML = isOpen ? '✕' : '☰'
    })

    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('open') && !nav.contains(e.target)) {
            navLinks.classList.remove('open')
            toggleBtn.innerHTML = '☰'
        }
    })

    navLinks.querySelectorAll('a, button').forEach(item => {
        item.addEventListener('click', () => {
            navLinks.classList.remove('open')
            toggleBtn.innerHTML = '☰'
        })
    })

    nav.appendChild(toggleBtn)
}

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav()
    if (getToken()) initNotifications()
})