import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li } = van.tags

const imageFileWidget = (imageFile) => keyValueTable(imageFile, { keys: ['cid', 'payload_cid', 'height', 'width'] })

const imageListItem = (imageFile) => li(navLink({ name: 'image-file', params: { cid: imageFile.cid }, context: { payload: imageFile } }, imageFile.cid))

const imageFilePage = (params, query, context) => contentModelPage('Image File', 'image-file', imageFileWidget, { params, query, context })

const imageFileListPage = (params, query, context) => contentModelListPage('Image Files', 'image-files', imageListItem, { params, query, context })

export default imageFilePage
export { imageListItem, imageFileListPage, imageFilePage, imageFileWidget }
