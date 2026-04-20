import { doc, setDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase'

function scrubUndefined(value) {
  if (Array.isArray(value)) {
    return value.map(scrubUndefined)
  }

  if (value && typeof value === 'object') {
    const output = {}
    for (const [key, nested] of Object.entries(value)) {
      if (nested !== undefined) {
        output[key] = scrubUndefined(nested)
      }
    }
    return output
  }

  return value
}

function userDocId(email) {
  return (email || 'unknown').toLowerCase().replace(/[^a-z0-9_-]/g, '_')
}

export async function upsertUserProfile(user) {
  if (!user?.email) return

  const userRef = doc(db, 'users', userDocId(user.email))
  await setDoc(
    userRef,
    scrubUndefined({
      userId: user.user_id || null,
      employeeId: user.employee_id || null,
      email: user.email,
      name: user.name || 'FairHire User',
      role: user.role || 'analyst',
      lastLoginAt: serverTimestamp(),
    }),
    { merge: true },
  )
}

export async function saveDatasetUpload({ user, upload, selectedTarget }) {
  if (!upload?.dataset_id) return

  const datasetRef = doc(db, 'datasets', upload.dataset_id)
  await setDoc(
    datasetRef,
    scrubUndefined({
      datasetId: upload.dataset_id,
      filename: upload.filename || null,
      rows: upload.rows || 0,
      columns: upload.columns || [],
      targetSuggestions: upload.target_suggestions || [],
      selectedTarget: selectedTarget || null,
      uploadedBy: user?.email || null,
      uploadedAt: serverTimestamp(),
    }),
    { merge: true },
  )
}

export async function saveTrainingRun({ user, training }) {
  if (!training?.run_id) return

  const runRef = doc(db, 'training_runs', training.run_id)
  await setDoc(
    runRef,
    scrubUndefined({
      runId: training.run_id,
      datasetId: training.dataset_id || null,
      modelType: training.model_type || null,
      targetColumn: training.target_column || null,
      metrics: {
        accuracy: training.accuracy ?? null,
        precision: training.precision ?? null,
        recall: training.recall ?? null,
        f1Score: training.f1_score ?? null,
        confusionMatrix: training.confusion_matrix || null,
      },
      predictionPreview: training.prediction_preview || [],
      trainedBy: user?.email || null,
      trainedAt: serverTimestamp(),
    }),
    { merge: true },
  )
}

export async function saveGeneratedReport({ user, report }) {
  if (!report?.run_id) return

  const reportRef = doc(db, 'reports', report.run_id)
  await setDoc(
    reportRef,
    scrubUndefined({
      runId: report.run_id,
      generatedBy: user?.email || null,
      generatedAt: serverTimestamp(),
      report,
    }),
    { merge: true },
  )
}
