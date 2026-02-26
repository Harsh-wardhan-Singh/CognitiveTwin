import { renderTeacherDashboard } from '../teacher/teacherDashboard.js'
import { renderTeacherClassSelect } from './teacherClassSelectView.js'
import { mountView } from '../testApp.js'

export function renderTeacherClassView() {

  mountView((container) => {

    container.innerHTML = `
      <div class="teacher-container">
        <button id="backToClasses" class="glass-btn" style="margin-bottom:20px;">
          Back to Classrooms
        </button>

        <div id="teacherContent"></div>
      </div>
    `

    // Render dashboard inside teacherContent
    renderTeacherDashboard()

    const backBtn = container.querySelector('#backToClasses')

    if (backBtn) {
      backBtn.addEventListener('click', renderTeacherClassSelect)
    }

  })
}