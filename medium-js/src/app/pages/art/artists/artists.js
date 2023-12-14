import van from 'vanjs-core'
import * as vanX from "vanjs-ext"
import cone from '../../../app'

const { router, navLink, pushHistory } = cone
const { section, div, h1, p, hr, ul, li, input, button, span } = van.tags

const artistListItem = (artist) => li(  navLink({name: 'artist', params: {cid: artist.cid}, context: {payload: artist}}, artist.name) )

const artistsPage = () => {

  const pageSize = van.state(5)
  const pageOffset = van.state(0)

  const pageState = van.state('')
  const artistList = vanX.reactive([])

  const getArtists = () => {

    pageState.val = 'loading...'

    fetch(router.backendUrl('artists', {}, { size: pageSize.val, offset: pageOffset.val}))
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
          pageState.val = 'no artists found'
        }else if (data.length === 0) {
          pageState.val = 'no artists on this page, go to previous page'
        }else{
          pageState.val = `showing artists ${pageOffset.val + 1} thru ${pageOffset.val + data.length}`
        }
        
        // @ts-ignore
        artistList.splice(0, Infinity, ...data)
      })
      .catch(error => {
        console.error(error)
        pageState.val = 'error: ' + error.toString()
      })
  }

  const pushBrowserUrl = () => pushHistory(router.navUrl('artists', {}, { size: pageSize.val, offset: pageOffset.val}))

  const nextPage = () => {
    pageOffset.val += pageSize.val
    pushBrowserUrl()
    getArtists()
  }

  const disableNextPage = vanX.calc(() => artistList.length < pageSize.val)

  const prevPage = () => {
    pageOffset.val = Math.max(pageOffset.val -= pageSize.val, 0)
    pushBrowserUrl()
    getArtists()
  }

  const changePageSize = (event) => {
    pageSize.val = parseInt(event.target.value)
    pageOffset.val = 0
    pushBrowserUrl()
    getArtists()
  }

  const disablePrevPage = vanX.calc(() => pageOffset.val === 0)

  getArtists()

  return () => section(
      h1('Artists'),
      p(
        'page size:',
        input({type: "number", value: pageSize, oninput: changePageSize }),
        button({onclick: getArtists}, 'refresh'),
        span(' | '),
        button({onclick: prevPage, disabled:disablePrevPage}, 'prev'),
        span(' | '),
        button({onclick: nextPage, disabled:disableNextPage}, 'next'),
      ),
      hr(),
      div(
        pageState,
        vanX.list(ul, artistList, v => artistListItem(v.val))
      )
    );
};

export default artistsPage;
