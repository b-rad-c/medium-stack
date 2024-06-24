import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li } = van.tags

// image file

export const imageFileWidget = (imageFile) => keyValueTable(imageFile, { keys: ['cid', 'payload_cid', 'height', 'width'] })

export const imageListItem = (imageFile) => li(navLink({ name: 'image-file', params: { cid: imageFile.cid }, context: { payload: imageFile } }, imageFile.cid))

export const imageFilePage = (params, query, context) => contentModelPage('Image File', 'image-file', imageFileWidget, { params, query, context })

export const imageFileListPage = (params, query, context) => contentModelListPage('Image Files', 'image-files', imageListItem, { params, query, context })

// image release

export const imageReleaseWidget = (imageRelease) => keyValueTable(imageRelease)

export const imageReleaseListItem = (imageRelease) => li(navLink({ name: 'image-release', params: { cid: imageRelease.cid }, context: { payload: imageRelease } }, imageRelease.cid))

export const imageReleasePage = (params, query, context) => contentModelPage('Image release', 'image-release', imageReleaseWidget, { params, query, context })

export const imageReleaseListPage = (params, query, context) => contentModelListPage('Image Releases', 'image-releases', imageReleaseListItem, { params, query, context })
