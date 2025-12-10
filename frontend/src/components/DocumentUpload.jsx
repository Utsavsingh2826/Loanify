import React, { useState } from 'react'
import { Upload, File, CheckCircle, XCircle, Loader2 } from 'lucide-react'
import { documentsAPI } from '../services/api'

const DOCUMENT_TYPES = [
  { value: 'pan_card', label: 'PAN Card' },
  { value: 'aadhaar_card', label: 'Aadhaar Card' },
  { value: 'bank_statement', label: 'Bank Statement' },
  { value: 'income_proof', label: 'Income Proof (Salary Slip/ITR)' },
  { value: 'address_proof', label: 'Address Proof' },
  { value: 'photo', label: 'Photograph' },
]

export default function DocumentUpload({ userId, applicationId, onUploadSuccess }) {
  const [selectedType, setSelectedType] = useState('')
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Check file size (10MB limit)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setUploadStatus({
          type: 'error',
          message: 'File size must be less than 10MB',
        })
        return
      }
      setFile(selectedFile)
      setUploadStatus(null)
    }
  }

  const handleUpload = async () => {
    if (!file || !selectedType) {
      setUploadStatus({
        type: 'error',
        message: 'Please select document type and file',
      })
      return
    }

    setUploading(true)
    setUploadStatus(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('document_type', selectedType)
      formData.append('user_id', userId)
      formData.append('application_id', applicationId)

      const response = await documentsAPI.upload(formData)

      setUploadStatus({
        type: 'success',
        message: 'Document uploaded successfully!',
      })

      // Auto-verify
      await documentsAPI.verify(response.data.document_id)

      // Reset form
      setFile(null)
      setSelectedType('')
      
      if (onUploadSuccess) {
        onUploadSuccess(response.data)
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Upload failed. Please try again.',
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Documents</h3>

      {/* Document Type Selection */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Document Type
        </label>
        <select
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          disabled={uploading}
        >
          <option value="">Select document type...</option>
          {DOCUMENT_TYPES.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* File Upload */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select File
        </label>
        <div className="flex items-center space-x-2">
          <input
            type="file"
            onChange={handleFileChange}
            accept="image/*,.pdf"
            className="hidden"
            id="file-upload"
            disabled={uploading}
          />
          <label
            htmlFor="file-upload"
            className="flex-1 px-4 py-2 border-2 border-dashed border-gray-300 rounded-md cursor-pointer hover:border-primary-500 transition-colors"
          >
            <div className="flex items-center justify-center space-x-2 text-gray-600">
              <Upload className="w-5 h-5" />
              <span className="text-sm">
                {file ? file.name : 'Click to select file'}
              </span>
            </div>
          </label>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Supported formats: JPG, PNG, PDF (Max 10MB)
        </p>
      </div>

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={!file || !selectedType || uploading}
        className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
      >
        {uploading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Uploading...</span>
          </>
        ) : (
          <>
            <Upload className="w-5 h-5" />
            <span>Upload Document</span>
          </>
        )}
      </button>

      {/* Upload Status */}
      {uploadStatus && (
        <div className={`mt-4 p-3 rounded-md flex items-center space-x-2 ${
          uploadStatus.type === 'success' 
            ? 'bg-green-50 text-green-800' 
            : 'bg-red-50 text-red-800'
        }`}>
          {uploadStatus.type === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <XCircle className="w-5 h-5" />
          )}
          <span className="text-sm">{uploadStatus.message}</span>
        </div>
      )}
    </div>
  )
}


