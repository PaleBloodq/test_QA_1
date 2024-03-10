import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';

export default function App() {
  return (
    <div className='w-screen h-screen bg-white dark:bg-[#1a1e22]'>
      <Routes>
        <Route path='/' element={<Home />} />
      </Routes>
    </div>
  )
}
