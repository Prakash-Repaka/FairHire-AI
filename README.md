# FairHire AI

Enterprise hiring intelligence platform for fairness auditing, explainability, and compliance-grade reporting.

[![Live Demo](https://img.shields.io/badge/Live-Firebase%20Hosting-FFCA28?logo=firebase&logoColor=black)](https://fairhire-67f38.web.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white)](https://vite.dev)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore%20%26%20Hosting-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-7B3FE4)](https://shap.readthedocs.io)

## Table of Contents

- [30-Second Judge Pitch](#30-second-judge-pitch)
- [Product Demo (GIF)](#product-demo-gif)
- [Why FairHire AI](#why-fairhire-ai)
- [Key Capabilities](#key-capabilities)
- [Tech Stack](#tech-stack)
- [Live Deployment](#live-deployment)
- [Product Walkthrough (Screenshots)](#product-walkthrough-screenshots)
- [Architecture](#architecture)
- [API Surface](#api-surface)
- [Local Setup](#local-setup)
- [Deployment (Firebase Hosting)](#deployment-firebase-hosting)
- [Demo Dataset](#demo-dataset)
- [License](#license)

## 30-Second Judge Pitch

**Problem:** Hiring models can look accurate while still producing unfair outcomes that are hard to explain to HR, legal, and leadership.

**Solution:** FairHire AI unifies model evaluation, bias auditing, explainability, what-if simulation, and compliance reporting into one guided enterprise workflow.

**Impact:** Teams move from raw dataset to a board-ready fairness narrative in minutes, with clear risk signals, mitigation paths, and accountable decision rationale.

## Product Demo (GIF)

![FairHire AI Demo Flow](screenshots/fairhire-demo.gif)

## Why FairHire AI

FairHire AI helps teams move from raw hiring data to decision-ready fairness evidence with a guided flow:

1. Upload hiring data.
2. Train and evaluate model performance.
3. Audit fairness across sensitive groups.
4. Explain candidate-level and global model behavior.
5. Export executive-ready reports.

## Key Capabilities

| Capability | What it does |
|---|---|
| Fairness Verdict Banner | Immediate risk signal with actionable remediation guidance |
| Guided Workflow Bar | Upload → Train → Audit → Rationale → Report progression across pages |
| What-if Simulator | Interactive threshold and reweight controls for fairness impact simulation |
| Bias Audit | Group-wise selection rates, demographic parity, and fairness index tracking |
| Decision Rationale | Feature-level influence and candidate-level explanation outputs |
| Executive Reports | Summary, risk areas, compliance status, and recommendations in one view |

## Tech Stack

| Layer | Stack |
|---|---|
| Frontend | React 19, Vite, Recharts, custom design system (single-page dashboard app) |
| Backend | FastAPI, Pydantic, scikit-learn, SHAP, NumPy/Pandas |
| Data & Auth | Firebase Firestore, Firebase Auth |
| Deployment | Firebase Hosting (frontend), local/uvicorn backend |
| Testing | Vitest + Testing Library (frontend), pytest + FastAPI TestClient (backend) |

## Live Deployment

- Web app: https://fairhire-67f38.web.app
  
## Product Walkthrough (Screenshots)

### Landing

![Landing](screenshots/8_landing_1776685849657.png)

### Login

![Login](screenshots/9_login_1776685862701.png)

### Dashboard

![Dashboard](screenshots/1_dashboard_1776685908800.png)

### Upload Dataset

![Upload Dataset](screenshots/2_upload_1776685934495.png)

### Model Evaluation

![Model Evaluation](screenshots/3_model_evaluation_1776685952834.png)

### Fairness Audit

![Fairness Audit](screenshots/4_fairness_audit_1776685970889.png)

### Decision Rationale

![Decision Rationale](screenshots/5_decision_insights_1776685987986.png)

### Reports

![Reports](screenshots/6_reports_1776686005196.png)

### Settings

![Settings](screenshots/7_settings_1776686021528.png)

## Architecture

```text
FairHire AI/
|- backend/
|  |- app/
|  |  |- main.py            # API routes and orchestration
|  |  |- ml_pipeline.py     # Training, fairness, explainability logic
|  |  |- schemas.py         # Request and response contracts
|  |  |- store.py           # Run and dataset state persistence helpers
|  |- data/
|  |  |- sample_dataset.csv # Demo data for end-to-end flow
|- frontend/
|  |- src/
|  |  |- App.jsx            # Main SPA shell and all pages
|  |  |- index.css          # Design system and theme tokens
|- firebase.json
|- .firebaserc
|- docker-compose.yml
|- requirements.txt
```

## API Surface

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Liveness check |
| GET | /runs | List run history |
| POST | /upload | Upload dataset for analysis |
| POST | /train | Train model with selected target column |
| GET | /bias | Compute fairness metrics for run and sensitive attribute |
| GET | /explain | Generate explainability outputs |
| GET | /report | Build consolidated audit report |
| POST | /simulate/whatif | Simulate threshold and reweighting changes |
| POST | /simulate/batch | Batch simulation grid |

Swagger docs are available at http://localhost:8000/docs when backend is running.

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm and pip

### Run Backend

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
cd backend
uvicorn main:app --reload --port 8000
```

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# backend
cd backend
pytest -q tests

# frontend
cd frontend
npm run test:run
```

## Deployment (Firebase Hosting)

```bash
cd frontend
npm run build

cd ..
npx firebase-tools deploy --only hosting --project fairhire-67f38
```

## Demo Dataset

Use the provided dataset at backend/data/sample_dataset.csv to run the full pipeline quickly.

## License

MIT
