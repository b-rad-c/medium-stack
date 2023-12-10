import van from 'vanjs-core'

const { section, div, br, h1, p, button, span, hr, ul, li } = van.tags

const userListItem = (user) => {
  console.log(user)
  return li(
    user.first_name + ' ' + user.last_name
  )
}

const usersPage = () => {

  const pageState = van.state('0 users')
  const userList = van.state([])

  /*



  use https://vanjs.org/x#reactive-list ?




  */

  const getUsers = () => {
    pageState.val = 'loading...'
    fetch('http://localhost:8000/api/v0/core/users')
    .then(r => r.json())
    .then(data => { 
      console.log(data)
      pageState.val = `${data.length} users`; 
      userList.val = data
    })
    .catch(error => {
      console.error(error)
      pageState.val = 'error: ' + error.toString()
    })
  }

  getUsers()

  return section(
      h1('Users'),
      p(pageState),
      br(),
      hr(),
      div(
        ul(() => userList.val.map(userListItem))
      )
    );
};

export default usersPage;
