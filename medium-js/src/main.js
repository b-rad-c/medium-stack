import van from 'vanjs-core'
import cone, { appState } from './app/app'
import navbar from './app/navbar'
import './main.css'
const { div } = van.tags;

const { routerElement } = cone

const Navbar = navbar();

const App = () =>
  div(
    Navbar(),
    routerElement
  );

document.body.replaceChildren(App());
