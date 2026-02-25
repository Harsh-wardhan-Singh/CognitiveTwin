/* ============================= */
/* STUDENT STATE */
/* ============================= */

let studentState = {
  mastery: {
    Binomial: { value: 70, lastUpdated: Date.now() },
    Poisson: { value: 65, lastUpdated: Date.now() },
    Normal: { value: 72, lastUpdated: Date.now() },
    Bayes: { value: 60, lastUpdated: Date.now() },
    Conditional: { value: 75, lastUpdated: Date.now() }
  },
  risk: 40
}

/* ============================= */
/* CONCEPT DEPENDENCY GRAPH */
/* ============================= */

const conceptGraph = {
  Conditional: ["Bayes"],
  Bayes: [],
  Binomial: ["Normal"],
  Normal: [],
  Poisson: []
}

/* ============================= */
/* MOMENTUM TRACKING */
/* ============================= */

let masteryMomentum = {}

Object.keys(studentState.mastery).forEach(concept => {
  masteryMomentum[concept] = 0
})

/* ============================= */
/* STATE GETTERS / SETTERS */
/* ============================= */

export function getStudentState() {
  return studentState
}

export function updateStudentState(newState) {
  studentState = {
    ...studentState,
    ...newState
  }
}

/* ============================= */
/* COGNITIVE MASTERY ENGINE */
/* ============================= */

export function updateCognitiveMastery(concept, correct, signal) {
  const current = studentState.mastery[concept].value

  let delta

  if (correct) {
    delta = 10 * signal
    studentState.mastery[concept].value =
      Math.min(100, current + delta)
  } else {
    delta = -12 * signal
    studentState.mastery[concept].value =
      Math.max(10, current + delta)
  }

  studentState.mastery[concept].lastUpdated = Date.now()

  masteryMomentum[concept] = delta

  const relatedConcepts = conceptGraph[concept] || []

  relatedConcepts.forEach(related => {
    const relatedCurrent =
      studentState.mastery[related].value

    const propagatedChange = delta * 0.3

    studentState.mastery[related].value = Math.max(
      10,
      Math.min(100, relatedCurrent + propagatedChange)
    )

    studentState.mastery[related].lastUpdated = Date.now()
  })
}

/* ============================= */
/* ADVANCED RISK ENGINE */
/* ============================= */

export function calculateRisk() {
  const masteryValues =
    Object.values(studentState.mastery)
      .map(m => m.value)

  const weakest = Math.min(...masteryValues)

  const avg =
    masteryValues.reduce((a, b) => a + b, 0) /
    masteryValues.length

  const variance =
    masteryValues.reduce(
      (sum, val) => sum + Math.pow(val - avg, 2),
      0
    ) / masteryValues.length

  const volatility =
    Object.values(masteryMomentum)
      .filter(v => v < 0)
      .reduce((sum, v) => sum + Math.abs(v), 0)

  const riskScore =
    0.4 * (100 - weakest) +
    0.3 * variance +
    0.3 * volatility

  return Math.min(100, Math.max(5, riskScore))
}

/* ============================= */
/* RETENTION DECAY */
/* ============================= */

export function applyRetentionDecay() {
  const now = Date.now()

  Object.keys(studentState.mastery).forEach(concept => {
    const conceptData = studentState.mastery[concept]

    const hoursPassed =
      (now - conceptData.lastUpdated) / (1000 * 60 * 60)

    if (hoursPassed <= 0) return

    const decayRate = 0.5  // % per hour (tunable)

    const decayAmount = hoursPassed * decayRate

    conceptData.value =
      Math.max(10, conceptData.value - decayAmount)

    conceptData.lastUpdated = now
  })
}