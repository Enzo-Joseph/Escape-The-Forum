<template>
        <div class="calendar-container">
            <vue-flatpickr
            v-model = "selectedDates"
            :config = "datePickerConfig"
            placeholder="Sélectionner les dates"
            class="calendar"
            ></vue-flatpickr>
        </div>
        </template>

<script>
    import VueFlatpickr from 'vue-flatpickr-component';
    import 'flatpickr/dist/flatpickr.css'; // Importer les styles Flatpickr
     
    export default {
        components: {
            VueFlatpickr,
        },
    
        data() {
            return {
                selectedDates: [], // tableau qui stocke les dates sélectionnées
    
                datePickerConfig: {
                    mode: 'range', // Permet de sélectionner une plage de dates
                },
    
            };
        },

        watch: {
            selectedDates: function() {
                if (this.selectedDates.includes('to')) {
                    var index = this.selectedDates.indexOf('to');
                    var start = this.selectedDates.substring(0, index - 1);
                    var end = this.selectedDates.substring(index + 3, this.selectedDates.length);
                    console.log(start, end);
                    this.$emit('datesUpdate', [start, end]);
                }
            }
        }   
    
    };

</script>

<style>
.calendar-container {
    display: flex;
    flex-direction: row;
}

.calendar {
    border:none;
    padding: 7%;
    border-radius: 4px;
}

</style>