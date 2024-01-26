<template>
    <div class="chart-element-container">
        <div class="top-container">
            <h2 class="bar-title">
                {{ data.title }}
            </h2>
            
            <div class="multiselect-container">
                <p class="multiselect-legend">type</p>
                <Multiselect 
                    class="multiselect-scope"
                    v-model="selectedChartType"
                    :allow-empty="false"
                    placeholder="Zone"
                    :multiple="false"
                    :show-labels="false"
                    :hide-selected="true"
                    :options="['bar', 'polarArea', 'doughnut', 'hbar']">
                </Multiselect>  
            </div>

            <!-- Selecteur d'échelle -->
            <div class="multiselect-container">
                <p v-if="data.hasZones" class="multiselect-legend">échelle</p>
                <Multiselect 
                    v-if="data.hasZones"
                    class="multiselect-scope"
                    v-model="selected"
                    :allow-empty="false"
                    placeholder="Zone"
                    :multiple="false"
                    :show-labels="false"
                    :hide-selected="true"
                    :options="options">
                </Multiselect>  
            </div>
        </div>
    
        <button 
            v-if="this.data.hasZones"
            v-for="dataset in selectedData.chartData.datasets" 
            v-on:click="dataset.visible = !dataset.visible"
            :class=" {showdataset:dataset.visible, hidedataset:!dataset.visible }"
            class="zone-selector">
            {{ dataset.label }}
        </button>

        <div class="chart">
            <CustomChart 
                :chartData="selectedData.chartData"
                :chartType="selectedChartType" />
        </div>
    </div>
</template>
  
<script>
import CustomChart from './CustomChart.vue'
import Multiselect from 'vue-multiselect'

export default {
    name: 'ChartContainer',
    components: {
        CustomChart,
        Multiselect,
    },
    props: {
        data: Object,
        chartType: String,
    },
    data() {
        return {
            selectedChartType: this.chartType,
            selected:'Détaillée',
            options: ['Globale', 'Détaillée'],
        }
    },
    computed:{
        selectedData(){
            return this.selected=='Détaillée' ? this.data.detailedChartData : this.data.globalChartData
        },
    }
}
</script>


<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<style>
.chart-element-container {
    width: 100%;
    height: 100%;
}
.top-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.bar-title {
    font-size: 1em;
}

.multiselect-container {
    display: flex;
    flex-direction:row;
    align-items:center;
    font-size: 0.8rem;
}
.multiselect-legend {
    margin-right: 5%;
}
.multiselect,
.multiselect__input,
.multiselect__single {
    font-family: inherit;
    font-size: 0.8rem;
    touch-action: manipulation;
}

.zone-selector {
    margin: 2% 0.5% 0 0.5%;
    padding: 0.5% 2%;
    border:0;
    /* box-shadow: 0 1px 2px 0px #AAA; */;
    border-radius: 2px;
    color: #5598dd;
}

.showdataset {
    background-color: rgb(238,244,252);
}

.hidedataset {
    background-color: white;
    /* box-shadow: -2px -2px 1px 0 #AAA; */
    /* text-decoration: line-through; */
}

.chart {
    padding-top:2%;
    width: 100%;
    /* border: 1px solid black; */
    /* aspect-ratio: 1/0.5; */
    height: 80%;
    /* border: 1px solid #AAA; */
}

</style>