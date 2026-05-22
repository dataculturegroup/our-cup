import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

// only include the boostrap CSS in dev mode because in prod the wrapping HTML includes it already
if (import.meta.env.MODE === 'development') {
  import('bootstrap/dist/css/bootstrap.min.css')
}

const app = mount(App, {
  target: document.getElementById('app')
})

export default app
