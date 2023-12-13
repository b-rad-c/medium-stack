import createCone from 'van-cone';
import van from 'vanjs-core';
const { div } = van.tags;

const routes = [
  {
    path: '/users/:cid',
    backend: '/core/users/cid/:cid',
    name: 'user',
    title: 'Medium Tech | User',
    callable: async () => import('./pages/user')
  },
  {
    path: '/users',
    backend: '/core/users',
    name: 'users',
    title: 'Medium Tech | Users',
    callable: async () => import('./pages/users')
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
const cone = createCone(layoutElement, routes, null, { backendPrefix: 'http://localhost:8000/api/v0' })
export default cone
