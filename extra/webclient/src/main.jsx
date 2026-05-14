import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { store } from './store/store.js'
import { Provider } from 'react-redux'
import 'virtual:svg-icons-register'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <App/>
    </Provider>
  </StrictMode>,
)
