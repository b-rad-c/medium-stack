import van from 'vanjs-core'
import cone, { NotLoggedInError, authenticatedFetch, logout, appState } from '../../app'
import { keyValueTable } from '../../../components/widgets'

const { router } = cone
const { section, div, p, h1, br, button } = van.tags

const userWidget = (user) => keyValueTable(user)

const mePage = (params, query, context) => {

  //
  // page state
  //

  const pageState = van.state('')
  const showUser = van.state(false)
  let userData = null
  
  //
  // load data function
  //

  const getMe = () => {

    pageState.val = 'loading...'
    showUser.val = false
    userData = null

    const url = router.backendUrl('me', params)

    console.log ('fetching', url)

    authenticatedFetch(url)
      .then(r => {
        if (!r.ok) {
          console.log(r)
          throw new Error(r.statusText)
        }
        return r.json()
      })
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
    try{
      getMe()
    }catch(error){
      console.error(error)

      if (error instanceof NotLoggedInError) {
        console.error(error)
        pageState.val = 'Not logged in'
      }else {
        pageState.val = 'Unknown error'
      }
      
    }
    
  }else{
    console.log('data preloaded')
    userData = context.payload
    showUser.val = true
  }

  return () =>
    section(
      h1('me'),
      div(
        () => showUser.val === true ? userWidget(userData) : p(pageState)
      ),
      br(),
      button({onclick: logout}, 'logout')
    );
};

export default mePage;
