import van from 'vanjs-core'
import * as vanX from "vanjs-ext"
import cone from '../../app'

const { router, navLink, pushHistory } = cone
const { section, div, h1, p, hr, ul, li, input, button, span } = van.tags

const fileUploadListItem = (fileUpload) => {
  console.log('fileUpload', fileUpload)
    return li(  navLink({name: 'file-uploader', params: {id: fileUpload.id}, context: {payload: fileUpload}}, fileUpload.id) )
  }

const fileUploadsPage = () => {

  const pageSize = van.state(5)
  const pageOffset = van.state(0)

  const pageState = van.state('')
  const fileUploadList = vanX.reactive([])

  const getFileUploads = () => {

    pageState.val = 'loading...'

    fetch(router.backendUrl('file-uploaders', {}, { size: pageSize.val, offset: pageOffset.val}))
      .then(r => {
        if (!r.ok) {
          console.log(r)
          throw new Error(r.statusText)
        }
        return r.json()
      })
      .then(data => { 
        console.log('data', data)
        if (data.length === 0 && pageOffset.val === 0) {
          pageState.val = 'no file uploaders found'
        }else if (data.length === 0) {
          pageState.val = 'no file uploaders on this page, go to previous page'
        }else{
          pageState.val = `showing file uploaders ${pageOffset.val + 1} thru ${pageOffset.val + data.length}`
        }
        
        // @ts-ignore
        fileUploadList.splice(0, Infinity, ...data)
      })
      .catch(error => {
        console.error(error)
        pageState.val = 'error: ' + error.toString()
      })
  }

  const pushBrowserUrl = () => pushHistory(router.navUrl('file-uploaders', {}, { size: pageSize.val, offset: pageOffset.val}))

  const nextPage = () => {
    pageOffset.val += pageSize.val
    pushBrowserUrl()
    getFileUploads()
  }

  const disableNextPage = vanX.calc(() => fileUploadList.length < pageSize.val)

  const prevPage = () => {
    pageOffset.val = Math.max(pageOffset.val -= pageSize.val, 0)
    pushBrowserUrl()
    getFileUploads()
  }

  const changePageSize = (event) => {
    pageSize.val = parseInt(event.target.value)
    pageOffset.val = 0
    pushBrowserUrl()
    getFileUploads()
  }

  const disablePrevPage = vanX.calc(() => pageOffset.val === 0)

  getFileUploads()

  return () => section(
      h1('File uploaders'),
      p(
        'page size:',
        input({type: "number", value: pageSize, oninput: changePageSize }),
        button({onclick: getFileUploads}, 'refresh'),
        span(' | '),
        button({onclick: prevPage, disabled:disablePrevPage}, 'prev'),
        span(' | '),
        button({onclick: nextPage, disabled:disableNextPage}, 'next'),
      ),
      hr(),
      div(
        pageState,
        vanX.list(ul, fileUploadList, v => fileUploadListItem(v.val))
      )
    );
};

export default fileUploadsPage;
