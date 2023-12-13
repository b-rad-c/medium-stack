import van from 'vanjs-core'
import cone from '../app'

const { router, navLink } = cone
const { section, div, p, h1, table, tr, td } = van.tags

const userWidget = (user) => {

  return table(
    tr(
      td('first name:'),
      td(user.first_name),
    ),
    tr(
      td('middle name:'),
      td(user.middle_name),
    ),
    tr(
      td('last name:'),
      td(user.last_name),
    ),
    tr(
      td('email:'),
      td(user.email),
    ),
    tr(
      td('phone number:'),
      td(user.phone_number),
    )
  )

}

const userPage = (params, query, context) => {

  //
  // page state
  //

  console.log('userPage')

  const pageState = van.state('')
  const showUser = van.state(false)
  let userData = null
  
  //
  // load data function
  //

  const getUser = () => {

    pageState.val = 'loading...'
    showUser.val = false
    userData = null

    const url = router.backendUrl('user', params)

    console.log ('fetching', url)

    fetch(url)
      .then(r => r.json())
      .then(data => { 
        userData = data
        pageState.val = ''
        showUser.val = true
      })
      .catch(error => {
        console.error(error)
        pageState.val = 'error: ' + error.toString()
      })
  }

  //
  // on initial load
  //

  if(typeof context.payload === 'undefined') {
    getUser()
  }else{
    console.log('data preloaded')
    userData = context.payload
    showUser.val = true
  }

  return () =>
    section(
      h1('user'),
      div(
        navLink({name: 'users'}, '< users'),
        () => showUser.val === true ? userWidget(userData) : p(pageState)
      )
    );
};

export default userPage;
