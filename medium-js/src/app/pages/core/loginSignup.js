import van from 'vanjs-core'
import * as vanX from 'vanjs-ext'
import cone, { setAuthToken, appState } from '../../app'


const { router, navigate } = cone
const { section, div, br, h1, button, input, p } = van.tags

const loading = van.state(false)

const signupForm = () => {

  const data = vanX.reactive({
    email: 'brad@email.com',
    first_name: 'Brad',
    middle_name: 'R',
    last_name: 'Corlett',
    password1: 'password',
    password2: 'password',
    phone_number: 'tel:+1-513-555-0123'
  })

  const signup = () => {

    const url = router.backendUrl('users')

    loading.val = true

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    }).then(r => {
      loading.val = false
      if (!r.ok) {
        console.log(r)
        throw new Error(r.statusText)
      }
      return r.json()
    })
      .then(data => {
        loading.val = false
        console.log('data', data)
      })
      .catch(error => {
        loading.val = false
        console.error(error)
      })
  }

  return div(
    'email: ',
    input({ type: 'text', value: () => data.email, oninput: e => data.email = e.target.value }), br(),
    'first name: ',
    input({ type: 'text', value: () => data.first_name, oninput: e => data.first_name = e.target.value }), br(),
    'middle name: ',
    input({ type: 'text', value: () => data.middle_name, oninput: e => data.middle_name = e.target.value }), br(),
    'last name: ',
    input({ type: 'text', value: () => data.last_name, oninput: e => data.last_name = e.target.value }), br(),
    'phone number: ',
    input({ type: 'text', value: () => data.phone_number, oninput: e => data.phone_number = e.target.value }), br(),
    'password: ',
    input({ type: 'password', value: () => data.password1, oninput: e => data.password1 = e.target.value }), br(),
    'confirm password: ',
    input({ type: 'password', value: () => data.password2, oninput: e => data.password2 = e.target.value }), br(),

    button({ onclick: () => signup(), disabled: () => loading.val === true }, 'signup'),
  )
}

const loginForm = () => {
  const data = vanX.reactive({ username: 'brad@email.com', password: 'password' })

  const login = () => {

    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);

    loading.val = true

    fetch(router.backendUrl('login'), {
      method: 'POST',
      body: formData
    }).then(r => {
      loading.val = false
      if (!r.ok) {
        console.log(r)
        throw new Error(r.statusText)
      }
      return r.json()
    })
      .then(data => {
        loading.val = false
        console.log('login successful')
        setAuthToken(data.access_token)
        navigate(router.navUrl('me'))
      })
      .catch(error => {
        loading.val = false
        console.error(error)
      })
  }

  return div(
    'username: ',
    input({
      type: 'text', value: () => data.username,
      oninput: e => data.username = e.target.value
    }), ' ',
    'password: ',
    input({
      type: 'password', value: () => data.password,
      oninput: e => data.password = e.target.value
    }), ' ',
    br(),
    button({ onclick: () => login(), disabled: () => loading.val === true }, 'login'),
  )
}

const loginSignupPage = () => {

  console.log('loginSignupPage - appState.loggedIn', appState.loggedIn)

  return () =>
    section(
      h1('Login'),
      br(),
      loginForm(),
      h1('Signup'),
      signupForm()
    );
};

export default loginSignupPage;
