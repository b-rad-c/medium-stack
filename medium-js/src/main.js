import navbar from './app/navbar'
import van from 'vanjs-core'
import cone from './app/app'
import './main.css'
const { div } = van.tags;

const { routerElement, router } = cone

const Navbar = navbar();

const App = () =>
  div(
    Navbar(),
    routerElement
  );

console.log(router.formatUrl('user', { userId: 123 }, { activeTab: 'profile'}))

document.body.replaceChildren(App());
