import van from 'vanjs-core'
import cone from '../app'
import { keyValueTable } from '../../components/widgets'

const { router, navLink } = cone
const { section, div, p, h1 } = van.tags

const userWidget = (user) => {
  return keyValueTable(
    user, 
    {
      keys: ['first_name', 'middle_name', 'last_name', 'email', 'phone_number'],
      labels: ['First Name', 'Middle Name', 'Last Name', 'Email', 'Phone']
    }
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
