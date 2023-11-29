import cone from './app'
import van from 'vanjs-core'

const { navLink } = cone
const { div, nav, hr } = van.tags

const navbar = () => {

  return () =>
    div(
      nav(
        { class: 'nav' },
        navLink({name: 'home', class: 'navbar-link'}, 'Home')
      ),
      hr()
    )
};

export default navbar;
