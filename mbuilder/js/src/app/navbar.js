import cone, { appState } from './app'
import van from 'vanjs-core'

const { navLink } = cone
const { div, hr, span } = van.tags

const navbar = () => {

  return () =>
    div({class: 'navbar'},
      span({'id': 'nav-bar-title'}, 'Medium Tech'), 
      span({'id': 'nav-bar-title'}, ' | '),

      navLink({name: 'home', class: 'navbar-link'}, 'Home'),
      span({'id': 'nav-bar-title'}, ' | '),

      () => (appState.loggedIn) ? navLink({name: 'me', class: 'navbar-link'}, 'Me') : navLink({name: 'login', class: 'navbar-link'}, 'Login or Signup'),

      hr()
    )
};

export default navbar;
