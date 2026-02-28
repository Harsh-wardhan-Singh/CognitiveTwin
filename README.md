# 🧠 CognitiveTwin – AI-Powered Adaptive Learning & Risk Intelligence Platform

---

## 📌 Overview

**CognitiveTwin** is a comprehensive full-stack AI-driven educational platform designed to **assess student knowledge mastery, predict learning risks, and provide personalized cognitive insights** in real-time.

The system operates across **three powerful integrated modes**:

- **🎓 Adaptive Quiz Mode** – Intelligent question delivery based on student ability
- **📊 Mastery Analysis Engine** – ML-powered learning progress tracking
- **⚠️ Risk Detection System** – Predictive alerts for at-risk students

This project demonstrates a complete **end-to-end intelligent learning analytics pipeline**:

📌 Student Assessment → Knowledge Modeling → Risk Prediction → Teacher Analytics → Intervention Recommendations

It combines:

- **Machine Learning** (Scikit-Learn for mastery prediction)
- **Real-time Knowledge State Tracking**
- **Adaptive Difficulty Adjustment**
- **Risk Scoring & Classification**
- **FastAPI Backend** (High-performance async APIs)
- **Interactive Dashboard** (Vue.js/JavaScript frontend)
- **PostgreSQL Database** (Reliable data persistence)
- **Cloud-Ready Architecture** (Docker & deployment configs included)

---

## 🎯 Motivation

Modern education faces critical challenges:

- **Knowledge Gaps** – Students don't know what they don't know
- **Undetected Struggles** – At-risk students identified too late
- **One-Size-Fits-All** – Static curricula don't adapt to individual needs
- **Lack of Predictive Insights** – Teachers need early warning systems
- **Inefficient Assessment** – Paper tests don't capture learning progress

CognitiveTwin was built to:

- **Quantify** student knowledge mastery in real-time
- **Predict** which students are at-risk before they fail
- **Personalize** learning paths based on cognitive state
- **Enable** teachers to intervene with data-backed insights
- **Demonstrate** production-grade AI/ML in education

---

## 🏗️ Architecture

```
                   ┌─────────────────────┐
                   │   Student/Teacher   │
                   │   Web Dashboard     │
                   └──────────▲──────────┘
                              │
                       JSON REST API
                              │
              ┌───────────────▼────────────────┐
              │      FastAPI Backend           │
              │    (Async Python Service)      │
              └───────┬──────────┬──────────┬──┘
                      │          │          │
         ┌────────────▼──┐  ┌───▼────────┐  ┌─────────────┐
         │   Auth        │  │  Quiz      │  │  Analytics  │
         │   Engine      │  │  Engine    │  │  Service    │
         └───────────────┘  └───────┬────┘  └─────────────┘
                                    │
                    ┌───────────────┴────────────┐
                    │                            │
          ┌─────────▼──────────┐      ┌────────▼───────┐
          │  Cognitive Engine  │      │  Risk Engine    │
          │  - Mastery Scoring │      │  - Risk Scoring │
          │  - ML Prediction   │      │  - At-Risk Alerts
          │  - Proficiency Gap │      │  - Intervention │
          └────────────────────┘      └─────────────────┘
                    │                            │
                    └───────────────┬────────────┘
                                    ▼
                      ┌──────────────────────┐
                      │   PostgreSQL DB      │
                      │  (Persistent Store)  │
                      └──────────────────────┘
```

---

## ⚙️ Core System Modes

### 🎓 Mode 1 – Adaptive Quiz Engine

Students take quizzes that intelligently adapt based on performance.

**Features:**
- Dynamic difficulty scaling
- Progress tracking per quiz
- Real-time confidence scoring
- Mastery-based question selection
- Instant answer feedback

**Pipeline:**
1. Student attempts question
2. Cognitive engine evaluates response
3. Mastery score updated
4. Next question difficulty adjusted
5. Risk flags triggered if needed

---

### 📊 Mode 2 – Mastery Analysis Engine

Real-time knowledge state modeling using ML.

**What It Tracks:**
- Overall mastery percentage
- Per-topic mastery scores
- Proficiency gaps
- Learning velocity
- Confidence levels

**How It Works:**
1. Collects student answer patterns
2. Trains ML model on historical data
3. Predicts current mastery level
4. Identifies knowledge gaps
5. Recommends focus areas

**Output Metrics:**
- Current Mastery %
- Predicted Next Performance
- Gap Analysis
- Learning Trajectory
- Intervention Priority Score

---

### ⚠️ Mode 3 – Risk Detection System

Predictive alerts for students at risk of falling behind.

**Risk Factors Monitored:**
- Low mastery with high assessment frequency
- Declining performance trend
- High gap between baseline and current mastery
- Failed attempts on critical concepts
- Low engagement metrics

**Alert Levels:**
- 🟢 **Low Risk** – On track, no intervention needed
- 🟡 **Medium Risk** – Monitor closely, consider support
- 🔴 **High Risk** – Intervention recommended
- 🔥 **Critical Risk** – Immediate action required

---

## 👥 User Roles & Features

### 🎓 Student Dashboard
- Take adaptive quizzes
- View personal mastery metrics
- Track learning progress
- Receive personalized insights
- See knowledge gaps
- Monitor risk scores

### 👨‍🏫 Teacher Analytics Portal
- Class-level performance overview
- Individual student monitoring
- Risk alerts & intervention recommendations
- Progress analytics & trends
- Detailed student profiles
- Export analytics reports

---

## 🗂️ Full Code Structure

```
CognitiveTwin/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── api/                     # Route handlers
│   │   │   ├── auth_routes.py       # Authentication endpoints
│   │   │   ├── quiz_routes.py       # Quiz delivery & submission
│   │   │   ├── student_routes.py    # Student profile & progress
│   │   │   └── teacher_routes.py    # Teacher analytics
│   │   ├── models/                  # SQLAlchemy DB models
│   │   │   ├── user.py              # User (Student/Teacher)
│   │   │   ├── question.py          # Quiz questions
│   │   │   ├── quiz.py              # Quiz definitions
│   │   │   ├── attempt.py           # Student attempts
│   │   │   ├── mastery.py           # Mastery scores
│   │   │   ├── risk_history.py      # Risk tracking
│   │   │   ├── classroom.py         # Classroom grouping
│   │   │   └── exam.py              # Exam management
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic
│   │   │   ├── auth_services.py     # Auth logic
│   │   │   ├── ai_generation/       # AI-powered content generation
│   │   │   ├── cognitive_engine/    # Mastery & learning models
│   │   │   ├── quiz_engine/         # Quiz delivery logic
│   │   │   ├── risk_engine/         # Risk scoring & alerts
│   │   │   ├── analytics/           # Data analytics
│   │   │   └── persistence/         # Data access layer
│   │   ├── core/                    # Core utilities
│   │   │   ├── security.py          # JWT & hashing
│   │   │   ├── logging.py           # Structured logging
│   │   │   ├── exceptions.py        # Custom exceptions
│   │   │   └── dependencies.py      # Dependency injection
│   │   ├── db/                      # Database layer
│   │   │   ├── session.py           # SQLAlchemy session
│   │   │   ├── base.py              # Base model configs
│   │   │   └── init_db.py           # DB initialization
│   │   └── utils/                   # Utility functions
│   │       ├── math_utils.py        # Math/scoring functions
│   │       └── validators.py        # Input validation
│   ├── requirements.txt             # Python dependencies
│   ├── run_seed.py                  # Database seeding script
│   └── test_*.py                    # Test files
│
├── frontend/                        # Vue.js/Vite Frontend
│   ├── src/
│   │   ├── main.js                 # Entry point
│   │   ├── components/             # Reusable UI components
│   │   ├── views/                  # Page views
│   │   │   ├── student/            # Student pages
│   │   │   └── teacher/            # Teacher pages
│   │   ├── services/               # API integration
│   │   │   └── api.js              # REST client
│   │   ├── styles/                 # CSS & styling
│   │   └── utils/                  # Frontend utilities
│   ├── index.html                  # HTML entry point
│   ├── package.json                # Node dependencies (Chart.js, Vite)
│   └── vite.config.js              # Vite build config
│
├── deployment/                     # Containerization & deployment
│   ├── Dockerfile                  # Docker image definition
│   ├── docker-compose.yml          # Local multi-container setup
│   └── render.yaml                 # Render.com deployment config
│
├── docs/                           # Documentation
│   └── technical_notes.md
│
└── README.md                       # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for frontend/Vite)
- **PostgreSQL 12+** (or use Docker)
- **Git**

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/cognitivetwin.git
cd cognitivetwin
```

### Step 2: Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/cognitive_twin

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Optional: AI API Keys (for content generation)
# HUGGINGFACE_API_KEY=your_hf_key_here
```

#### Initialize Database

```bash
python -m app.scripts.init_db
```

You should see:
```
✅ Database initialized successfully!
   - Created tables
   - Initialized sample data
```

### Step 3: Frontend Setup

```bash
cd ../frontend
npm install
```

### Step 4: Start the Application

#### Terminal 1: Start Backend

```bash
cd backend
# Make sure venv is activated
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
🚀 Cognitive Twin Backend starting up...
✅ Database initialized
✅ All routes registered
```

#### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:5173` (Vite default)

### Step 5: Access the Application

Open your browser to:

```
http://localhost:5173
```

**Test Credentials:**
- **Student Email:** student1@example.com
- **Student Password:** password123
- **Teacher Email:** teacher@example.com
- **Teacher Password:** password123

---

## 🧪 Testing the System

### Option A: Using the Web Interface

1. Login as **Student**
2. Navigate to **Quiz** section
3. Take a quiz and submit answers
4. View your **Mastery Dashboard**
5. Check your **Risk Score** (if applicable)
6. Switch to **Teacher** login to see analytics

### Option B: Using API (cURL/Postman)

#### Register New User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "role": "student"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123"
  }'
```

#### Get Student Progress
```bash
curl -X GET http://localhost:8000/students/progress \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🐳 Docker Setup (Alternative)

### Using Docker Compose

Build and run everything at once:

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

This will:
- Start PostgreSQL container
- Build backend service
- Start uvicorn server
- Make API available at `http://localhost:8000`

### Manual Docker Build

```bash
docker build -f deployment/Dockerfile -t cognitivetwin:latest .
docker run -p 8000:8000 cognitivetwin:latest
```

---

## 🚀 Deployment Setup

### Option 1: Deploy to Render.com (Recommended)

**Note:** This project is not yet deployed. Follow these steps to deploy:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Service**
   - Visit [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use existing `deployment/render.yaml`

3. **Configure Environment Variables**
   - Add `DATABASE_URL` (use Render's PostgreSQL)
   - Add `SECRET_KEY` (use a strong random key)
   - Configure other variables as needed

4. **Deploy** – Render automatically deploys on push

### Option 2: Deploy to Heroku

```bash
heroku create cognitivetwin
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

### Option 3: Self-hosted (AWS/GCP/Azure)

Use the provided `Dockerfile` to containerize and deploy to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Any Kubernetes cluster

---

## 📊 Example Workflow

### Student Scenario

1. **Student logs in** → Views dashboard
2. **Takes quiz** → System presents adaptive questions
3. **Submits answers** → Cognitive engine processes
4. **Mastery updated** → Progress visualization refreshed
5. **Risk scored** → Alerts if needed
6. **Insights generated** → Recommendations shown

### Teacher Scenario

1. **Teacher logs in** → Views class analytics
2. **Checks risk alerts** → Identifies 3 at-risk students
3. **Reviews mastery trends** → Sees common knowledge gaps
4. **Intervenes** → Assigns targeted remedial questions
5. **Monitors progress** → Re-evaluates after intervention

---

## 🔑 Key Endpoints

### Authentication
- `POST /auth/register` – Create new account
- `POST /auth/login` – Login & get JWT token
- `POST /auth/logout` – Logout
- `GET /auth/me` – Get current user

### Student Quizzes
- `GET /quizzes` – List available quizzes
- `GET /quizzes/{quiz_id}` – Get quiz questions
- `POST /attempts/{quiz_id}` – Submit answers
- `GET /students/progress` – Get mastery dashboard

### Teacher Analytics
- `GET /teacher/class/{classroom_id}` – Class overview
- `GET /teacher/students/{student_id}` – Student details
- `GET /teacher/analytics` – Advanced analytics
- `GET /teacher/risk-alerts` – At-risk students

---

## 🔧 Configuration

### Database Tuning
Edit `backend/app/db/session.py` for connection pooling options.

### ML Model Parameters
Adjust cognitive engine thresholds in `backend/app/services/cognitive_engine/`.

### Risk Scoring Rules
Customize risk calculation in `backend/app/services/risk_engine/`.

---

## 🧠 ML & Cognitive Engine

The platform uses **Scikit-Learn** for mastery prediction:

- **Algorithm:** Gradient Boosting Classifier / Linear Regression
- **Features:** Attempt history, time spent, confidence, topic patterns
- **Training:** Runs on historical student data
- **Inference:** Real-time prediction after each quiz attempt

Model files stored in `backend/app/services/cognitive_engine/models/`.

---

## 📈 Monitoring & Logging

All requests are logged with:
- Timestamp
- User ID
- Route accessed
- Response time
- Error details

Logs available in console and `logs/` directory (when configured).

---

## 🐛 Troubleshooting

### Issue: Database Connection Error
**Solution:** Ensure PostgreSQL is running and `DATABASE_URL` is correct in `.env`.

### Issue: CORS Errors
**Solution:** Check `backend/app/main.py` CORS configuration for correct frontend URL.

### Issue: JWT Token Expired
**Solution:** Login again to get a new token. Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` if needed.

### Issue: Frontend not connecting to backend
**Solution:** Ensure backend is running on `http://localhost:8000` and check browser console for network errors.

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org)
- [PostgreSQL Best Practices](https://wiki.postgresql.org)
- [Vue.js & Vite](https://vitejs.dev)
- [Scikit-Learn ML](https://scikit-learn.org)

---

## 🔮 Future Improvements

- [ ] Real-time AI content generation (GPT integration)
- [ ] Mobile app (React Native)
- [ ] Advanced NLP for open-ended question evaluation
- [ ] Gamification & badges system
- [ ] Parent/Guardian portal
- [ ] Integration with LMS platforms (Canvas, Blackboard)
- [ ] Real-time collaboration features
- [ ] Deep Learning models (Neural Networks)
- [ ] Multi-language support
- [ ] Accessibility improvements (WCAG 2.1)

---

## 📬 Contact & Support

**Created by:** Harsh Wardhan Singh, Shikhar Sadhu, and Sn Omm Tripathi

**For Questions, Bugs, or Collaborations:**
- Open an issue on GitHub
- Email: your_email@example.com
- Discord: [Join our community](discord_link)

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) file for details.

---

## ⭐ Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌍 Current Status

🚀 **Local Development:** Fully functional
📦 **Deployment:** Ready for cloud deployment (not yet hosted)
🔧 **Maintenance:** Actively developed
📚 **Documentation:** Comprehensive

**Next Steps:** Deploy to Render.com or preferred hosting platform.

---

**Happy Learning! 🎓**

⭐ If you found this project interesting, consider starring the repository!
