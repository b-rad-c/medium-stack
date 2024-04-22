import van from 'vanjs-core'

const { table, tr, td } = van.tags

const keyValueTable = (data, props) => {

    const { tableClass, rowClass, lColClass, rColClass, keys, labels, end } = props || {};

    const keyList = keys || Object.keys(data)
    const keyFields = (labels && labels.length == keyList.length) ? labels : keyList

    const keyEnding = (typeof end !== 'undefined') ? end : ':'

    const rows = keyList.map((key, index) => {

        let value

        console.log('key typeof', key, typeof data[key], data[key])

        if (Array.isArray(data[key])) {
            value = data[key].join(', ')
        } else if (data[key] === null) {
            value = '-'
        } else if (typeof data[key] === 'object') {
            value = keyValueTable(data[key], props)
        }else {
            value = data[key]
        }

        return tr({ 'class': rowClass || 'key-value-table-row' },
            td({ 'class': lColClass || 'key-value-table-l-col' }, keyFields[index], keyEnding),
            td({ 'class': rColClass || 'key-value-table-r-col' }, value),
        )
    })

    return table({ 'class': tableClass || 'key-value-table' }, rows)

}

export { keyValueTable }
