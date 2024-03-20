import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Game from './pages/Game';
import Subscription from './pages/Subscription';
import Cart from './pages/Cart';

export default function App() {
  return (
    <div className='w-full h-full bg-white dark:bg-[#1a1e22]'>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/game/:gameId' element={<Game />} />
        <Route path='/subscription/:platform/:id' element={<Subscription />} />
        <Route path='/cart' element={<Cart />} />
      </Routes>
    </div>
  )
}
