<script>
  import { onMount, afterUpdate } from 'svelte';
  import { sum } from 'd3-array';
  import { scaleOrdinal, scaleLinear, scaleTime } from "d3-scale";
  import { area, stack } from "d3-shape";
  import AxisX from "./AxisX.svelte";
  import AxisY from "./AxisY.svelte";
  import Legend from "./Legend.svelte";
  import HoverEvents from "./HoverEvents.svelte";
  import Tooltip from "./Tooltip.svelte";
  import { fade } from "svelte/transition";
  // import { tweened } from "svelte/store";
  // import {cubicOut} from 'svelte/easing';
  // import { interpolateString } from 'd3-interpolate';

  export let data, attribute
  
  const renewables = ['Wind onshore', 'Natural Gas', 'Biomass', 'Wind offshore', 'Nuclear', 'Solar', 'Run-of-River Hydro', 'Pumped storage generation', 'Other renewables', 'Dam Hydro', 'Geothermal']
  const non_renewables = ['Lignite', 'Hard Coal', 'Other fossil fuel', 'Oil',  'Non-renewable waste']
  
  const colorScale = scaleOrdinal()
    .domain(non_renewables.concat(renewables)) 
    .range(['darkslategray', 'dimgray', 'lightgray', 'gold', 'magenta', 'blue', 'lawngreen', 'saddlebrown', 'aqua', 'purple', 'yellow', 'teal', 'darkorange', 'red', 'dodgerblue', 'pink'])

  const margin = { top: 40, right: 30, bottom: 30, left: 60 };
  let div
  let height = 520;
  let width = 600;

  let innerHeight = height - margin.top - margin.bottom;
  let innerWidth = width - margin.left - margin.right;

  $: clickedItem = null
  $: hoveredDate = null
  $: xPos = 0

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

  $: stackKeys = Object.keys(data[0]).filter(d => d !== 'date_id' && d !== 'region').sort()

  $: legendData = stackKeys.map(d => {
    return {
      color: colorScale(d),
      text: d,
      total: sum(data.map(el => el[d]))
    }
  })

  $: legendData.sort((a,b) => b.total - a.total)

  $: stackKeysSorted = legendData.map(d => d.text)

  $: legendData_renewable = legendData.filter(d => renewables.indexOf(d.text) !== -1)
  $: legendData_nonrenewable = legendData.filter(d => non_renewables.indexOf(d.text) !== -1)

  $: yScale = scaleLinear()
    .domain([0, attribute === 'value' ? 2000 : 1])  //in Gwh
    .range([innerHeight, 0]);

  $: xScale = scaleTime()
    .domain([new Date(data[0]['date_id']), new Date(data[data.length-1]['date_id'])])
    .range([0, innerWidth]);

  $: stackedData = stack()
    .keys(stackKeysSorted)(data)

  $: areaFunc = area()
    .x(d => xScale(new Date(d.data.date_id)))
    .y0(d => yScale(d[0]))
    .y1(d => yScale(d[1]));

  $: hoveredData = hoveredDate ? data.filter(d => d.date_id >= hoveredDate)[0] : null

  // let line = tweened(0, {
	// 	duration: 400,
	// 	easing: cubicOut,
  //   interpolate: interpolateString
	// });

  // $: tweenAreaFunc = (d) => line.set(areaFunc(d));
</script>

<div class="chart-container" bind:this={div}>
  <svg
    {width}
    {height}
  >
    <g transform="translate({margin.left} {margin.top})">
      <AxisX
        height={innerHeight}
        interval="Day"
        ticks={xScale.ticks(20)}
        {xScale}
      />
      <AxisY
        width={innerWidth} 
        {yScale} 
        ticks={yScale.ticks(6)}
        title='Power Generation Value (in GWh)'
      />
      {#each stackedData as d, index}
        <path
          transition:fade
          d={areaFunc(d)}
          stroke={colorScale(d.key)}
          fill={colorScale(d.key)}
          stroke-width="1"
          opacity={clickedItem
          ? clickedItem === d.key 
            ? 1
            : 0.2
          : 1}
        />
      {/each}
      <HoverEvents
        width={innerWidth}
        height={innerHeight}
        {xScale}
        {margin}
        bind:hoveredDate
        bind:xPos
      />
    </g>
  </svg>
  {#if hoveredDate && hoveredData}
    <Tooltip data={hoveredData} x={xPos} {colorScale} {width} />
  {/if}
</div>
<div><span style='font-size: 0.7em; margin-left: 20px;'>Click on a legend item to highlight the fuel source. Double-click on any item to un-highlight.</span></div>
<Legend legendData={legendData_renewable} title="Renewables" bind:clicked={clickedItem}/>
<Legend legendData={legendData_nonrenewable} title="Non-renewables" bind:clicked={clickedItem}/>

<style>
  .chart-container {
    position: relative;
    width: 100%;
    height: 72%;
  }
</style>