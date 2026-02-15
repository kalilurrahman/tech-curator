<script>
  import { onMount } from 'svelte';
  import NewsCard from '$lib/components/NewsCard.svelte';
  
  let stories = [];
  let loading = true;
  const API_URL = 'http://localhost:8000'; 

  onMount(async () => {
    try {
      const res = await fetch(`${API_URL}/feed`);
      if(res.ok) stories = await res.json();
    } catch (e) {
      console.error("Feed error:", e);
    } finally {
      loading = false;
    }
  });

  function handleSwipe(event) {
    const { id } = event.detail;
    stories = stories.filter(s => s.cluster_id !== id);
  }
</script>

<main class="w-screen h-screen flex items-center justify-center relative bg-black">
  {#if loading}
    <div class="animate-pulse text-gray-500">Curating...</div>
  {:else if stories.length === 0}
    <div class="text-center">
      <h1 class="text-2xl font-bold mb-2">All Caught Up</h1>
      <button class="px-6 py-2 bg-gray-800 rounded-full" on:click={() => location.reload()}>Refresh</button>
    </div>
  {:else}
    <div class="relative w-full h-full max-w-md flex items-center justify-center">
      {#each stories.slice(0, 3).reverse() as story, i (story.cluster_id)}
        <NewsCard {story} index={i} on:swipe={handleSwipe} />
      {/each}
    </div>
  {/if}
</main>
