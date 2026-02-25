import { setUser } from '../testApp.js'
import { getStudentState } from '../services/state.js'

export function renderLogin() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="login-container">
      <h1>Cognitive Twin</h1>

      <div class="role-buttons">
        <button id="studentBtn">Sign in as Student</button>
        <button id="teacherBtn">Sign in as Teacher</button>
      </div>

      <div id="authForm" style="display:none;">
        <input id="email" placeholder="Email" />
        <input id="password" type="password" placeholder="Password" />
        <button id="loginSubmit">Login</button>
        <p id="loginError" style="color:red;"></p>
      </div>
    </div>
  `

  let selectedRole = null

  document.getElementById('studentBtn').onclick = () => {
    selectedRole = 'student'
    document.getElementById('authForm').style.display = 'block'
  }

  document.getElementById('teacherBtn').onclick = () => {
    selectedRole = 'teacher'
    document.getElementById('authForm').style.display = 'block'
  }

  document.getElementById('loginSubmit').onclick = () => {
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    const error = document.getElementById('loginError')

    if (selectedRole === 'student') {
      if (email === 'student@test.com' && password === '1234') {
        setUser({
          role: 'student',
          id: 'S1',
          hasTakenQuiz: false,
          data: null
        })
      } else {
        error.textContent = 'Invalid student credentials.'
      }
    }

    if (selectedRole === 'teacher') {
      if (email === 'teacher@test.com' && password === 'admin') {
        setUser({
          role: 'teacher',
          id: 'T1'
        })
      } else {
        error.textContent = 'Invalid teacher credentials.'
      }
    }
  }
}