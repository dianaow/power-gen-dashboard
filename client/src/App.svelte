<script>
  import { onMount } from 'svelte';
  import StackedAreaChart from './lib/StackedAreaChart.svelte';
  import LineChart from './lib/LineChart.svelte';
  
  let data = {}
  let dailyData = []
  let monthlyData = []
  let options = []
  let selectedOption = 'Germany'
  let selectedAttr = 'value'

  async function getData() {
    try {
      const response = await fetch('/data', {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();

      if (result) {
        data = {
          daily: JSON.parse(result.type.daily), 
          monthly: JSON.parse(result.categorized.monthly), 
          perc_daily: JSON.parse(result.type.perc_daily)
        }
        options = [...new Set(data.monthly.map(d => d['region']))]

        // filter data by default country 
        dailyData = data.daily.filter(d => d['region'] === selectedOption)
        monthlyData = data.monthly.filter(d => d['region'] === selectedOption)
        monthlyData = [monthlyData[0], monthlyData[monthlyData.length-1]]

      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  onMount(async() => {
    await getData();
  })

  function handleOptionChange(event) {
    selectedOption = event.target.value;
    
    // filter data by selected country from dropdown menu
    if(selectedAttr === 'perc'){
      dailyData = data.perc_daily.filter(d => d['region'] === selectedOption)
    } else if(selectedAttr === 'value'){
      dailyData = data.daily.filter(d => d['region'] === selectedOption)
    }
    monthlyData = data.monthly.filter(d => d['region'] === selectedOption)
    monthlyData = [monthlyData[0], monthlyData[monthlyData.length-1]]
  }

  function handleTabClick(value){
    selectedAttr = value;
    if(selectedAttr === 'perc'){
      dailyData = data.perc_daily.filter(d => d['region'] === selectedOption)
    } else if(selectedAttr === 'value'){
      dailyData = data.daily.filter(d => d['region'] === selectedOption)
    }
  }
</script>

<main>
  {#if monthlyData.length > 0}
  <div class='header'>
    <h2 style="margin-left: 20px;">Power generation for different fuel sources </h2>
    <h2 style="margin-left: 20px;">from October to December 2022 in </h2>
    <div class='dropdown'>
      <select value={selectedOption} on:change={handleOptionChange}>
        {#each options as option}
        <option value={option}>{option}</option>
        {/each}
      </select>
      <span class="caret"></span>
    </div>
    <div class="buttons">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div
        class={selectedAttr === 'value' ? 'active' : ''}
        on:click={() => handleTabClick('value')}
      >
        Absolute values
      </div>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div
        class={selectedAttr === 'perc' ? 'active' : ''}
        on:click={() => handleTabClick('perc')}
      >
        % of the total generation
      </div>
    </div>
  </div>
  <div class="wrapper">
    <div class='left'>
      {#if dailyData.length > 0}
        <StackedAreaChart data={dailyData} attribute={selectedAttr}/>
      {/if}
    </div>
    <div class='right'>
      {#if monthlyData.length > 0}
        <LineChart data={monthlyData} />
      {/if}
    </div>
  </div>
  {:else}
  <div class="wrapper">Loading...</div>
  {/if}
</main>

<style>
  .header {
    display: flex;
    width: 100vw;
  }

  .wrapper {
    display: flex;
    width: 100vw;
    height: calc(100vh - 80px);
  }

  .left {
    width: 80%;
    height: 100%;
  }

  .right {
    width: 20%;
    height: 100%;
  }

  .buttons {
    display: flex;
    margin: 0 20px;
    width: auto;
    height: 70px;
  }

  .buttons div {
    padding: 8px 12px;
    cursor: pointer;
    border-bottom: none;
    background-color: #d3d3d3;
    color: #696969;
    transition: background-color 0.3s ease;
    border-radius: 10px;
    margin: 10px;
  }
  
  .buttons div:hover {
    background-color: #C0C0C0;
  }
  
  .buttons div.active {
    background-color: #000;
    color: #fff;
  }


  .dropdown {
    position: relative;
    display: inline-block;
    display: flex;
    padding: 8px 12px;
    cursor: pointer;
    background-color: #fff;
    color: black;
    border: 2px solid black;
    border-radius: 10px;
    margin: 10px 20px;
  } 
  
  .dropdown select {
    height: 100%;
    font-family: Avenir;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-color: transparent;
    border: none;
    outline: none;
    text-align: center;
    font-size: 1.5em;
    margin: 0px 16px;
  }

  .caret {
    position: absolute;
    top: 50%;
    right: 8px;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 5px 5px 0 5px;
    border-color: black transparent transparent transparent;
    pointer-events: none;
    margin-left: 8px
  }
</style>

