const api_base = construct_api_url();

function construct_api_url(){
	let url = window.location.href;
	if (url.includes(':5173/')) url = url.replace(':5173/',':8000/')
    return url+'api/';
}

export function get(endpoint){
	return fetch(api_base+endpoint,{
		credentials: 'include',
		method: 'GET',
		headers: {
			"Content-Type": "application/json"
		}
	})
}

export function post(endpoint,data){
	return fetch(api_base+endpoint,{
		credentials: 'include',
		method: 'POST',
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	})
}