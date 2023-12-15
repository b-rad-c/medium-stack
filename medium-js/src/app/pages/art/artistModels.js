import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li } = van.tags

export const artistWidget = (artist) => {
  return keyValueTable(artist,
    {
      keys: ['name', 'short_name', 'abreviated_name', 'summary', 'description', 'mediums', 'tags'],
      labels: ['name', 'short name', 'abreviated name', 'summary', 'description', 'mediums', 'tags']
    }
  )
}

export const artistListItem = (artist) => li(  navLink({name: 'artist', params: {cid: artist.cid}, context: {payload: artist}}, artist.name) )

export const artistPage = (params, query, context) => contentModelPage('Artist', 'artist', artistWidget, { params, query, context })

export const artistListPage = (params, query, context) => contentModelListPage('Artists', 'artists', artistListItem, { params, query, context })
