import { renderTeacherDashboard } from '../teacher/teacherDashboard.js'
import { renderTeacherClassSelect } from './teacherClassSelectView.js'

export function renderTeacherClassView() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="teacher-container">
      <button id="backToClasses" class="glass-btn" style="margin-bottom:20px;">
        Back to Classrooms
      </button>

      <div id="teacherContent"></div>
    </div>
  `

  // Render dashboard inside container
  renderTeacherDashboard()

  const backBtn = document.getElementById('backToClasses')

  if (backBtn) {
    backBtn.addEventListener('click', renderTeacherClassSelect)
  }
}