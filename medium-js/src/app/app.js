import createCone from 'van-cone';
import van from 'vanjs-core';
const { div } = van.tags;

console.log('context.js')

const routes = [
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
