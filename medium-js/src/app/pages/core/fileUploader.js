import van from 'vanjs-core'
import cone from '../../app'
import { keyValueTable } from '../../../components/widgets'
import { contentModelListPage, contentModelPage } from '../../../components/page'

const { navLink } = cone
const { li } = van.tags

export const fileUploaderWidget = (fileUploader) => keyValueTable(fileUploader)

export const fileUploaderListItem = (fileUploader) => li(navLink({ name: 'file-uploader', params: { id: fileUploader.id }, context: { payload: fileUploader } }, fileUploader.id))

export const fileUploaderPage = (params, query, context) => contentModelPage('File uploader', 'file-uploader', fileUploaderWidget, { params, query, context })

export const fileUploaderListPage = (params, query, context) => contentModelListPage('File uploaders', 'file-uploaders', fileUploaderListItem, { params, query, context })
