import { Routes, Route, useLocation } from 'react-router-dom';
import { useTransition, animated } from 'react-spring';
import Home from './pages/Home';
import Game from './pages/Game';
import Subscription from './pages/Subscription';
import Cart from './pages/Cart';
import { useEffect } from 'react';
import DonationPage from './pages/DonationPage';
import SearchPage from './pages/SearchPage';
import Profile from './pages/Profile';

export default function App() {

  const location = useLocation();
  const transitions = useTransition(location, {
    from: { opacity: 0 },
    enter: { opacity: 1 },
    leave: { opacity: 0 },
    config: { duration: 300 }
  });

  useEffect(() => {
    setTimeout(() => {
      window.scrollTo(0, 0);
    }, 300)
  }, [location])

  return transitions((styles, item) => (
    <animated.div style={styles} className="animated-page">
      <div className='w-full h-full bg-white dark:bg-[#1a1e22]'>
        <Routes location={item}>
          <Route path='/' element={<Home />} />
          <Route path='/game/:gameId' element={<Game />} />
          <Route path='/subscription/:subscriptionId/:id' element={<Subscription />} />
          <Route path='/donation/:id' element={<DonationPage />} />
          <Route path='/search' element={<SearchPage />} />
          <Route path='/cart' element={<Cart />} />
          <Route path='/profile' element={<Profile />} />
        </Routes>
      </div>
    </animated.div>
  ))
}
