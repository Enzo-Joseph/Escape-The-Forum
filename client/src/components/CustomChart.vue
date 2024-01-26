<template>
    <div class="bar-chart inner-chart">
      <Bar
        v-if="(chartType==='bar')"
        :data="barData"
        :options="barOptions">
      </Bar>
    </div>

    <div class="bar-chart inner-chart">
      <Bar
        v-if="(chartType==='hbar')"
        :data="barData"
        :options="hBarOptions">
      </Bar>
    </div>

    <div class="doughnut-chart inner-chart">
      <Doughnut
        v-if="chartType==='doughnut'"
        :data="doughnutData"
        :options="doughnutOptions">
    </Doughnut>
    </div>

    <div class="polar-chart inner-chart">
      <PolarArea
        v-if="chartType==='polarArea'"
        :data="polarAreaData"
        :options="polarAreaOptions">
    </PolarArea>
    </div>
 </template>

 <script>
import { Bar, Doughnut, PolarArea} from 'vue-chartjs'
import 'chart.js/auto'

export default {
name: 'CustomChart',
components:{
  Bar,
  Doughnut,
  PolarArea,
},
props:{
  id:null,
  chartType:null,
  chartData:null,
},
computed: {
  barData(){
    
    var labels = [];
    var datasets = [];
    var nbRiddlesVisible = 0;
    
    for (let i= 0; i < this.chartData.datasets.length; i++) {
      if (this.chartData.datasets[i].visible) {
        // We need to fill the data with 0s to match the number of labels
        var temp = new Array(nbRiddlesVisible).fill(0);
        var tempDataset = {...this.chartData.datasets[i]}; // clone
        tempDataset.data = temp.concat(tempDataset.data);
        datasets.push(tempDataset);                    
        
        
        labels = labels.concat(this.chartData.datasets[i].labels);
          
        nbRiddlesVisible += this.chartData.datasets[i].data.length;
      }
    }
    return {
      labels: labels,
      datasets: datasets
    }
  },
  barOptions() {
    return {
      plugins: {
          legend: {
              display: false
          },
          ticks:{
              display: true
          }
      },
      responsive: true,
      scales: {
          x: {
              stacked: true,
              display:true,
          },                    
      },       
    }
  },
  hBarOptions(){
    return {
      indexAxis: 'y',
      plugins: {
          legend: {
              display: false
          },
          ticks:{
              display: true
          }
      },
      responsive: true,
      scales: {
          x: {
              stacked: true,
              display:true,
          },                    
      },       
    }
  },
  polarAreaData(){
    var labels = [];
      var datasets = [{
        data:[],
        backgroundColor:[],
      }];
      for (let i= 0; i < this.chartData.datasets.length; i++) {
          if (this.chartData.datasets[i].visible) {
            labels = labels.concat(this.chartData.datasets[i].labels);
            for (let j = 0; j < this.chartData.datasets[i].data.length; j++) {
              datasets[0].data.push(this.chartData.datasets[i].data[j]);
              datasets[0].backgroundColor.push(this.chartData.datasets[i].backgroundColor);
            }
          }
      }
      return {
          labels: labels,
          datasets: datasets
      }
  },
  polarAreaOptions() {
    return {
      plugins: {
          legend: {
              display: false
          },
          ticks:{
              display: true
          }
      },
      responsive: true,
      scales: {
          x: {
              stacked: true,
              display:false,
          },                    
      },       
    }
  },
  doughnutData(){
    var labels = [];
      var datasets = [{
        data:[],
        backgroundColor:[],
      }];
      for (let i= 0; i < this.chartData.datasets.length; i++) {
          if (this.chartData.datasets[i].visible) {
            labels = labels.concat(this.chartData.datasets[i].labels);
            datasets[0].data = datasets[0].data.concat(this.chartData.datasets[i].data);
            
            for (let j = 0; j < this.chartData.datasets[i].data.length; j++) {
              datasets[0].backgroundColor.push(this.chartData.datasets[i].backgroundColor);
            }
          }
      }
      return {
          labels: labels,
          datasets: datasets
      }
  },
  doughnutOptions() {
    return {
      plugins: {
          legend: {
              display: false
          },
          ticks:{
              display: true
          }
      },
      responsive: true,
      scales: {
          x: {
              stacked: true,
              display:false,
          },                    
      },       
    }
  },

},
}
</script>

<style scoped>

.inner-chart {
  width: 100%;
  /* height: 100%; */
  margin: auto;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  
}
.bar-chart {
  margin: auto;
  
}
.doughnut-chart {
  max-width:50%;
  /* margin: auto; */
  /* height:100%; */
}

.polar-chart {
  max-width:50%;
  margin: auto;
}
</style>