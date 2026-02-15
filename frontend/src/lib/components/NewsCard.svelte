<script>
  import { createEventDispatcher } from 'svelte';
  export let story;
  export let index;
  
  const dispatch = createEventDispatcher();
  let x = 0;
  let isDragging = false;
  let startX = 0;
  let isExpanded = false;

  function start(cx) { if(!isExpanded) { isDragging = true; startX = cx; } }
  function move(cx) { if(isDragging) x = cx - startX; }
  function end() {
    isDragging = false;
    if(Math.abs(x) > 100) {
      dispatch('swipe', { direction: x>0?'right':'left', id: story.cluster_id });
      x = x>0 ? 1000 : -1000;
    } else {
      x = 0;
    }
  }
</script>

<div 
  class="absolute w-[90%] h-[70%] bg-[#171717] rounded-3xl border border-gray-800 overflow-hidden shadow-2xl transition-transform"
  style="
    z-index: {100-index}; 
    transform: translate({x}px, {isExpanded?0:index*10}px) rotate({x*0.05}deg) scale({1-index*0.05});
    opacity: {1-index*0.2};
  "
  on:touchstart={e=>start(e.touches[0].clientX)}
  on:touchmove={e=>move(e.touches[0].clientX)}
  on:touchend={end}
  on:mousedown={e=>start(e.clientX)}
  on:mousemove={e=>move(e.clientX)}
  on:mouseup={end}
  on:click={() => { if(x===0) isExpanded = !isExpanded; }}
>
  <div class="p-6 h-full flex flex-col justify-between select-none">
    {#if !isExpanded}
      <div>
        <span class="text-xs font-bold text-blue-500 tracking-widest">{story.topic_label}</span>
        <h2 class="text-xl font-bold mt-4 leading-tight">{story.primary_article.title}</h2>
        <p class="mt-4 text-gray-400 text-lg leading-relaxed">{story.primary_article.summary}</p>
      </div>
      <div class="border-t border-gray-800 pt-4 flex justify-between text-xs text-gray-500">
        <span>{story.primary_article.source}</span>
        {#if story.related_articles.length > 0}
          <span class="bg-gray-800 px-2 py-1 rounded text-white">+{story.related_articles.length} Sources</span>
        {/if}
      </div>
    {:else}
      <div class="h-full flex flex-col">
        <h3 class="text-blue-500 font-bold mb-4 uppercase text-sm">Cluster Coverage</h3>
        <div class="flex-1 overflow-y-auto space-y-4">
          <a href={story.primary_article.url} target="_blank" class="block">
            <div class="text-white font-bold text-sm">{story.primary_article.source} <span class="bg-blue-600 text-[10px] px-1 rounded ml-2">PRIMARY</span></div>
            <div class="text-gray-400 text-xs mt-1">{story.primary_article.title}</div>
          </a>
          {#each story.related_articles as art}
            <a href={art.url} target="_blank" class="block border-t border-gray-800 pt-3">
              <div class="text-gray-300 font-bold text-sm">{art.source}</div>
              <div class="text-gray-500 text-xs mt-1">{art.title}</div>
            </a>
          {/each}
        </div>
        <button class="w-full py-3 mt-4 bg-gray-800 rounded-lg font-bold" on:click|stopPropagation={()=>isExpanded=false}>Close</button>
      </div>
    {/if}
  </div>
</div>
