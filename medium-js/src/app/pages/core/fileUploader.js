import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'

const { router, navLink } = cone
const { section, div, p, h1 } = van.tags

const fileUploaderWidget = (fileUploader) => keyValueTable(fileUploader)

const fileUploaderPage = (params, query, context) => {

  //
  // page state
  //

  const pageState = van.state('')
  const showFileUploader = van.state(false)
  let fileUploaderData = null
  
  //
  // load data function
  //

  const getFileUploader = () => {

    pageState.val = 'loading...'
    showFileUploader.val = false
    fileUploaderData = null

    const url = router.backendUrl('file-uploader', params)

    console.log ('fetching', url)

    fetch(url)
      .then(r => {
        if (!r.ok) {
          console.log(r)
          throw new Error(r.statusText)
        }
        return r.json()
      })
      .then(data => { 
        fileUploaderData = data
        pageState.val = ''
        showFileUploader.val = true
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
    getFileUploader()
  }else{
    console.log('data preloaded')
    fileUploaderData = context.payload
    showFileUploader.val = true
  }

  return () =>
    section(
      h1('file uploader'),
      div(
        navLink({name: 'file-uploaders'}, '< file uploaders'),
        () => showFileUploader.val === true ? fileUploaderWidget(fileUploaderData) : p(pageState)
      )
    );
};

export default fileUploaderPage;
