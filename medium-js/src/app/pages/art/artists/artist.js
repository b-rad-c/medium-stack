import van from 'vanjs-core'
import cone from '../../../app'
import { keyValueTable } from '../../../../components/widgets'

const { router, navLink } = cone
const { section, div, p, h1 } = van.tags

const artistWidget = (artist) => {
  return keyValueTable(artist,
    {
      keys: ['name', 'short_name', 'abreviated_name', 'summary', 'description', 'mediums', 'tags'],
      labels: ['name', 'short name', 'abreviated name', 'summary', 'description', 'mediums', 'tags']
    }
  )
}

const artistPage = (params, query, context) => {

  //
  // page state
  //

  const pageState = van.state('')
  const showArtist = van.state(false)
  let artistData = null
  
  //
  // load data function
  //

  const getArtist = () => {

    pageState.val = 'loading...'
    showArtist.val = false
    artistData = null

    const url = router.backendUrl('artist', params)

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
        artistData = data
        pageState.val = ''
        showArtist.val = true
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
    getArtist()
  }else{
    console.log('data preloaded')
    artistData = context.payload
    showArtist.val = true
  }

  return () =>
    section(
      h1('artist'),
      div(
        navLink({name: 'artists'}, '< artists'),
        () => showArtist.val === true ? artistWidget(artistData) : p(pageState)
      )
    );
};

export default artistPage;
