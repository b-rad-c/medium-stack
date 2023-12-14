import van from 'vanjs-core'

const { table, tr, td } = van.tags

const keyValueTable = (data, props) => {

    const { tableClass, rowClass, lColClass, rColClass, keys, labels, end } = props || {};

    const keyList = keys || Object.keys(data)
    const keyFields = (labels && labels.length == keyList.length) ? labels : keyList

    const keyEnding = (typeof end !== 'undefined') ? end : ':'

    const rows = keyList.map((key, index) => {
        const value = (Array.isArray(data[key])) ? data[key].join(', ') : data[key]
        return tr({'class': rowClass || 'key-value-table-row'},
            td({'class': lColClass || 'key-value-table-l-col'}, keyFields[index], keyEnding),
            td({'class': rColClass || 'key-value-table-r-col'}, value),
        )
    })

    return table({'class': tableClass || 'key-value-table'}, rows)

}

export { keyValueTable }
