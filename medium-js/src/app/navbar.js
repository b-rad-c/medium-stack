import cone from './app'
import van from 'vanjs-core'

const { navLink } = cone
const { div, nav, hr, h1, ul, li, span, p } = van.tags

const navbar = () => {

  return () =>
    div({class: 'navbar'},
      span({'id': 'nav-bar-title'}, 'Medium Tech | '), 
      navLink({name: 'home', class: 'navbar-link'}, 'Home'),
      hr()
    )
};

export default navbar;
