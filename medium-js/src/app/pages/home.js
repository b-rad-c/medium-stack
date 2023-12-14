import van from 'vanjs-core'
import cone from '../app'


const { navLink } = cone
const { section, div, br, h1, ul, li } = van.tags

const homePage = () => {

  return () =>
    section(
      h1('Home'),
      br(),
      div(
        ul(
          li(navLink({name: 'users'}, 'Users')),
          li(navLink({name: 'file-uploaders'}, 'File uploaders')),
          li(navLink({name: 'artists'}, 'Artists')),
        )
      )
    );
};

export default homePage;
