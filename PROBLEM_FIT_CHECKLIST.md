# FairHire AI Problem-Statement Fit Checklist

## Proposed Problem Statement Fit
FairHire AI addresses the challenge of biased and opaque ML-driven hiring decisions by providing:
- bias detection across sensitive groups,
- explainable model decisions,
- measurable fairness metrics,
- and actionable reporting for compliance and governance.

## PRD Alignment Matrix

### 1) Product Objective
- Requirement: Audit hiring models for bias, explainability, fairness.
- Evidence in app: Upload -> Train -> Bias -> Explainability -> Reports flow.
- Status: Complete for MVP.

### 2) Problem Statement
- Requirement: Handle implicit bias, imbalance, hidden correlations; reduce unfair rejection and transparency risk.
- Evidence in app: Fairness metrics + explainability views + decision insights and reporting.
- Status: Complete for MVP demonstration.

### 3) Core Feature Coverage

#### Dataset Upload
- Requirement: Upload CSV, preview data, select target column.
- Evidence: Upload endpoint + UI preview + target suggestions/selection.
- Status: Complete.

#### Model Training
- Requirement: Baseline model training and metrics.
- Evidence: Train endpoint returns accuracy/precision/recall/F1 and confusion matrix.
- Status: Complete.

#### Bias Detection
- Requirement: Demographic parity and equal opportunity metrics across sensitive groups.
- Evidence: Bias endpoint computes demographic parity difference, equal opportunity difference, fairness index, and group rates.
- Status: Complete (parameterized by sensitive column).
- Demo note: Show gender, education, and experience by changing the sensitive column per run.

#### Explainability
- Requirement: Feature importance and candidate-level rationale.
- Evidence: Explain endpoint returns global feature importance + local contributions.
- Status: Complete.

#### Fairness Dashboard
- Requirement: Bias visualizations, group comparison, fairness index.
- Evidence: Dashboard and fairness sections render model + bias artifacts.
- Status: Complete.

#### Report Generation
- Requirement: Exportable report with metrics, bias findings, recommendations.
- Evidence: Report endpoint + PDF export route.
- Status: Complete (ensure PDF dependency present in deployed backend).

## TRD Alignment Matrix

### Architecture
- Requirement: Frontend + FastAPI backend + ML layer + database.
- Evidence: React frontend, FastAPI backend, scikit-learn/fairlearn/SHAP pipeline, Firestore integration.
- Status: Complete.

### API Set
- Requirement: /upload, /train, /bias, /explain, /report
- Status: Complete.

### ML Pipeline
- Requirement: preprocessing, training, fairness metrics, SHAP explainability.
- Status: Complete.

### Security and Validation
- Requirement: input validation, file limits, safe handling.
- Evidence: upload validation module (type/size/content checks).
- Status: Complete.

### Performance
- Requirement: async processing and cached/persisted results.
- Evidence: queued background jobs + persisted dataset/run/report data.
- Status: Complete.

### Deployment
- Requirement: deployable stack and optional Docker.
- Evidence: backend/frontend Dockerfiles + docker-compose + env template.
- Status: Complete.

## Open Innovation Positioning (for judging)
- This is not just a model trainer; it is a reusable fairness-audit framework.
- It can plug into multiple decision workflows beyond hiring (admissions, lending pre-screening, grant triage).
- It combines model performance + fairness + explainability + governance reporting in one workflow.

## Final Submission Acceptance Checklist
- [ ] Show end-to-end flow live: login -> upload -> train -> bias -> explain -> report.
- [ ] Demonstrate fairness metrics for at least 2 sensitive columns.
- [ ] Show one local explanation for a candidate-level decision.
- [ ] Export one report (PDF) during demo.
- [ ] Show persisted records in Firestore collections (users, datasets, training_runs, reports).
- [ ] Explain one mitigation action derived from the findings.

## Suggested 2-Minute Demo Order
1. Problem in one line: hiring AI can be biased and opaque.
2. Upload and train quickly.
3. Show fairness metrics and group gaps.
4. Show why a candidate decision happened (local explanation).
5. Export report and show Firestore persistence.
6. Close with governance impact: fairer hiring and audit readiness.
