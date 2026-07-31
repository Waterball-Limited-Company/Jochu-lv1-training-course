import './styles/app.css'
import { createRouter } from './router'

const root = document.querySelector<HTMLElement>('#app')
if (!root) throw new Error('Missing #app root')

if (location.pathname === '/') history.replaceState({}, '', '/home')
const router = createRouter(root)
void router.render()
