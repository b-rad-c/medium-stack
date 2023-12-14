import createCone from 'van-cone';
import van from 'vanjs-core';
const { div } = van.tags;

const routes = [
  {
    path: '/art/artists/:cid',
    backend: '/art/artists/cid/:cid',
    name: 'artist',
    title: 'Medium Tech | Artist',
    callable: async () => import('./pages/art/artists/artist')
  },
  {
    path: '/art/artists',
    backend: '/mart/artists',
    name: 'artists',
    title: 'Medium Tech | Artists',
    callable: async () => import('./pages/art/artists/artists')
  },
  {
    path: '/file-uploader',
    backend: '/core/file-uploader',
    name: 'file-uploader',
    title: 'Medium Tech | File Uploader',
    callable: async () => import('./pages/core/fileUploader')
  },
  {
    path: '/file-uploaders',
    backend: '/core/file-uploader',
    name: 'file-uploaders',
    title: 'Medium Tech | File Uploaders',
    callable: async () => import('./pages/core/fileUploaders')
  },
  {
    path: '/users/:cid',
    backend: '/core/users/cid/:cid',
    name: 'user',
    title: 'Medium Tech | User',
    callable: async () => import('./pages/core/user')
  },
  {
    path: '/users',
    backend: '/core/users',
    name: 'users',
    title: 'Medium Tech | Users',
    callable: async () => import('./pages/core/users')
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
