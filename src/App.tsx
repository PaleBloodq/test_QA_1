import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Game from './pages/Game';

export default function App() {
  return (
    <div className='w-screen h-full bg-white dark:bg-[#1a1e22]'>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/game/:gameId' element={<Game />} />
      </Routes>
    </div>
  )
}
