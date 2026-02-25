/* ============================= */
/* CLASS DATA GENERATION */
/* ============================= */

function randomizeMastery(baseMastery) {
  const clone = {}

  Object.keys(baseMastery).forEach(concept => {
    const baseValue = baseMastery[concept].value

    const noise = (Math.random() - 0.5) * 30

    const newValue = Math.max(
      10,
      Math.min(100, baseValue + noise)
    )

    clone[concept] = {
      value: newValue,
      lastUpdated: Date.now()
    }
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

/* ============================= */
/* RISK FROM ARBITRARY MASTERY */
/* ============================= */

function calculateRiskFromMastery(mastery) {
  const values =
    Object.values(mastery).map(m => m.value)

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