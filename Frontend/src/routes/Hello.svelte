<script>
    import { onMount } from 'svelte';
    let response = $state(null);

    async function load(){
        let url = window.location.href;
        if (url.endsWith(':5173/')) url = url.replace(':5173/',':8000/')
        url += 'api/hello';
        console.log({url});
        const resp = await fetch(url);
        if (resp.ok){
            response = await resp.json();
        }
    }

    onMount(load);
</script>


{#if response}
<h2>Response from API:</h2>
<pre>
    <code>
        {JSON.stringify(response,null,2)}
    </code>
</pre>
{:else}
<div>Hello?</div>
{/if}