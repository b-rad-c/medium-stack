import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li } = van.tags

// still image

export const stillImageWidget = (stillImage) => keyValueTable(stillImage)

export const stillImageListItem = (stillImage) => li(navLink({ name: 'still-image', params: { cid: stillImage.cid }, context: { payload: stillImage } }, stillImage.cid))

export const stillImagePage = (params, query, context) => contentModelPage('Still image', 'still-image', stillImageWidget, { params, query, context })

export const stillImageListPage = (params, query, context) => contentModelListPage('Still Images', 'still-images', stillImageListItem, { params, query, context })
