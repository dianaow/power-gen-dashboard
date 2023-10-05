<script>
  export let legendData;
  export let title;
  export let clicked;
</script>

<style>
  .legend-container {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
  }

  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
    margin-left: 20px;
    font-size: 0.9em;
    min-width: 200px;
  }

  .color-circle {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    margin-right: 8px;
  }
</style>

{#if title}
  <h3 style="margin: 5px 20px;">{title}</h3>
{/if}
<div class='legend-container'>
  {#each legendData as { color, text }}
    <div 
      class="legend-item"
      cursor='pointer'
      on:click={(event) => {
        event.stopImmediatePropagation();
        clicked = text
      }}
      on:dblclick={(event) => {
        event.stopImmediatePropagation();
        clicked = null
      }}
    >
      <div class="color-circle" style="background-color: {color}"></div>
      <span>{text}</span>
    </div>
  {/each}
</div>
