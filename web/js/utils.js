async function SendRequest(url, data = null) {
    try {
        let params = {
            method: data == null ? 'GET' : 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            redirect: 'follow',
            referrerPolicy: 'no-referrer'
        }

        let isForm = data !== null && data instanceof FormData

        if (data != null)
            params.body = isForm ? data : JSON.stringify(data)

        if (!isForm)
            params.headers = {'Content-Type': 'application/json'}

        const response = await fetch(url, params)

        if (response?.ok)
            return await response.json()

        const error = await response.json()
        return {"status": "error", "message": error["message"]}
    }
    catch (error) {
        return {"status": "error", "message": error}
    }
}
