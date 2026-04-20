import { render, screen, waitFor } from '@testing-library/react'
import React from 'react'
import App from './App'

vi.mock('./firestoreService', () => ({
  saveDatasetUpload: vi.fn(async () => {}),
  saveGeneratedReport: vi.fn(async () => {}),
  saveTrainingRun: vi.fn(async () => {}),
  upsertUserProfile: vi.fn(async () => {}),
}))

vi.mock('recharts', () => {
  const Stub = ({ children }) => <div>{children}</div>
  return {
    Bar: Stub,
    BarChart: Stub,
    CartesianGrid: Stub,
    Cell: Stub,
    ReferenceLine: Stub,
    Pie: Stub,
    PieChart: Stub,
    ResponsiveContainer: Stub,
    Tooltip: Stub,
    XAxis: Stub,
    YAxis: Stub,
  }
})

describe('App smoke', () => {
  beforeEach(() => {
    window.location.hash = ''
    localStorage.clear()
  })

  it('renders landing experience by default', async () => {
    render(<App />)

    expect(await screen.findByText('FairHire AI')).toBeInTheDocument()
    expect(
      await screen.findByText('Design the hiring process around fairness, evidence, and calm authority.'),
    ).toBeInTheDocument()
  })

  it('redirects protected route users to login when session is missing', async () => {
    window.location.hash = '#/dashboard'
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Corporate access')).toBeInTheDocument()
    })
  })
})
