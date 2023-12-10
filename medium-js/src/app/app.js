import createCone from 'van-cone';
import van from 'vanjs-core';
const { div } = van.tags;
import usersPage from './pages/users';

console.log('app.js')

const routes = [
  {
    path: '/users/:userId',
    name: 'user',
    title: 'Medium Tech | User',
    callable: async () => import('./pages/user')
  },
  {
    path: '/users',
    name: 'users',
    title: 'Medium Tech | Users',
    callable: async () => usersPage
  },
  {
    path: '/',
    name: 'home',
    title: 'Medium Tech | Home',
    callable: async () => import('./pages/home')
  },
  {
    path: '.*',
    name: 'notFound',
    title: 'Medium Tech | Not Found',
    callable: async () => import('./pages/notFound')
  },
];


const layoutElement = div({ id: 'layout' })

const cone = createCone(layoutElement, routes)
export default cone
