import van from 'vanjs-core'
import * as vanX from "vanjs-ext"
import cone from '../../app'

const { router, navLink, pushHistory } = cone
const { section, div, h1, p, hr, ul, li, input, button, span } = van.tags

const userListItem = (user) => {
  const fullName = user.first_name + ' ' + user.last_name
  return li(  navLink({name: 'user', params: {cid: user.cid}, context: {payload: user}}, fullName) )
}

const usersPage = () => {

  const pageSize = van.state(5)
  const pageOffset = van.state(0)

  const pageState = van.state('')
  const userList = vanX.reactive([])

  const getUsers = () => {

    pageState.val = 'loading...'

    fetch(router.backendUrl('users', {}, { size: pageSize.val, offset: pageOffset.val}))
      .then(r => {
        if (!r.ok) {
          console.log(r)
          throw new Error(r.statusText)
        }
        return r.json()
      })
      .then(data => { 
        if (data.length === 0 && pageOffset.val === 0) {
          pageState.val = 'no users found'
        }else if (data.length === 0) {
          pageState.val = 'no users on this page, go to previous page'
        }else{
          pageState.val = `showing users ${pageOffset.val + 1} thru ${pageOffset.val + data.length}`
        }
        
        // @ts-ignore
        userList.splice(0, Infinity, ...data)
      })
      .catch(error => {
        console.error(error)
        pageState.val = 'error: ' + error.toString()
      })
  }

  const pushBrowserUrl = () => pushHistory(router.navUrl('users', {}, { size: pageSize.val, offset: pageOffset.val}))

  const nextPage = () => {
    pageOffset.val += pageSize.val
    pushBrowserUrl()
    getUsers()
  }

  const disableNextPage = vanX.calc(() => userList.length < pageSize.val)

  const prevPage = () => {
    pageOffset.val = Math.max(pageOffset.val -= pageSize.val, 0)
    pushBrowserUrl()
    getUsers()
  }

  const changePageSize = (event) => {
    pageSize.val = parseInt(event.target.value)
    pageOffset.val = 0
    pushBrowserUrl()
    getUsers()
  }

  const disablePrevPage = vanX.calc(() => pageOffset.val === 0)

  getUsers()

  return () => section(
      h1('Users'),
      p(
        'page size:',
        input({type: "number", value: pageSize, oninput: changePageSize }),
        button({onclick: getUsers}, 'refresh'),
        span(' | '),
        button({onclick: prevPage, disabled:disablePrevPage}, 'prev'),
        span(' | '),
        button({onclick: nextPage, disabled:disableNextPage}, 'next'),
      ),
      hr(),
      div(
        pageState,
        vanX.list(ul, userList, v => userListItem(v.val))
      )
    );
};

export default usersPage;
