import { calculateRisk } from '../services/state.js'

const baseConcepts = [
  "Binomial",
  "Poisson",
  "Normal",
  "Bayes",
  "Conditional"
]

function randomizeMastery(baseMastery) {
  const clone = {}

  Object.keys(baseMastery).forEach(concept => {
    const noise = (Math.random() - 0.5) * 30
    clone[concept] = Math.max(
      10,
      Math.min(100, baseMastery[concept] + noise)
    )
  })

  return clone
}

export function generateClassData(baseMastery, size = 20) {
  const classData = []

  for (let i = 0; i < size; i++) {
    const mastery = randomizeMastery(baseMastery)

    const risk = calculateRiskFromMastery(mastery)

    classData.push({
      id: `S${i + 1}`,
      mastery,
      risk
    })
  }

  return classData
}

function calculateRiskFromMastery(mastery) {
  const values = Object.values(mastery)

  const weakest = Math.min(...values)

  const avg =
    values.reduce((a, b) => a + b, 0) / values.length

  const variance =
    values.reduce(
      (sum, val) => sum + Math.pow(val - avg, 2),
      0
    ) / values.length

  const riskScore =
    0.5 * (100 - weakest) +
    0.5 * variance

  return Math.min(100, Math.max(5, riskScore))
}