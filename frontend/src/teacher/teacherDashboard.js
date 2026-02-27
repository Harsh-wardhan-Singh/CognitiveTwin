import './teacher.css'
import { fetchClassInsights } from '../services/api.js'
import { currentUser } from '../testApp.js'

export async function renderTeacherDashboard(classroomId, forceRefresh = false) {
  const container = document.getElementById('dashboardContent')
  
  if (!classroomId) {
    container.innerHTML = `<p>Please select a classroom first.</p>`
    return
  }

  try {
    const classAnalytics = await fetchClassInsights(classroomId)
    
    container.innerHTML = `
      <div style="margin-bottom: 30px;">
        <h2 class="teacher-title">Class Cognitive Overview</h2>
        <button id="refreshBtn" class="glass-btn" style="margin-bottom:20px;">Refresh Data</button>
        <div class="class-summary" id="classSummary"></div>
        <div class="teacher-insights" id="teacherInsights"></div>
        <div id="heatmap" class="heatmap"></div>
      </div>
    `

    renderClassSummary(classAnalytics)
    renderInsights(classAnalytics)
    renderHeatmap(classAnalytics)
    
    document.getElementById('refreshBtn').addEventListener('click', () => {
      renderTeacherDashboard(classroomId, true)
    })
  } catch (error) {
    console.error("Failed to load class insights:", error)
    container.innerHTML = `
      <div style="margin-bottom: 30px;">
        <h2 class="teacher-title">Class Cognitive Overview</h2>
        <p>No data available yet. Students need to complete exams first.</p>
      </div>
    `
  }
}

function renderHeatmap(analytics) {
  const heatmap = document.getElementById('heatmap')
  
  if (!analytics.heatmap || Object.keys(analytics.heatmap).length === 0) {
    heatmap.innerHTML = '<p>No data available yet.</p>'
    return
  }

  const concepts = Object.keys(analytics.heatmap || {})

  let html = `
    <div class="heatmap-row header">
      <div class="heatmap-cell">Concept</div>
      <div class="heatmap-cell">Average Mastery</div>
    </div>
  `

  concepts.forEach(c => {
    const value = analytics.heatmap[c]
    html += `
      <div class="heatmap-row">
        <div class="heatmap-cell">${c}</div>
        <div class="heatmap-cell mastery" style="background-color: ${getColor(value)}">
          ${Math.round(value)}%
        </div>
      </div>
    `
  })

  heatmap.innerHTML = html
}

function renderInsights(analytics) {
  const container = document.getElementById('teacherInsights')

  const weakConcepts = analytics.weak_concepts || []
  const atRiskCount = analytics.at_risk_count || 0
  const totalStudents = analytics.total_students || 0

  container.innerHTML = `
    <div class="insight-card">
      <h3>Class Size</h3>
      <p>${totalStudents} students</p>
    </div>

    <div class="insight-card">
      <h3>At-Risk Students</h3>
      <p>${atRiskCount} / ${totalStudents}</p>
    </div>

    <div class="insight-card">
      <h3>Average Class Mastery</h3>
      <p>${Math.round(analytics.average_mastery || 0)}%</p>
    </div>

    <div class="insight-card">
      <h3>Weakest Concepts</h3>
      <p>${weakConcepts.slice(0, 3).join(', ') || 'N/A'}</p>
    </div>
  `
}

function renderClassSummary(analytics) {
  const summary = document.getElementById('classSummary')
  const heatmap = analytics.heatmap || {}
  const concepts = Object.keys(heatmap)

  const conceptHTML = concepts.map(
    (concept) => `<div>${concept}: ${Math.round(heatmap[concept])}%</div>`
  ).join('')

  summary.innerHTML = `
    <div class="insight-card">
      <h3>Class Average Risk</h3>
      <p>${Math.max(0, Math.round(100 - (analytics.average_mastery || 0)))}%</p>
    </div>

    <div class="insight-card">
      <h3>Students Assessed</h3>
      <p>${analytics.total_students || 0}</p>
    </div>

    <div class="insight-card">
      <h3>Concept Performance</h3>
      ${conceptHTML || '<p>No data</p>'}
    </div>
  `
}

function getColor(value) {
  // value is 0-100, scale to 0-255 range
  const red = Math.round(255 - (value * 2.55))
  const green = Math.round(value * 2.55)
  return `rgb(${red}, ${green}, 80)`
}