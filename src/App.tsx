import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';

export default function App() {
  return (
    <div className='w-full h-screen bg-white dark:bg-black'>
      <Routes>
        <Route path='/' element={<Home />} />
      </Routes>
    </div>
  )
}
