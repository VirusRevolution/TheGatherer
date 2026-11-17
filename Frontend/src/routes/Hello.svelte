<script>
    import { onMount } from 'svelte';
	import { get } from '../lib/api.svelte';

    let response = $state(null);

    async function load(){
        const resp = await get('hello');
        if (resp.ok) response = await resp.json();
    }

    window.setTimeout(load,1000);
</script>

{#if response}
<p>Received response from API: {response.message}</p>
{:else}
<div>Contacting the backend…</div>
{/if}