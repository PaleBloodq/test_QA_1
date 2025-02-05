import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './assets/styles/global.css'
import { Provider } from 'react-redux'
import { BrowserRouter } from "react-router-dom";
import { store } from './store/store.ts'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Provider store={store}>
    <BrowserRouter basename={import.meta.env.VITE_BASE_URL}>
      <App />
    </BrowserRouter>
  </Provider>
)
