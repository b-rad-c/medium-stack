import van from 'vanjs-core'
import cone from '../app'


const { navLink } = cone
const { section, div, br, h1, h2, ul, li } = van.tags

const homePage = () => {

  return () =>
    section(
      h1('Home'),
      br(),
      div(
        h2('Core'),
        ul(
          li(navLink({name: 'users'}, 'Users')),
          li(navLink({name: 'file-uploaders'}, 'File uploaders')),
          li(navLink({name: 'image-files'}, 'Image files')),
          li(navLink({name: 'image-releases'}, 'Image releases')),
        ),
        h2('Art'),
        ul(
          li(navLink({name: 'artists'}, 'Artists')),
          li(navLink({name: 'still-images'}, 'Still images'))
        )
      )
    );
};

export default homePage;
