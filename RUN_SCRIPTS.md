# Run Scripts

## 1) Activate Python venv (PowerShell)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& "d:\FairHire AI\.venv\Scripts\Activate.ps1"
```

## 2) Run Backend (FastAPI)
```powershell
Set-Location "d:\FairHire AI\backend"
python -m uvicorn app.main:app --port 8000 --reload
```

Note: `app.main` requires ML dependencies (`pandas`, `scikit-learn`, `shap`, etc.).

If you are missing ML dependencies (for example pandas), run the lightweight runtime server:
```powershell
Set-Location "d:\FairHire AI\backend"
python -m uvicorn app.server:app --port 8000 --reload
```

If `python` is not on PATH, use:
```powershell
Set-Location "d:\FairHire AI\backend"
& "d:\FairHire AI\.venv\Scripts\python.exe" -m uvicorn app.server:app --port 8000 --reload
```

## 2.1) Troubleshooting: pandas install fails on Python 3.14
- Cause: `pandas==2.3.1` does not currently provide a prebuilt wheel for Python 3.14, so pip attempts a source build and fails without Visual Studio build tools.
- Fast workaround: use `app.server` (lightweight runtime) as shown above.
- Full ML workaround: create a Python 3.11 or 3.12 virtual environment and reinstall requirements, then run `app.main`.

## 3) Run Frontend (Vite)
```powershell
Set-Location "d:\FairHire AI\frontend"
npm install
npm run dev
```

## 4) Build Frontend
```powershell
Set-Location "d:\FairHire AI\frontend"
npm run build
```

## 5) Run Backend + Frontend (two terminals)
Terminal A:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& "d:\FairHire AI\.venv\Scripts\Activate.ps1"
Set-Location "d:\FairHire AI\backend"
python -m uvicorn app.main:app --port 8000 --reload
```

Terminal B:
```powershell
Set-Location "d:\FairHire AI\frontend"
npm run dev
```
