import van from 'vanjs-core'
import * as vanX from "vanjs-ext"
import cone, { authenticatedFetch } from '../app/app'

const { router, pushHistory } = cone
const { section, div, h1, p, hr, ul, input, button, span } = van.tags

const contentModelPage = (pageTitle, routeName, contentModelWidget, routerData, authenticateFetch) => {
    const { params, query, context } = routerData
    //
    // page state
    //

    const pageState = van.state('')
    const showModel = van.state(false)
    let modelData = null

    //
    // load data function
    //

    const request = authenticateFetch === true ? authenticatedFetch : fetch

    const getModel = () => {

        pageState.val = 'loading...'
        showModel.val = false
        modelData = null

        const url = router.backendUrl(routeName, params)

        console.log('fetching', url)

        request(url)
            .then(r => {
                if (!r.ok) {
                    console.log(r)
                    throw new Error(r.statusText)
                }
                return r.json()
            })
            .then(data => {
                modelData = data
                pageState.val = ''
                showModel.val = true
            })
            .catch(error => {
                console.error(error)
                pageState.val = 'error: ' + error.toString()
            })
    }

    //
    // on initial load
    //

    if (typeof context.payload === 'undefined') {
        getModel()
    } else {
        console.log('data preloaded')
        modelData = context.payload
        showModel.val = true
    }

    return section(
        h1(pageTitle),
        div(
            () => showModel.val === true ? contentModelWidget(modelData) : p(pageState)
        )
    );
}


const contentModelListPage = (pageTitle, routeName, listItem, routerData) => {

    const { params, query, context } = routerData

    const pageSize = van.state(parseInt(query.size) || 25)
    const pageOffset = van.state(parseInt(query.offset) || 0)

    const pageState = van.state('')
    const itemList = vanX.reactive(context.payload || [])

    const getItems = () => {

        pageState.val = 'loading...'

        fetch(router.backendUrl(routeName, {}, { size: pageSize.val, offset: pageOffset.val }))
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
                    pageState.val = 'no items found'
                } else if (data.length === 0) {
                    pageState.val = 'no items on this page, go to previous page'
                } else {
                    pageState.val = `showing items ${pageOffset.val + 1} thru ${pageOffset.val + data.length}`
                }

                // @ts-ignore
                itemList.splice(0, Infinity, ...data)
            })
            .catch(error => {
                console.error(error)
                pageState.val = 'error: ' + error.toString()
            })
    }

    const pushBrowserUrl = () => pushHistory(router.navUrl(routeName, {}, { size: pageSize.val, offset: pageOffset.val }))

    const nextPage = () => {
        pageOffset.val += pageSize.val
        pushBrowserUrl()
        getItems()
    }

    const disableNextPage = vanX.calc(() => itemList.length < pageSize.val)

    const prevPage = () => {
        pageOffset.val = Math.max(pageOffset.val -= pageSize.val, 0)
        pushBrowserUrl()
        getItems()
    }

    const changePageSize = (event) => {
        pageSize.val = parseInt(event.target.value)
        pageOffset.val = 0
        pushBrowserUrl()
        getItems()
    }

    const disablePrevPage = vanX.calc(() => pageOffset.val === 0)

    getItems()

    return section(
        h1(pageTitle),
        p(
            'page size:',
            input({ type: "number", value: pageSize, oninput: changePageSize }),
            button({ onclick: getItems }, 'refresh'),
            span(' | '),
            button({ onclick: prevPage, disabled: disablePrevPage }, 'prev'),
            span(' | '),
            button({ onclick: nextPage, disabled: disableNextPage }, 'next'),
        ),
        hr(),
        div(
            pageState,
            vanX.list(ul, itemList, v => listItem(v.val))
        )
    );
};

export { contentModelListPage, contentModelPage }
