import createCone from 'van-cone';
import van from 'vanjs-core';
import * as vanX from 'vanjs-ext';
const { div } = van.tags;

//
// cone app
//

const routes = [

  //
  // art
  //

  // still images

  {
    path: '/art/still-images/:cid',
    backend: '/mart/still-images/cid/:cid',
    name: 'still-image',
    title: 'Medium Tech | Still Image',
    callable: async () => (await import('./pages/art/imageModels')).stillImagePage
  },
  {
    path: '/art/still-images',
    backend: '/mart/still-images',
    name: 'still-images',
    title: 'Medium Tech | Still Images',
    callable: async () => (await import('./pages/art/imageModels')).stillImageListPage
  },

  // artists

  {
    path: '/art/artists/:cid',
    backend: '/art/artists/cid/:cid',
    name: 'artist',
    title: 'Medium Tech | Artist',
    callable: async () => (await import('./pages/art/artistModels')).artistPage
  },
  {
    path: '/art/artists',
    backend: '/mart/artists',
    name: 'artists',
    title: 'Medium Tech | Artists',
    callable: async () => (await import('./pages/art/artistModels')).artistListPage
  },

  //
  // core
  //

  // file uploaders

  {
    path: '/file-uploader',
    backend: '/core/file-uploader',
    name: 'file-uploader',
    title: 'Medium Tech | File Uploader',
    callable: async () => (await import('./pages/core/fileUploader')).fileUploaderPage
  },
  {
    path: '/file-uploaders',
    backend: '/core/file-uploader',
    name: 'file-uploaders',
    title: 'Medium Tech | File Uploaders',
    callable: async () => (await import('./pages/core/fileUploader')).fileUploaderListPage
  },

  // images

  {
    path: '/image-files/:cid',
    backend: '/core/image-files/cid/:cid',
    name: 'image-file',
    title: 'Medium Tech | Image File',
    callable: async () => (await import('./pages/core/imageModels')).imageFilePage
  },
  {
    path: '/image-files',
    backend: '/core/image-files',
    name: 'image-files',
    title: 'Medium Tech | Imagae Files',
    callable: async () => (await import('./pages/core/imageModels')).imageFileListPage
  },

  {
    path: 'image-release/:cid',
    backend: '/core/image-release/cid/:cid',
    name: 'image-release',
    title: 'Medium Tech | Image Release',
    callable: async () => (await import('./pages/core/imageModels')).imageReleasePage
  },
  {
    path: '/image-release',
    backend: '/core/image-release',
    name: 'image-releases',
    title: 'Medium Tech | Image Releases',
    callable: async () => (await import('./pages/core/imageModels')).imageReleaseListPage
  },

  // users

  {
    path: '/users/me',
    backend: '/core/users/me',
    name: 'me',
    title: 'Medium Tech | Me',
    callable: async () => (await import('./pages/core/user')).mePage
  },
  {
    path: '/users/:cid',
    backend: '/core/users/cid/:cid',
    name: 'user',
    title: 'Medium Tech | User',
    callable: async () => (await import('./pages/core/user')).userPage
  },
  {
    path: '/users',
    backend: '/core/users',
    name: 'users',
    title: 'Medium Tech | Users',
    callable: async () => (await import('./pages/core/user')).userListPage
  },
  {
    path: '/login',
    backend: '/core/auth/login',
    name: 'login',
    title: 'Medium Tech | Login',
    callable: async () => import('./pages/core/loginSignup')
  },

  //
  // main
  //

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

//
// app state
//

const appState = vanX.reactive({ loggedIn: false })

//
// authentication
//

class NotLoggedInError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NotLoggedInError';
  }
}

const getAuthToken = () => localStorage.getItem('authToken')

const setAuthToken = (token) => {
  localStorage.setItem('authToken', token)
  appState.loggedIn = true
}
const logout = () => {
  localStorage.removeItem('authToken')
  appState.loggedIn = false
  cone.navigate(cone.router.navUrl('login'))
}

const authenticatedFetch = (url, options) => {
  const authToken = getAuthToken()
  if (!authToken) {
    throw new NotLoggedInError('Not logged in')
  }
  const params = options || {}
  if (!params.headers) params.headers = {}
  params.headers['Authorization'] = `Bearer ${authToken}`
  return fetch(url, { ...params })
}

//
// set initial state
//

appState.loggedIn = !!getAuthToken()

export default cone
export { getAuthToken, setAuthToken, authenticatedFetch, logout, appState, NotLoggedInError }
