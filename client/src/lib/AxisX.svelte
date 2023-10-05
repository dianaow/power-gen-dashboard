<script>
  export let height;
  export let xScale;
  export let interval;
  export let ticks;

  const TICK_LENGTH = 4
</script>

{#each ticks as tick, i}

{#if tick}
  <line
      x1={xScale(new Date(tick))}
      x2={xScale(new Date(tick))}
      y1={height}
      y2={height + TICK_LENGTH}
      stroke="#808080"
  />
  {#if interval === 'Day'}
      <text
          x={xScale(new Date(tick))}
          y={height + TICK_LENGTH}
          dy="6"
          dominant-baseline="hanging"
          text-anchor="middle"
      >
      { `${new Date(tick).toLocaleDateString('en-US', { day: '2-digit' })}/${new Date(tick).toLocaleDateString('en-US', { month: '2-digit' })}`}
  </text>
  {/if}
  {#if interval === 'Month'}
      <text
          x={xScale(tick)}
          y={height + TICK_LENGTH}
          dy="6"
          dominant-baseline="hanging"
          text-anchor="middle"
      >
          {new Date(tick).toString().split(' ')[1]}
      </text>
  {/if}
{/if}
{/each}

<style>
  text {
      font-size: 0.85rem;
      fill: black;
  }
</style>
