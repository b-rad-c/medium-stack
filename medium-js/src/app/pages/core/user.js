import van from 'vanjs-core'
import cone, { logout } from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li, div, button } = van.tags

//
// users
//

export const userWidget = (user) => {
  return keyValueTable(
    user, 
    {
      keys: ['first_name', 'middle_name', 'last_name', 'email', 'phone_number'],
      labels: ['First Name', 'Middle Name', 'Last Name', 'Email', 'Phone']
    }
  )
}

export const userListItem = (user) => li(navLink({ name: 'user', params: { cid: user.cid }, context: { payload: user } }, `${user.first_name} ${user.last_name}`))

export const userPage = (params, query, context) => contentModelPage('User', 'user', userWidget, { params, query, context })

export const userListPage = (params, query, context) => contentModelListPage('Users', 'users', userListItem, { params, query, context })

//
// me (authenticated user)
//

export const meWidget = (user) => keyValueTable(user)

export const mePage = (params, query, context) => {

  return div(
    contentModelPage('Me', 'me', meWidget, { params, query, context }, true),
    button({ onclick: logout }, 'Logout')
  )
  
}