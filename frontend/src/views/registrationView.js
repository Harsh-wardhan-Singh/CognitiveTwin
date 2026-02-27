import { setUser } from '../testApp.js'
import { register } from '../services/auth.js'
import { goToLogin } from '../testApp.js'

export function renderRegistration() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="login-container">
      <h1>Cognitive Twin</h1>
      <h2>Create Account</h2>

      <div class="registration-form">
        <div class="form-group">
          <label for="regEmail">Email:</label>
          <input id="regEmail" type="email" placeholder="Enter your email" />
        </div>

        <div class="form-group">
          <label for="regPassword">Password:</label>
          <input id="regPassword" type="password" placeholder="Enter password" />
        </div>

        <div class="form-group">
          <label for="regConfirmPassword">Confirm Password:</label>
          <input id="regConfirmPassword" type="password" placeholder="Confirm password" />
        </div>

        <div class="form-group">
          <label for="regRole">I am a:</label>
          <select id="regRole">
            <option value="">-- Select Role --</option>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </div>

        <button id="registerSubmit" class="submit-btn">Create Account</button>
        <p id="registrationError" style="color:#ff6b6b; margin-top: 10px; white-space: pre-wrap;"></p>
        <p id="registrationSuccess" style="color:#51cf66; margin-top: 10px;"></p>

        <div class="auth-link">
          <p>Already have an account? <a href="#" id="goToLoginBtn">Sign In</a></p>
        </div>
      </div>
    </div>
  `

  document.getElementById('registerSubmit').onclick = async () => {
    const email = document.getElementById('regEmail').value.trim().toLowerCase()
    const password = document.getElementById('regPassword').value
    const confirmPassword = document.getElementById('regConfirmPassword').value
    const role = document.getElementById('regRole').value.trim().toLowerCase()
    const errorEl = document.getElementById('registrationError')
    const successEl = document.getElementById('registrationSuccess')

    errorEl.textContent = ''
    successEl.textContent = ''

    // Validation
    if (!email || !password || !confirmPassword || !role) {
      errorEl.textContent = 'Please fill in all fields'
      return
    }

    if (password !== confirmPassword) {
      errorEl.textContent = 'Passwords do not match'
      return
    }

    if (password.length < 6) {
      errorEl.textContent = 'Password must be at least 6 characters'
      return
    }

    // Strict email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      errorEl.textContent = 'Please enter a valid email address (e.g., user@example.com)'
      return
    }

    // Validate role is exactly student or teacher
    if (role !== 'student' && role !== 'teacher') {
      errorEl.textContent = 'Please select a valid role: Student or Teacher'
      return
    }

    try {
      const user = await register(email, password, role)
      successEl.textContent = 'Account created! Redirecting...'
      
      setTimeout(() => {
        setUser({
          role: user.role,
          id: user.id,
          email: user.email,
          hasTakenQuiz: false,
          data: null,
          isBackendAuth: true
        })
      }, 1000)
    } catch (err) {
      // Check if error has detailed validation info
      let errorMessage = err.message || 'Registration failed. Please try again.'
      
      // Parse backend error response if available
      if (err.details && Array.isArray(err.details)) {
        errorMessage = 'Validation failed:\n' + err.details.map(d => `• ${d.field}: ${d.message}`).join('\n')
      }
      
      errorEl.textContent = errorMessage
    }
  }

  document.getElementById('goToLoginBtn').onclick = (e) => {
    e.preventDefault()
    goToLogin()
  }

  // Allow Enter key to submit
  document.getElementById('regConfirmPassword').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      document.getElementById('registerSubmit').click()
    }
  })
}
