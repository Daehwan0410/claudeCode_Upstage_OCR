import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/common/Navbar'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import ReceiptList from './pages/ReceiptList'
import ReceiptDetail from './pages/ReceiptDetail'
import Stats from './pages/Stats'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/receipts" element={<ReceiptList />} />
          <Route path="/receipts/:id" element={<ReceiptDetail />} />
          <Route path="/stats" element={<Stats />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
