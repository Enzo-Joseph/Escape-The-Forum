import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', {
  state: () => ({ 
    loaded: false,
    error: null,

    cardsData:{},
    chartsData:{}, 

    allData: {
      title: 'data.json',
      data: null,
    },
  }),
  
  actions:{ // methods
    async getData(){
        this.loaded = false;
        var url = 'http://localhost:5005/dashboard_data/'
        axios.get(url).then((res) => {
          
          
          this.allData.data = res.data['json_data']; 
          this.cardsData = res.data['cards'];
          this.chartsData = res.data['charts'];
          this.loaded = true;

          console.log("data loaded");
          
        }).catch((error) => {
            console.error(error);
            this.error = error;
        });
    },
    downloadData(){
        const jsonData = JSON.stringify(this.allData.data);
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.download = this.allData.title;

        link.click();

        URL.revokeObjectURL(url);
    },
  }
})
