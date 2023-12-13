import van from 'vanjs-core'

const { table, tr, td } = van.tags

const keyValueTable = (data, props) => {

    console.log('keyValueTable', data)

    const { tableClass, rowClass, lColClass, rColClass, keys, labels, end } = props || {};

    const keyList = keys || Object.keys(data)
    const keyFields = (labels && labels.length == keyList.length) ? labels : keyList

    const keyEnding = (typeof end !== 'undefined') ? end : ':'

    console.log('keyList', keyList)

    const rows = keyList.map((key, index) => {
        return tr({'class': rowClass || 'key-value-table-row'},
            td({'class': lColClass || 'key-value-table-l-col'}, keyFields[index], keyEnding),
            td({'class': rColClass || 'key-value-table-r-col'}, data[key]),
        )
    })

    console.log('rows', rows)

    return table({'class': tableClass || 'key-value-table'}, rows)

}

export { keyValueTable }
