import { renderLogin } from './views/loginView.js'
import { renderStudentHome } from './views/studentHomeView.js'
import { renderTeacherClassSelect } from './views/teacherClassSelectView.js'

export let currentUser = null

export function setUser(user) {
  currentUser = user

  if (user.role === 'student') {
    renderStudentHome()
  }

if (user.role === 'teacher') {
  renderTeacherClassSelect()
}
}

export function logout() {
  currentUser = null
  renderLogin()
}

renderLogin()