import cone, { appState } from './app'
import van from 'vanjs-core'
import * as vanX from 'vanjs-ext'

const { navLink } = cone
const { div, hr, span } = van.tags

const notLoggedIn = () => [
  span({'id': 'nav-bar-title'}, ' | '), 
  navLink({name: 'login', class: 'navbar-link'}, 'Login or Signup')
]

const loggedIn = () => [
  span({'id': 'nav-bar-title'}, ' | '),
  navLink({name: 'me', class: 'navbar-link'}, 'Me')
]

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
