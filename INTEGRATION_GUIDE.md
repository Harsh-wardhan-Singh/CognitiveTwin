# Cognitive Twin - Full Stack Integration Guide

## System Overview

This document describes the complete end-to-end integration of the Cognitive Twin system, connecting:
- **Frontend**: Static HTML/CSS/JS with real API calls
- **Backend API**: FastAPI with authentication and REST endpoints
- **AI Pipeline**: Multi-engine cognitive system with BKT, Risk Prediction, and Analytics
- **Database**: PostgreSQL with SQLAlchemy ORM

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/CSS/JS)                  │
│                    ↓ Real API Fetch Calls ↓                 │
├─────────────────────────────────────────────────────────────┤
│                    FASTAPI BACKEND (main.py)                │
│                                                              │
│  ┌─────────────┬─────────────┬──────────┬──────────────┐   │
│  │ Auth Routes │ Quiz Routes │ Student  │ Teacher      │   │
│  │ (login,     │ (submit,    │ Routes   │ Routes       │   │
│  │ register)   │ next-q,     │ (join,   │ (insights,   │   │
│  │             │ risk-score) │ dashboard)│ analytics)  │   │
│  └──────┬──────┴──────┬──────┴──────┬───┴──────────┬───┘   │
│         │             │             │              │        │
│         └─────────────┴─────────────┴──────────────┘        │
│                       ↓                                      │
│           SERVICE CONTAINER (Dependency Injection)          │
│                       ↓                                      │
├─────────────────────────────────────────────────────────────┤
│                    COGNITIVE PIPELINE                       │
│                                                              │
│  ┌──────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐    │
│  │ Mastery  │ │Retention│ │Confidence│ │ Dependency  │    │
│  │ Update   │ │ Decay   │ │ Model    │ │ Propagation │    │
│  │ (BKT)    │ │         │ │          │ │             │    │
│  └──────────┘ └─────────┘ └─────────┘ └──────────────┘    │
│                                                              │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ Feature  │ │ Risk    │ │Analytics │ │ Explanation │   │
│  │ Extractor│ │Predictor│ │ Insights │ │ Generator   │   │
│  │          │ │         │ │          │ │ (LLM)       │   │
│  └──────────┘ └─────────┘ └──────────┘ └──────────────┘   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    PERSISTENCE LAYER                        │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Mastery      │ │ Attempt      │ │ Mastery      │        │
│  │ Repository   │ │ Repository   │ │ History      │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                 DATABASE (PostgreSQL)                       │
│                                                              │
│  users | classrooms | questions | attempts | mastery       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Pipeline Execution Flow

When a student submits a quiz answer, the system executes:

```
1. VALIDATION
   └─ Check answer is correct
   └─ Validate confidence (1-10)
   └─ Validate response time

2. DECAY PHASE
   └─ Apply retention decay to all concepts (time-based)
   └─ Update mastery_dict with decayed values

3. MASTERY UPDATE (BKT)
   └─ Apply Bayesian Knowledge Tracing
   └─ Update mastery_value for submitted concept
   └─ Apply confidence weighting

4. CONFIDENCE RECALCULATION
   └─ Compute confidence metrics based on attempt history
   └─ Store in confidence_metrics

5. DEPENDENCY PROPAGATION
   └─ Update prerequisite concepts
   └─ Update dependent concepts
   └─ Propagate mastery changes through concept graph

6. FEATURE EXTRACTION
   └─ Extract 17-dimensional risk feature vector
   └─ Based on mastery, confidence, temporal patterns

7. RISK PREDICTION
   └─ Feed features to trained risk model
   └─ Get risk_probability (0-1)
   └─ Classify as "low", "medium", "high"

8. INSIGHTS GENERATION
   └─ Find weak topics (mastery < 0.4)
   └─ Calculate calibration gap
   └─ Compute volatility scores
   └─ Determine learning trends

9. PERSISTENCE
   └─ Store attempt in database
   └─ Upsert mastery values
   └─ Store mastery history

10. RESPONSE
    └─ Return is_correct + new mastery + risk to frontend
```

---

## API Endpoint Contract

### Authentication Endpoints

```
POST /auth/register
  Request: { email, password, role }
  Response: { message }

POST /auth/login
  Request: { email, password }
  Response: Sets access_token cookie

POST /auth/logout
  Response: Clears access_token cookie

GET /auth/me
  Response: { id, email, role }
```

### Quiz Endpoints

```
GET /quiz/next-question
  Auth: Required
  Response: { id, topic, concept, difficulty, question_text }

POST /quiz/submit
  Auth: Required
  Request: { question_id, user_answer, confidence, response_time }
  Response: { is_correct, mastery_update, risk_score, risk_level }

GET /quiz/risk-score
  Auth: Required
  Response: { user_id, risk_score, risk_label, risk_factors }

GET /quiz/explanation/{question_id}
  Auth: Required
  Response: { explanation, concept, mastery_level }
```

### Student Endpoints

```
GET /student/dashboard
  Auth: Required (Student)
  Response: { user_id, mastery, risk_score, insights, recent_attempts }

POST /student/join/{classroom_id}
  Auth: Required (Student)
  Response: { message }

GET /student/classrooms
  Auth: Required (Student)
  Response: [{ id, name, subject, teacher_id }]
```

### Teacher Endpoints

```
POST /teacher/classroom
  Auth: Required (Teacher)
  Request: { name, subject, syllabus_scope, exam_pattern, progress_topics }
  Response: Classroom object

GET /teacher/classroom/{classroom_id}/insights
  Auth: Required (Teacher)
  Response: { class_id, average_mastery, at_risk_count, weak_concepts, heatmap }

GET /teacher/student/{student_id}/dashboard
  Auth: Required (Teacher)
  Response: { user_id, mastery, risk_score, insights, recent_attempts }
```

---

## File Structure

```
backend/
├── requirements.txt (All dependencies)
├── .env (Database and secrets configuration)
├── app/
│   ├── main.py (FastAPI app with all routes, error handling, CORS)
│   │
│   ├── core/
│   │   ├── exceptions.py (Custom exception classes)
│   │   ├── dependencies.py (JWT auth, role checking)
│   │   ├── security.py (Token creation/verification)
│   │   ├── hashing.py (Password hashing)
│   │   ├── logging.py (Logging setup)
│   │   └── service_container.py (Dependency injection)
│   │
│   ├── db/
│   │   ├── base.py (SQLAlchemy declarative base)
│   │   ├── session.py (Database connection and session)
│   │   └── init_db.py (Database initialization script)
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── classroom.py
│   │   ├── question.py
│   │   ├── attempt.py
│   │   ├── mastery.py
│   │   ├── mastery_history.py
│   │   └── classroom_student.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── question_schema.py
│   │   ├── attempt_schema.py
│   │   ├── mastery_schema.py
│   │   ├── analytics_schema.py
│   │   └── classroom_schema.py
│   │
│   ├── api/
│   │   ├── auth_routes.py (Login, register, logout)
│   │   ├── quiz_routes.py (Submit answer, get question, risk score)
│   │   ├── student_routes.py (Dashboard, join classroom)
│   │   └── teacher_routes.py (Class insights, student monitoring)
│   │
│   ├── services/
│   │   ├── auth_services.py (Authentication logic)
│   │   │
│   │   ├── cognitive_engine/
│   │   │   ├── pipeline.py (Main orchestrator - executes all steps)
│   │   │   ├── mastery_update.py (BKT implementation)
│   │   │   ├── retention_decay.py (Temporal decay)
│   │   │   ├── confidence_model.py (Confidence calculation)
│   │   │   ├── dependency_propagation.py (Concept dependencies)
│   │   │   ├── concept_graph.py (Graph structure)
│   │   │   └── bkt_config.py (BKT parameters)
│   │   │
│   │   ├── risk_engine/
│   │   │   ├── feature_extractor.py (Extract ML features)
│   │   │   ├── predictor.py (Load and run model)
│   │   │   ├── feature_schema.py (Feature definitions)
│   │   │   └── models/risk_model.joblib (Trained model)
│   │   │
│   │   ├── analytics/
│   │   │   ├── insight_generator.py (Weak topics, trends, volatility)
│   │   │   ├── class_risk_aggregator.py (Class-level risk)
│   │   │   └── heatmap_builder.py (Performance heatmap)
│   │   │
│   │   ├── ai_generation/
│   │   │   ├── explanation_generator.py (LLM-based explanations)
│   │   │   ├── llm_client.py (LLM API calls)
│   │   │   └── schema_validator.py (JSON validation)
│   │   │
│   │   ├── quiz_engine/
│   │   │   ├── quiz_selector.py (Adaptive question selection)
│   │   │   ├── quiz_builder.py (Quiz construction)
│   │   │   ├── adaptive_logic.py (Difficulty adjustment)
│   │   │   └── quiz_session.py (Session tracking)
│   │   │
│   │   ├── core/
│   │   │   ├── submission_controller.py (Orchestrates submission flow)
│   │   │   ├── student_state.py (In-memory student state)
│   │   │   └── event_bus.py (Async event handling)
│   │   │
│   │   └── persistence/
│   │       ├── mastery_repository.py (Save mastery)
│   │       └── attempt_repository.py (Save attempts)
│   │
│   ├── scripts/
│   │   └── init_db.py (Initialize sample data)
│   │
│   └── tests/
│       ├── test_auth.py
│       ├── test_mastery.py
│       └── test_risk.py

frontend/
├── index.html
├── src/
│   ├── services/
│   │   └── api.js (Real API calls - NO MORE MOCKS)
│   ├── student/
│   │   ├── quiz.js
│   │   └── profile.js
│   ├── teacher/
│   │   ├── analytics.js
│   │   └── teacherDashboard.js
│   ├── views/
│   │   ├── loginView.js
│   │   ├── studentDashboardView.js
│   │   └── teacherClassView.js
│   └── styles/
│       └── global.css
```

---

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file)
DATABASE_URL=postgresql://user:password@localhost/cognitive_twin
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Initialize database with sample data
python -m app.scripts.init_db

# Start server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Verify it's connecting to the backend
# Update src/services/api.js if needed (API_BASE_URL)

# Open index.html in a browser or use a simple HTTP server
python -m http.server 3000
```

### 3. Test Endpoints

```bash
# Create a teacher
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"teacher@example.com","password":"password123","role":"teacher"}'

# Create a student
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password123","role":"student"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password123"}' \
  -c cookies.txt

# Get next question
curl -X GET http://localhost:8000/quiz/next-question \
  -b cookies.txt

# Submit answer and trigger pipeline
curl -X POST http://localhost:8000/quiz/submit \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"question_id":1,"user_answer":"n × p","confidence":8,"response_time":5000}'
```

---

## Key Features Delivered

✅ **Backend-Frontend Connection**
  - Real API calls replacing mock data
  - Proper error handling and validation
  - CORS enabled for cross-origin requests

✅ **Complete Pipeline Integration**
  - Quiz submission → Mastery update → Risk prediction
  - Proper execution order preserved
  - Exception handling at each stage

✅ **Dependency Injection**
  - ServiceContainer manages all engines
  - Easy to mock/test
  - No circular imports

✅ **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (student/teacher)
  - Cookie-based session management

✅ **Database Integration**
  - SQLAlchemy ORM
  - Proper relationships and foreign keys
  - Mastery history tracking
  - Attempt persistence

✅ **Error Handling**
  - Custom exception classes
  - Graceful error responses
  - Logging throughout system

✅ **Analytics & Insights**
  - Class-level insights
  - Student-level dashboards
  - Risk score calculation
  - Performance heatmaps

✅ **AI Integration**
  - LLM-based explanation generation
  - Adaptive content delivery
  - Feature-based risk modeling

---

## Critical Implementation Notes

### No Service Merging
Each engine operates independently:
- **BKT** handles mastery only
- **Risk Engine** handles prediction only
- **Analytics** handle insights only
- **LLM** handles content only

### Pipeline Order (NON-NEGOTIABLE)
1. Decay
2. BKT Update
3. Confidence
4. Propagation
5. Feature Extraction
6. Risk Prediction
7. Analytics
8. Persistence

### Student ID vs User ID
- Database uses `user_id` (consistent)
- Frontend uses `user.id`
- Pipeline receives user_id from auth

### Cold Start Handling
- New students initialized with mastery = 0.5
- Risk score defaults to 0 for new students
- Feature vector defaults to zeros

---

## Troubleshooting

**Issue**: "Circular import"
- Check that all imports use absolute paths (`from app.services...`)
- Avoid importing main.py inside services

**Issue**: "Risk model not found"
- Ensure `app/services/risk_engine/models/risk_model.joblib` exists
- Check RISK_MODEL_PATH in .env

**Issue**: "Database connection failed"
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Run `python -m app.scripts.init_db` to create tables

**Issue**: "LLM client initialization failed"
- System gracefully handles this (falls back to template explanations)
- Check LLM credentials if explanation endpoint returns errors

---

## Future Enhancements

- [ ] WebSocket support for real-time dashboard updates
- [ ] Adaptive quiz generation (not just selection)
- [ ] Advanced analytics with chart visualization
- [ ] Integration with learning management systems
- [ ] Mobile app frontend
- [ ] Advanced concept graph learning
- [ ] Teacher-customizable BKT parameters

---

## Deployment

The system is production-ready with:
- Error handling middleware
- CORS configuration
- Database connection pooling
- Logging throughout
- Health check endpoint
- Static file serving for frontend

To deploy:
1. Set environment variables in production
2. Use a production ASGI server (Gunicorn + Uvicorn)
3. Configure reverse proxy (Nginx/Apache)
4. Enable HTTPS
5. Set CORS origins appropriately

---

**Status**: ✅ FULLY INTEGRATED AND OPERATIONAL
