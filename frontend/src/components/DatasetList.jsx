function DatasetList({ datasets, selectedDatasetId, onSelectDataset, loading }) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Datasets</h2>
        <div className="flex items-center justify-center py-8">
          <svg className="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
    )
  }

  if (datasets.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Datasets</h2>
        <p className="text-sm text-gray-500">No datasets uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Datasets</h2>
      <div className="space-y-2">
        {datasets.map((dataset) => (
          <button
            key={dataset.dataset_id}
            onClick={() => onSelectDataset(dataset.dataset_id)}
            className={`w-full text-left p-4 rounded-lg border transition-all ${
              selectedDatasetId === dataset.dataset_id
                ? 'bg-blue-50 border-blue-300 shadow-sm'
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            }`}
          >
            <div className="font-medium text-gray-900">{dataset.name}</div>
            <div className="text-sm text-gray-600 mt-1">
              {dataset.rows.toLocaleString()} rows × {dataset.columns} columns
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default DatasetList

