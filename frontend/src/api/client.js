import axios from 'axios'

// VITE_API_BASE_URL 환경변수 사용 (dev: http://localhost:8000, prod: 배포 URL)
const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '') + '/api'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
})

// 응답 에러 공통 처리 — FastAPI detail 필드 추출
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.detail ?? '서버 오류가 발생했습니다'
    return Promise.reject(new Error(message))
  }
)

// ── 영수증 API ────────────────────────────────────────────────────────────────

export const uploadReceipt = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/receipts/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000, // OCR 처리 시간 고려 (최대 60초)
  })
}

export const getReceipts = (params) =>
  api.get('/receipts', { params })

export const getReceipt = (id) =>
  api.get(`/receipts/${id}`)

export const updateReceipt = (id, data) =>
  api.put(`/receipts/${id}`, data)

export const deleteReceipt = (id) =>
  api.delete(`/receipts/${id}`)

// ── 통계 API ─────────────────────────────────────────────────────────────────

export const getStatsSummary = (params) =>
  api.get('/stats/summary', { params })

// ── 카테고리 API ──────────────────────────────────────────────────────────────

export const getCategories = () =>
  api.get('/categories')

export default api
