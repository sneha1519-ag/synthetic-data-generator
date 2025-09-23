// App.jsx
import React, { useState } from 'react';
import { PlusCircle, Download, Sparkles } from 'lucide-react';

function App() {
  const [rowCount, setRowCount] = useState(100);
  const [selectedFields, setSelectedFields] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [realism, setRealism] = useState('realistic');
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedData, setGeneratedData] = useState(null);
  const [error, setError] = useState(null);
  const [generationMode, setGenerationMode] = useState('manual');

  // Backend API URL - change this to match your backend deployment
  const API_URL = 'http://localhost:8000';

  const availableFields = [
    { id: 'name', label: 'Full Name' },
    { id: 'email', label: 'Email Address' },
    { id: 'phone', label: 'Phone Number' },
    { id: 'address', label: 'Address' },
    { id: 'city', label: 'City' },
    { id: 'state', label: 'State/Province' },
    { id: 'zip', label: 'Zip/Postal Code' },
    { id: 'country', label: 'Country' },
    { id: 'company', label: 'Company Name' },
    { id: 'job_title', label: 'Job Title' },
    { id: 'age', label: 'Age' },
    { id: 'birthdate', label: 'Birth Date' },
    { id: 'salary', label: 'Salary' },
    { id: 'username', label: 'Username' },
    { id: 'password', label: 'Password' },
    { id: 'credit_card', label: 'Credit Card Number' },
    { id: 'timestamp', label: 'Timestamp' },
    { id: 'device_id', label: 'Device ID' },
    { id: 'reading', label: 'Sensor Reading' },
    { id: 'location', label: 'Location Coordinates' },
    { id: 'status', label: 'Status' },
  ];

  const templates = [
    {
      id: 'ecommerce',
      name: 'E-commerce Data',
      fields: ['name', 'email', 'address', 'city', 'state', 'zip', 'country', 'credit_card'],
      description: 'Customer and order data for online stores'
    },
    {
      id: 'healthcare',
      name: 'Healthcare Records',
      fields: ['name', 'birthdate', 'address', 'phone', 'city', 'state'],
      description: 'Patient data for healthcare applications'
    },
    {
      id: 'hr',
      name: 'HR Employee Data',
      fields: ['name', 'email', 'job_title', 'salary', 'address', 'phone', 'birthdate'],
      description: 'Employee records for HR departments'
    },
    {
      id: 'iot',
      name: 'IoT Sensor Logs',
      fields: ['timestamp', 'device_id', 'reading', 'location', 'status'],
      description: 'Sensor data for IoT applications'
    }
  ];

  const handleFieldToggle = (fieldId) => {
    if (selectedFields.includes(fieldId)) {
      setSelectedFields(selectedFields.filter(id => id !== fieldId));
    } else {
      setSelectedFields([...selectedFields, fieldId]);
    }
  };

  const selectTemplate = (template) => {
    setSelectedTemplate(template);
    setSelectedFields(template.fields);
  };

  const resetTemplate = () => {
    setSelectedTemplate(null);
    setSelectedFields([]);
  };

  const generateData = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const requestBody = {
        rowCount,
        realism,
        generationMode
      };

      // Add fields only in manual mode
      if (generationMode === 'manual') {
        requestBody.fields = selectedFields;
      }

      // Add prompt only in AI mode
      if (generationMode === 'ai' && prompt) {
        requestBody.prompt = prompt;
      }

      console.log("Sending request to backend:", requestBody);

      const response = await fetch(`${API_URL}/api/generate-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        let errorMessage = 'Failed to generate data';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          // If parsing JSON fails, use the default error message
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log("Received data from backend:", data);
      setGeneratedData(data);
    } catch (error) {
      console.error("Error generating data:", error);
      setError(error.message || 'An unexpected error occurred');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadCSV = () => {
    if (!generatedData || !generatedData.datasetId) {
      setError('No data available to download');
      return;
    }

    // Create a download link for the CSV file
    const downloadUrl = `${API_URL}/api/download/${generatedData.datasetId}`;

    // Create a temporary link element and trigger download
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `synthetic_data_${generatedData.datasetId}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-blue-600 text-white p-4 shadow-md">
          <div className="container mx-auto">
            <h1 className="text-2xl font-bold">Synthetic Data Generator</h1>
            <p className="text-blue-100">Create realistic synthetic data for your projects</p>
          </div>
        </header>

        <main className="container mx-auto p-4 md:p-8">
          {/* Add a templates section */}
          {generationMode === 'manual' && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">Quick Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {templates.map(template => (
                      <div
                          key={template.id}
                          className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                              selectedTemplate && selectedTemplate.id === template.id
                                  ? 'bg-blue-50 border-blue-500'
                                  : 'bg-white border-gray-200 hover:border-blue-300'
                          }`}
                          onClick={() => selectTemplate(template)}
                      >
                        <h3 className="font-medium">{template.name}</h3>
                        <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                        <p className="text-xs text-gray-400 mt-2">{template.fields.length} fields</p>
                      </div>
                  ))}
                </div>
                {selectedTemplate && (
                    <button
                        onClick={resetTemplate}
                        className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                    >
                      Clear template
                    </button>
                )}
              </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Configuration Panel */}
            <div className="lg:col-span-2 space-y-6">
              {/* Section: Generation Mode */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4">Generation Mode</h2>
                <div className="space-y-2">
                  <label className="flex items-center space-x-2">
                    <input
                        type="radio"
                        name="generationMode"
                        value="manual"
                        checked={generationMode === 'manual'}
                        onChange={() => setGenerationMode('manual')}
                        className="text-blue-600 focus:ring-blue-500"
                    />
                    <span>Manual Field Selection</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                        type="radio"
                        name="generationMode"
                        value="ai"
                        checked={generationMode === 'ai'}
                        onChange={() => setGenerationMode('ai')}
                        className="text-blue-600 focus:ring-blue-500"
                    />
                    <span>AI-Powered Generation</span>
                  </label>
                </div>
              </div>

              {/* Section: AI Prompt (only shown in AI mode) */}
              {generationMode === 'ai' && (
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-lg font-semibold mb-4">AI-Powered Data Generation</h2>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Describe the data you want to generate
                        </label>
                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="e.g., Generate a dataset for an online clothing store with customer information, order details, and shipping information"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                            rows={4}
                        />
                      </div>
                      <p className="text-sm text-gray-500">
                        The AI will automatically determine the appropriate fields and generate realistic data based on your description.
                      </p>
                    </div>
                  </div>
              )}

              {/* Section: Row Count */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4">Data Size</h2>
                <label className="block">
                  <span className="text-gray-700">Number of rows: {rowCount}</span>
                  <input
                      type="range"
                      min="10"
                      max="10000"
                      value={rowCount}
                      onChange={(e) => setRowCount(parseInt(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer mt-2"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>10</span>
                    <span>5,000</span>
                    <span>10,000</span>
                  </div>
                </label>
              </div>

              {/* Section: Field Selection (only shown in manual mode) */}
              {generationMode === 'manual' && (
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-lg font-semibold mb-4">Field Selection</h2>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {availableFields.map(field => (
                          <label key={field.id} className="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                checked={selectedFields.includes(field.id)}
                                onChange={() => handleFieldToggle(field.id)}
                                className="rounded text-blue-600 focus:ring-blue-500"
                            />
                            <span>{field.label}</span>
                          </label>
                      ))}
                    </div>
                    <div className="mt-4">
                      <button
                          onClick={() => setSelectedFields(availableFields.map(f => f.id))}
                          className="text-sm text-blue-600 hover:text-blue-800 mr-4"
                      >
                        Select All
                      </button>
                      <button
                          onClick={() => setSelectedFields([])}
                          className="text-sm text-blue-600 hover:text-blue-800"
                      >
                        Clear All
                      </button>
                    </div>
                  </div>
              )}

              {/* Section: Data Realism */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4">Data Realism Options</h2>
                <div className="space-y-2">
                  <label className="flex items-center space-x-2">
                    <input
                        type="radio"
                        name="realism"
                        value="realistic"
                        checked={realism === 'realistic'}
                        onChange={() => setRealism('realistic')}
                        className="text-blue-600 focus:ring-blue-500"
                    />
                    <span>Realistic (names, valid emails, location-based addresses)</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                        type="radio"
                        name="realism"
                        value="randomized"
                        checked={realism === 'randomized'}
                        onChange={() => setRealism('randomized')}
                        className="text-blue-600 focus:ring-blue-500"
                    />
                    <span>Randomized</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                        type="radio"
                        name="realism"
                        value="biased"
                        checked={realism === 'biased'}
                        onChange={() => setRealism('biased')}
                        className="text-blue-600 focus:ring-blue-500"
                    />
                    <span>Biased (to simulate edge cases)</span>
                  </label>
                </div>
              </div>

              {/* Data Preview Section - Show when data is generated */}
              {generatedData && (
                  <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-lg font-semibold mb-4">Data Preview</h2>
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                        <tr>
                          {generatedData.fields.map(field => (
                              <th
                                  key={field}
                                  scope="col"
                                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                              >
                                {field}
                              </th>
                          ))}
                        </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                        {generatedData.sampleData.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                              {generatedData.fields.map(field => (
                                  <td key={`${rowIndex}-${field}`} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {String(row[field])}
                                  </td>
                              ))}
                            </tr>
                        ))}
                        </tbody>
                      </table>
                    </div>
                    <p className="mt-4 text-sm text-gray-500">
                      Showing {Math.min(10, generatedData.sampleData.length)} of {generatedData.rowCount} rows
                    </p>
                  </div>
              )}
            </div>

            {/* Action Panel */}
            <div className="lg:col-span-1 space-y-6">
              <div className="bg-white p-6 rounded-lg shadow sticky top-4">
                <h2 className="text-lg font-semibold mb-4">Generation Summary</h2>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Row Count</h3>
                    <p className="text-lg">{rowCount.toLocaleString()} rows</p>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium text-gray-500">
                      {generationMode === 'manual' ? 'Selected Fields' : 'Generation Mode'}
                    </h3>
                    {generationMode === 'manual' ? (
                        selectedFields.length > 0 ? (
                            <p className="text-lg">{selectedFields.length} fields selected</p>
                        ) : (
                            <p className="text-orange-500">No fields selected</p>
                        )
                    ) : (
                        <p className="text-lg">AI-Powered</p>
                    )}
                  </div>

                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Data Realism</h3>
                    <p className="text-lg capitalize">{realism}</p>
                  </div>

                  {prompt && generationMode === 'ai' && (
                      <div>
                        <h3 className="text-sm font-medium text-gray-500">Using AI Prompt</h3>
                        <p className="text-sm text-gray-700 italic">"{prompt}"</p>
                      </div>
                  )}

                  {error && (
                      <div className="rounded-md bg-red-50 p-4 my-4">
                        <div className="flex">
                          <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <div className="ml-3">
                            <h3 className="text-sm font-medium text-red-800">Error</h3>
                            <div className="mt-2 text-sm text-red-700">
                              <p>{error}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                  )}

                  <button
                      onClick={generateData}
                      disabled={isGenerating || (generationMode === 'manual' && selectedFields.length === 0) || (generationMode === 'ai' && !prompt)}
                      className={`w-full py-3 px-6 flex items-center justify-center space-x-2 rounded-md text-white font-medium ${
                          (generationMode === 'manual' && selectedFields.length === 0) || (generationMode === 'ai' && !prompt)
                              ? 'bg-gray-400 cursor-not-allowed'
                              : 'bg-blue-600 hover:bg-blue-700'
                      }`}
                  >
                    {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <span>Generating...</span>
                        </>
                    ) : (
                        <>
                          <PlusCircle className="w-5 h-5" />
                          <span>Generate Data</span>
                        </>
                    )}
                  </button>

                  {generatedData && (
                      <button
                          onClick={downloadCSV}
                          className="w-full py-3 px-6 flex items-center justify-center space-x-2 rounded-md bg-green-600 hover:bg-green-700 text-white font-medium"
                      >
                        <Download className="w-5 h-5" />
                        <span>Download CSV</span>
                      </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>

        <footer className="bg-gray-100 border-t mt-12 py-6">
          <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
            <p>Synthetic Data Generator - Powered by Google GenAI</p>
          </div>
        </footer>
      </div>
  );
}

export default App;