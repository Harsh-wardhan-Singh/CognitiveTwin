import { renderLogin } from './views/loginView.js'
import { renderRegistration } from './views/registrationView.js'
import { renderStudentHome } from './views/studentHomeView.js'
import { renderTeacherClassSelect } from './views/teacherClassSelectView.js'
import { checkExistingSession, logout as authLogout } from './services/auth.js'

export let currentUser = null

export function setUser(user) {
  currentUser = user
  renderApp()
}

export function logout() {
  currentUser = null
  authLogout()
  renderLogin()
}

export function goToLogin() {
  currentUser = null
  renderLogin()
}

export function goToRegistration() {
  currentUser = null
  renderRegistration()
}

/* ============================= */
/* GLOBAL APP SHELL */
/* ============================= */

function renderApp() {
  if (!currentUser) return   //  CRITICAL LINE

  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="app-shell">
      <div class="app-header">
        <div class="app-title">Cognitive Twin</div>
        <button id="logoutBtn" class="glass-btn">Logout</button>
      </div>

      <div id="appContent"></div>
    </div>
  `

  document
    .getElementById('logoutBtn')
    .addEventListener('click', logout)

  routeUser()
}

export function mountView(callback) {
  const container = document.getElementById('appContent')

  if (!container) {
    console.error("appContent not found — are you logged in?")
    return
  }

  callback(container)
}

function routeUser() {
  if (!currentUser) return   // 🔥 CRITICAL

  if (currentUser.role === 'student') {
    renderStudentHome()
  }

  if (currentUser.role === 'teacher') {
    renderTeacherClassSelect()
  }
}

/* ============================= */
/* INITIAL LOAD */
/* ============================= */

// Check if user already has a valid backend session
(async () => {
  try {
    const existingSession = await checkExistingSession()
    if (existingSession) {
      setUser(existingSession)
    } else {
      renderLogin()
    }
  } catch (error) {
    console.error('Startup error:', error)
    renderLogin()
  }
})()