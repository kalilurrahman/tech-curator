<script>
  import { onMount } from 'svelte';
  import NewsCard from '$lib/components/NewsCard.svelte';
  import { fade } from 'svelte/transition';
  
  let stories = [];
  let loading = true;
  let refreshing = false;
  let searchQuery = '';
  let searchTimeout;
  const API_URL = 'http://localhost:8000'; 

  async function fetchFeed(query = '') {
    loading = true;
    try {
      const url = query ? `${API_URL}/feed?q=${encodeURIComponent(query)}` : `${API_URL}/feed`;
      const res = await fetch(url);
      if(res.ok) stories = await res.json();
    } catch (e) {
      console.error("Feed error:", e);
    } finally {
      loading = false;
      refreshing = false;
    }
  }

  onMount(() => {
    fetchFeed();
  });

  function handleSwipe(event) {
    const { id } = event.detail;
    stories = stories.filter(s => s.cluster_id !== id);
  }

  async function handleRefresh() {
    refreshing = true;
    try {
      await fetch(`${API_URL}/refresh`, { method: 'POST' });
      // Give the backend a moment to process (since it's async background task)
      // Ideally we'd poll, but for now a simple delay is okay or just re-fetching
      await new Promise(r => setTimeout(r, 2000));
      await fetchFeed(searchQuery);
    } catch (e) {
      console.error("Refresh error:", e);
      refreshing = false;
    }
  }

  function handleSearchInput(e) {
    const value = e.target.value;
    searchQuery = value;
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      fetchFeed(value);
    }, 500);
  }
</script>

<main class="w-screen h-screen flex flex-col items-center justify-center relative bg-black overflow-hidden">

  <!-- Header / Search Bar -->
  <div class="absolute top-0 w-full max-w-md p-4 z-50 flex gap-2">
    <input
      type="text"
      placeholder="Search stories..."
      class="flex-1 bg-gray-900 border border-gray-800 rounded-full px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
      on:input={handleSearchInput}
      value={searchQuery}
    />
    <button
      class="bg-gray-900 border border-gray-800 text-white rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-800 transition-colors"
      on:click={handleRefresh}
      disabled={refreshing}
      title="Refresh Feed"
    >
      <span class:animate-spin={refreshing}>⟳</span>
    </button>
  </div>

  {#if loading && !refreshing && stories.length === 0}
    <div class="animate-pulse text-gray-500">Curating...</div>
  {:else if stories.length === 0}
    <div class="text-center" in:fade>
      <h1 class="text-2xl font-bold mb-2 text-white">All Caught Up</h1>
      <p class="text-gray-500 mb-6">{searchQuery ? `No results for "${searchQuery}"` : "Check back later for more updates."}</p>
      <button
        class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full transition-colors font-bold"
        on:click={handleRefresh}
        disabled={refreshing}
      >
        {refreshing ? 'Refreshing...' : 'Refresh Feed'}
      </button>
    </div>
  {:else}
    <div class="relative w-full h-full max-w-md flex items-center justify-center pt-16 pb-4">
      {#each stories.slice(0, 3).reverse() as story, i (story.cluster_id)}
        <NewsCard {story} index={i} on:swipe={handleSwipe} />
      {/each}
    </div>
  {/if}
</main>
