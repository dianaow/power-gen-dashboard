<script>
  export let width;
  export let yScale;
  export let title;
  export let ticks;

  const TICK_LENGTH = 10
</script>

<g class='axis y'>
  {#each ticks as tick, index}
    <g 
      class='tick' 
      transform="translate(0, {yScale(tick)})"
    >
      <line 
        x1={-TICK_LENGTH} 
        x2={width} 
        y1={0} 
        y2={0} 
        stroke={index === 0 ? '#8f8f8f' : '#e5e7eb'} 
      /> 
      <text 
        x={-TICK_LENGTH-30} 
        dominant-baseline="middle"
      >
        {tick}
      </text>
    </g>
  {/each}
  <text 
    class="axis-title" 
    x={-TICK_LENGTH-30} 
    y={-36} 
    dy="4" 
    dominant-baseline="hanging" 
    text-anchor="start"
  >
    {title}
  </text>
</g>

<style>
  text {
      font-size: 0.7rem;
      fill: black;
  }
</style>
