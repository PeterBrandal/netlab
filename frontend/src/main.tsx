import { createRoot } from 'react-dom/client'
import { Terminal } from './Terminal'

export function App() {
    return <Terminal />
}

const app = document.getElementById('app')

if (!app) throw new Error('shi failed')



createRoot(app).render(<App />)