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

document.body.replaceChildren(App());
