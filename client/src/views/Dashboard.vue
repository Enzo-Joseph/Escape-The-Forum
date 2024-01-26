<template >
    <p v-if="!this.store.loaded && !this.store.error">Loading...</p>
    <p v-if="this.store.error">{{ this.store.error }}</p>
    <body v-if="this.store.loaded">

      <header class="header">
        <h1 class="title">Escape The Forum</h1>

        <button class="button" @click="this.store.downloadData()">Télécharger</button>

      </header>
      
      <main class="main-container">

        <!-- Cards -->
        <div class="cards">
          <Card 
            v-for="cardData in this.store.cardsData"
            class="element card" 
            :title="cardData['title']"
            :text="cardData['text']"/>
        </div>

        <!-- Charts -->
        <div class="charts-container">
            <ChartContainer 
              v-for="chartData in this.store.chartsData"
              class="element chart-container"
              :chartType="chartData['chartType']"
              :data="chartData"/>
        </div>
    </main>
  </body>
</template>

<script>
import ChartContainer from '../components/ChartContainer.vue'
import Calendar from '../components/Calendar.vue'
import Card from '../components/Card.vue'
import Multiselect from 'vue-multiselect'
import { useCounterStore } from '@/stores/counter'


export default {
components: {
    ChartContainer,
    Card,
    Multiselect,
    Calendar
},
data() {
  return {
    store: useCounterStore(),
  }
}
};
</script>

<style>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: var(--spacing);
  height:20%;

}

.multiselect__single {
  white-space: nowrap;
  overflow: hidden; 
}


.center-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width:40%;
  height: 100%;
}

.title {
  font-size: 2rem;
  text-align: left;
}

.main-container {
  display:flex;
  flex-direction: column;
  margin: var(--spacing);
  height:auto;
  /* border:1px solid #CCC; */
}

.selector {
  width: 50%;
  margin: 0;
}

.button {
  cursor: pointer;
  color: white;
  background-color: #6363C8;
  border-radius: 5px;
  padding: 0.5% 2%;
  height: 100%;
}

.element {
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 1px 5px 0px #CCC;
}

.cards {
  display:grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr;
  gap: var(--spacing);
  height: 5%;
  margin-top :var(--spacing);
}

.card {
  padding: 2%;
  text-align: center
}

.charts-container {
  display: grid;
  width: 100%;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  margin-top: var(--spacing);
  gap: var(--spacing);
}

.chart-container {
  padding: 2%;
  width: 100%;
}

@media (max-width: 1024px) {
  .charts-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr 1fr 1fr;
  }
  
}

</style>