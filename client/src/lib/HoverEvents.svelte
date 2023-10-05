<script>
  export let xScale;
  export let margin;
  export let width;
  export let height;
  export let hoveredDate;
  export let xPos;

  const handleMousemove = function (e) {
      hoveredDate = Math.round(xScale.invert(e.offsetX - margin.left))
      xPos = e.offsetX - margin.left
  };

  const handleMouseleave = function () {
      hoveredDate = null
      xPos = 0
  };
</script>

<rect
  class="hover-listener"
  fill="transparent"
  {width}
  {height}
  on:mousemove={handleMousemove}
  on:mouseleave={handleMouseleave}
/>

{#if hoveredDate}
  <line
    x1={xScale(hoveredDate)}
    x2={xScale(hoveredDate)}
    y1={0}
    y2={height}
    stroke="darkgrey"
    stroke-dasharray="2, 2"
    pointer-events="none"
  />
{/if}

<style>
  rect {
      cursor: crosshair;
  }
</style>
