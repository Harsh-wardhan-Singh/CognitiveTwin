import { setUser } from '../testApp.js'
import { getStudentState } from '../services/state.js'
import { login } from '../services/auth.js'
import { goToRegistration } from '../testApp.js'

export function renderLogin() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="login-container">
      <h1>Cognitive Twin</h1>

      <div class="auth-container">
        <div class="role-buttons">
          <button id="studentBtn" class="role-btn">Sign in as Student</button>
          <button id="teacherBtn" class="role-btn">Sign in as Teacher</button>
        </div>

        <div id="authForm" class="auth-form" style="display:none;">
          <div class="form-group">
            <label for="email">Email:</label>
            <input id="email" type="email" placeholder="Enter your email" />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input id="password" type="password" placeholder="Enter your password" />
          </div>
          <button id="loginSubmit" class="submit-btn">Login</button>
          <p id="loginError" style="color:#ff6b6b; margin-top: 10px;"></p>

          <div class="auth-link">
            <p>Don't have an account? <a href="#" id="goToSignupBtn">Create one here</a></p>
          </div>
        </div>
      </div>
    </div>
  `

  let selectedRole = null

  document.getElementById('studentBtn').onclick = () => {
    selectedRole = 'student'
    document.getElementById('authForm').style.display = 'block'
    document.getElementById('email').focus()
  }

  document.getElementById('teacherBtn').onclick = () => {
    selectedRole = 'teacher'
    document.getElementById('authForm').style.display = 'block'
    document.getElementById('email').focus()
  }

  document.getElementById('loginSubmit').onclick = async () => {
    const email = document.getElementById('email').value.trim().toLowerCase()
    const password = document.getElementById('password').value
    const error = document.getElementById('loginError')

    error.textContent = ''

    if (!email || !password) {
      error.textContent = 'Please enter both email and password'
      return
    }

    try {
      const user = await login(email, password, selectedRole)
      setUser({
        role: user.role,
        id: user.id,
        email: user.email,
        hasTakenQuiz: user.hasTakenQuiz || false,
        data: user.data || null,
        isBackendAuth: user.isBackendAuth || false
      })
    } catch (err) {
      // Display detailed error if available
      let errorMessage = err.message || 'Invalid credentials. Please try again.'
      
      if (err.details && Array.isArray(err.details)) {
        errorMessage = 'Validation failed:\n' + err.details.map(d => `• ${d.field}: ${d.message}`).join('\n')
      }
      
      error.textContent = errorMessage
    }
  }

  document.getElementById('goToSignupBtn').onclick = (e) => {
    e.preventDefault()
    goToRegistration()
  }

  // Allow Enter key to submit
  document.getElementById('password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      document.getElementById('loginSubmit').click()
    }
  })
}