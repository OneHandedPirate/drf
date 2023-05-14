const loginForm = document.querySelector('#login-form')
const searchForm = document.querySelector('#search-form')
const baseEndpoint = "http://localhost:8000/api"
const contentContainer = document.querySelector('#content-container')
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event) {
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)
    const options = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options)
        .then(response => response.json())
        .then(authData => {
            handleAuthData(authData, getProductList)
        })
        .catch(
            err => console.log(err)
        )
}

function handleSearch(event) {
    event.preventDefault()
    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    // console.log(data)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/v2/?${searchParams}`
    let headers = {
        "Content-Type": "application/json",

    }
    const authToken = localStorage.getItem('access')
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`
    }
    const options = {
        method: 'GET',
        headers: headers,
    }
    fetch(endpoint, options)
        .then(response => response.json())
        .then(data => {
            const validData = isTokenNotValid(data)
            if (validData && contentContainer) {
                contentContainer.innerHTML = ''
                if (data && data.hits) {
                    let htmlStr = ''
                    for (let result of data.hits) {
                        htmlStr += "<li>" + result.title + "</li>"
                    }
                    contentContainer.innerHTML = htmlStr
                    if (data.hits.length === 0) {
                        contentContainer.innerHTML = "<p>No results fount</p>"
                    }
                } else {
                    contentContainer.innerHTML = "<p>No results fount</p>"
                }
            }
            // writeToContainer(data)
        })
        .catch(
            err => console.log(err)
        )
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = '<pre>' +
            JSON.stringify(data, null, 4) + '</pre>'
    }
}

function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)
    if (callback) {
        callback()
    }
}

function getFetchOptions(method, body) {
    return {
        method: method === null ? 'GET' : method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === 'token_not_valid') {
        alert('Please log in again!')
    } else {
        return true
    }
}

function getProductList() {
    const endpoint = `${baseEndpoint}/products/`
    const options = getFetchOptions()
    fetch(endpoint, options)
        .then(response => {
            console.log(response)
            return response.json()
        })
        .then(data => {
            const validData = isTokenNotValid(data)
            if (validData) {
                writeToContainer(data)
            }
        })
}


const searchClient = algoliasearch('O6EQXFR0PU', '04c6af6e6556f875567b18453f9d833c');

const search = instantsearch({
    indexName: 'cfe_Product',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
    }),

    instantsearch.widgets.clearRefinements({
        container: '#clear-refinements',
    }),

    instantsearch.widgets.refinementList({
        container: '#user-list',
        attribute: 'user'
    }),

    instantsearch.widgets.refinementList({
        container: '#public-list',
        attribute: 'public'
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `
            <div>
                <div>{{ title }}</div>
                <div>{{ body }}</div>
                
                <p>{{ user }}</p><p>\${{ price }}</p>
            </div>`
        }
    })
]);

search.start();

