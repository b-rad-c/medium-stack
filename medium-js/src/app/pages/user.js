import van from 'vanjs-core'

const { section, div, br, h1, img } = van.tags

const userPage = () => {

  return () =>
    section(
      h1('user'),
      br(),
      div()
    );
};

export default userPage;
