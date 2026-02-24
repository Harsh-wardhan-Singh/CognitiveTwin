let circleElement = null
let percentageLabel = null
let circumferenceValue = 0
let numberAnimation = null

export function createRiskRing(containerId, percentage = 0) {
  const container = document.getElementById(containerId)
  if (!container) return

  const radius = 60
  circumferenceValue = 2 * Math.PI * radius

  container.innerHTML = `
    <div class="risk-ring-wrapper">
      <svg width="150" height="150">
        <circle
          cx="75"
          cy="75"
          r="${radius}"
          stroke="rgba(255,255,255,0.08)"
          stroke-width="10"
          fill="transparent"
        />
        <circle
          id="risk-progress"
          cx="75"
          cy="75"
          r="${radius}"
          stroke="#00F5FF"
          stroke-width="10"
          fill="transparent"
          stroke-dasharray="${circumferenceValue}"
          stroke-dashoffset="${circumferenceValue}"
          stroke-linecap="round"
        />
      </svg>
      <div class="risk-percentage">0%</div>
    </div>
  `

  circleElement = container.querySelector('#risk-progress')
  percentageLabel = container.querySelector('.risk-percentage')

  if (!circleElement || !percentageLabel) return

  circleElement.style.transition = "stroke-dashoffset 1s cubic-bezier(.4,0,.2,1)"
  circleElement.style.filter = "drop-shadow(0 0 8px rgba(0,245,255,0.6))"

  updateRiskRing(percentage)
}

export function updateRiskRing(percentage) {
  if (!circleElement || !percentageLabel) return

  const safePercentage = Math.max(0, Math.min(100, percentage))
  const offset = circumferenceValue - (safePercentage / 100) * circumferenceValue

  circleElement.style.strokeDashoffset = offset

  animateNumber(safePercentage)
}

function animateNumber(target) {
  if (numberAnimation) {
    cancelAnimationFrame(numberAnimation)
  }

  let current = parseInt(percentageLabel.textContent.replace('%', '')) || 0
  const start = current
  const duration = 600
  const startTime = performance.now()

  function update(time) {
    const progress = Math.min((time - startTime) / duration, 1)
    const value = Math.round(start + (target - start) * progress)

    percentageLabel.textContent = `${value}%`

    if (progress < 1) {
      numberAnimation = requestAnimationFrame(update)
    }
  }

  numberAnimation = requestAnimationFrame(update)
}