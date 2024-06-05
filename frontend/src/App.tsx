import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { useTransition, animated } from 'react-spring';
import Home from './pages/Home';
import Game from './pages/Game';
import Subscription from './pages/Subscription';
import Cart from './pages/Cart';
import { useEffect } from 'react';
import DonationPage from './pages/DonationPage';
import SearchPage from './pages/SearchPage';
import Profile from './pages/Profile';
import { useGetUserQuery, useRefreshTokenMutation } from './services/userApi';
import { setIsLoggined, setUpdateData, setUserData } from './features/User/userSlice';
import { useDispatch } from 'react-redux';

export default function App() {



  window.Telegram.WebApp.expand()
  const dispatch = useDispatch();
  const location = useLocation();
  const transitions = useTransition(location, {
    from: { opacity: 0 },
    enter: { opacity: 1 },
    leave: { opacity: 0 },
    config: { duration: 400 },
    exitBeforeEnter: true,
  });
  const navigate = useNavigate();

  const { data: userData, error: userError } = useGetUserQuery({});
  const [refreshToken, { data: refreshData, error: refreshError }] = useRefreshTokenMutation()

  useEffect(() => {
    dispatch(setUserData(userData))
    dispatch(setUpdateData({
      psEmail: userData?.playstation_email,
      psPassword: userData?.playstation_password,
      billEmail: userData?.bill_email,
    }))
    if (userData !== undefined) {
      dispatch(setIsLoggined((true)))
    } else {
      dispatch(setIsLoggined((false)))
    }
  }, [userData])


  useEffect(() => {
    if (userError && 'status' in userError && userError.status === 403) {
      refreshToken({ token: sessionStorage.getItem('token') })
    }
  }, [userError])

  useEffect(() => {
    if (refreshData) {
      const newToken = refreshData?.token;
      sessionStorage.setItem('token', newToken);

      const tokenRegex = /token=([^&#]+)/;
      let url = window.location.href;
      if (url.match(tokenRegex)) {
        url = url.replace(tokenRegex, `token=${newToken}`);
      } else {
        const separator = url.includes('?') ? '&' : '?';
        url += `${separator}token=${newToken}`;
      }

      window.history.pushState({}, '', url);
      window.location.reload()
    }
  }, [refreshData]);

  useEffect(() => {
    if (refreshError) {
      window.Telegram.WebApp.showAlert('Произошла ошибка, пожалуйста перезайдите в приложение', () => {
        window.Telegram.WebApp.close()
      });
    }
  }, [refreshError])



  const telegramThemeColor = window?.Telegram?.WebApp.headerColor

  useEffect(() => {
    const bodyDiv = document.getElementById('webapp-root-body')
    if (telegramThemeColor === '#ffffff') {
      bodyDiv.classList.value = 'light'
      bodyDiv.style.backgroundColor = '#ffffff'

    } else {
      bodyDiv.classList.value = 'dark'
      bodyDiv.style.backgroundColor = '#000000'
    }

  }, [telegramThemeColor])

  const backButton = window?.Telegram?.WebApp.BackButton
  useEffect(() => {
    if (location.pathname !== '/') {
      backButton && backButton.show()
    } else {
      backButton.hide()
    }
    backButton && backButton.onClick(() => navigate(-1))
  }, [location.pathname])



  return transitions((styles, item) => (
    <animated.div style={styles} className="animated-page">
      <div className='w-full h-full bg-white dark:bg-[#1a1e22]'>
        <Routes location={item}>
          <Route path='/' element={<Home />} />
          <Route path='/game/:gameId/:pubId' element={<Game />} />
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