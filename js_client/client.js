const loginForm = document.querySelector('#login-form')
const baseEndpoint = "http://localhost:8000/api"
const contentContainer = document.querySelector('#content-container')
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
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
