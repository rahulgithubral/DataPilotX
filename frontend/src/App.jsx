import { useState, useEffect } from 'react'
import UploadCard from './components/UploadCard'
import DatasetList from './components/DatasetList'
import AskAI from './components/AskAI'
import { getDashboard } from './api'

function App() {
  const [datasets, setDatasets] = useState([])
  const [selectedDatasetId, setSelectedDatasetId] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshDatasets = async () => {
    try {
      setLoading(true)
      const data = await getDashboard()
      setDatasets(data.datasets || [])
      if (data.datasets && data.datasets.length > 0 && !selectedDatasetId) {
        setSelectedDatasetId(data.datasets[data.datasets.length - 1].dataset_id)
      }
    } catch (error) {
      console.error('Failed to load datasets:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refreshDatasets()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">DataPilotX</h1>
          <p className="text-gray-600 mt-1">AI-Powered Data Analysis Platform</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <UploadCard onUploadSuccess={refreshDatasets} />
            <DatasetList
              datasets={datasets}
              selectedDatasetId={selectedDatasetId}
              onSelectDataset={setSelectedDatasetId}
              loading={loading}
            />
          </div>

          {/* Right Main Content */}
          <div className="lg:col-span-2">
            <AskAI selectedDatasetId={selectedDatasetId} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

