import van from 'vanjs-core'
import cone from '../app'


const { navLink } = cone
const { section, div, br, h1, img } = van.tags

const homePage = () => {

  return () =>
    section(
      h1('Home'),
      br(),
      div(
        navLink({name: 'users'}, 'Users')
      )
    );
};

export default homePage;
