<script>
  import { onMount, afterUpdate } from 'svelte'
  import { groups } from 'd3-array'
  import { scaleLinear, scaleTime } from 'd3-scale'
  import { line } from 'd3-shape'
  import AxisX from './AxisX.svelte'
  import AxisY from './AxisY.svelte'

  export let data

  const margin = { top: 40, right: 30, bottom: 30, left: 60 };
  let div
  let width = 200
  let height = 520
  let innerHeight = height - margin.top - margin.bottom
  let innerWidth = width - margin.left - margin.right

  // data = [{date_id: 'oct', 'renewable': 100}, {date_id: 'oct', 'non-renewable': 10}, {date_id: 'dec', 'renewable': 100}, {date_id: 'dec', 'non-renewable': 10}]
  // newData = {date_id: 'oct', type: 'renewable', value: 100}
  
  onMount(() => {
    updateChartSize()
  })

  afterUpdate(() => {
    updateChartSize()
  })

  function updateChartSize() {
    if (div) {
      width = div.clientWidth
      innerWidth = width - margin.left - margin.right
      height = div.clientHeight
      innerHeight = height - margin.top - margin.bottom
    }
  }

  $: newData = data.reduce((result, item) => {
    // Extract the common properties from the item
    const { date_id } = item;

    // Check if the item has a 'renewable' property and add it to the result
    if ('renewable' in item) {
      result.push({ date_id, type: 'renewable', value: item.renewable });
    }

    // Check if the item has a 'non-renewable' property and add it to the result
    if ('non-renewable' in item) {
      result.push({ date_id, type: 'non-renewable', value: item['non-renewable'] });
    }

    return result;
  }, []);

  $: lineData = groups(
    newData,
    d => d.type
  )

  $: yScale = scaleLinear()
      .domain([0, 50000])
      .range([innerHeight, 0]);

  $: xScale = scaleTime()
    .domain([new Date(data[0]['date_id']), new Date(data[data.length-1]['date_id'])])
    .range([0, innerWidth]);

  $: lineGenerator = line()
    .x((d, i) => xScale(new Date(d.date_id)))
    .y((d) => yScale(d.value))
</script>

<div class="chart-container" bind:this={div}>
  <svg {width} {height}>
    <g transform="translate({margin.left} {margin.top})">
      <AxisX
        height={innerHeight}
        {xScale}
        interval="Month"
        ticks={data.map((d) => d.date_id)}
      />
      <AxisY 
        width={innerWidth} 
        {yScale} 
        ticks={yScale.ticks(6)}
        title='Power Generation Value (in GWh)'
      />
      {#each lineData as d}
        <path
          d={lineGenerator(d[1])} 
          stroke="black"
          fill="transparent" 
          stroke-width="3" 
        />
        <circle
          cx={xScale(d[1][0].date_id)}
          cy={yScale(d[1][0].value)}
          r={5}
          fill="black"
        />
        <circle
          cx={xScale(d[1][1].date_id)}
          cy={yScale(d[1][1].value)}
          r={5}
          fill="black"
        />
        <text
          x={xScale(d[1][1].date_id) - 20}
          y={yScale(d[1][1].value) - 10}
          fill="black"
          text-anchor="end"
        >
          {d[0]}
        </text>
      {/each}
    </g>
  </svg>
</div>

<style>
  .chart-container {
    width: 100%;
    height: 72%;
  }
</style>