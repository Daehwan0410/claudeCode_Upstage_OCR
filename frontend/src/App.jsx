import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/common/Navbar'
import Sidebar from './components/common/Sidebar'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import ReceiptList from './pages/ReceiptList'
import ReceiptDetail from './pages/ReceiptDetail'
import Stats from './pages/Stats'

export default function App() {
  return (
    <BrowserRouter>
      {/* 전체 레이아웃: Navbar(상단) + Sidebar(좌) + 콘텐츠(우) */}
      <div className="h-screen flex flex-col">
        <Navbar />
        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto bg-slate-50 p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/receipts" element={<ReceiptList />} />
              <Route path="/receipts/:id" element={<ReceiptDetail />} />
              <Route path="/stats" element={<Stats />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}
