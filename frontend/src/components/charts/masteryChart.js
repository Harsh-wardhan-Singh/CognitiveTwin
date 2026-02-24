import {
  Chart,
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

let masteryChartInstance = null

export function createMasteryChart(canvasId) {
  const ctx = document.getElementById(canvasId)

  masteryChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Binomial', 'Poisson', 'Normal', 'Bayes', 'Conditional'],
      datasets: [
        {
          label: 'Mastery Level',
          data: [80, 65, 72, 60, 75],
          backgroundColor: 'rgba(0,245,255,0.15)',
          borderColor: '#00F5FF',
          pointBackgroundColor: '#00F5FF',
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: 'rgba(255,255,255,0.7)'
          }
        }
      },
      scales: {
        r: {
          grid: { color: 'rgba(255,255,255,0.1)' },
          angleLines: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: {
            color: 'rgba(255,255,255,0.8)',
            font: { size: 13 }
          },
          ticks: { display: false }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  })
}

export function updateMasteryChart(newData) {
  if (!masteryChartInstance) return

  masteryChartInstance.data.datasets[0].data = newData
  masteryChartInstance.update()
}