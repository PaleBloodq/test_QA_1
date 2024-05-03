import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './assets/styles/global.css'
import { Provider } from 'react-redux'
import { HashRouter } from "react-router-dom";
import { store } from './store/store.ts'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Provider store={store}>
    <HashRouter basename={'/'}>
      <App />
    </HashRouter>
  </Provider>
)
