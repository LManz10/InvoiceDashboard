<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Bar,Pie } from 'vue-chartjs'
import { useRoute } from 'vue-router'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import {getAnalysisData, filterAndAnalyze} from '../services/api'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)
const chartData = ref<any>(null)
const pieChartData = ref<any>(null)

const focusNodePieChartData = ref<any>(null)
const resultPathPieChartData = ref<any>(null)
const severityPieChartData = ref<any>(null)
const sourceConstraintComponentPieChartData = ref<any>(null)

const isLoading = ref(true)
const route = useRoute()


const runId = route.params.runId as string
const error = ref<string | null>(null)
const dashboardData = ref<any>(null)

const totalViolationCount = ref<number | null>(null)
const anzahlAffectedSuppliers = ref<number | null>(null)
const focusNodeVerteilung = ref<number | null>(null)
const resultPathVerteilung = ref<number | null>(null)
const severityVerteilung = ref<number | null>(null)
const sourceConstraintComponentVerteilung = ref<number | null>(null)

const violationList = ref([]);

const resultPathFilterInput = ref(''); 
const focusNodeFilterInput = ref(''); 
const severityFilterInput = ref('');

const graphData = ref<string | null>(null);



  const chartFarben = [
    '#ff1346ff', 
    '#1d89d1ff', 
    '#f1c55cff',
    '#3cbdbdff',
    '#7a50cfff',
    '#d4873aff'  
];





onMounted(async () => {
  isLoading.value = true
  error.value = null
  
  try {

    const data = await getAnalysisData(runId)

    totalViolationCount.value = data.violation_count
    violationList.value = data.list_of_violations || [];
    graphData.value = data.graph;
    anzahlAffectedSuppliers.value= data.anzahl_betroffener_suppliers;

    focusNodeVerteilung.value = data.focus_node_verteilung;
    resultPathVerteilung.value = data.result_path_verteilung;
    severityVerteilung.value = data.severity_verteilung;
    sourceConstraintComponentVerteilung.value = data.source_constraint_component_verteilung;


    console.log('jooooooooooooooooooooo')
    console.log(sourceConstraintComponentVerteilung.value)
    console.log('jooooooooooooooooooooo')



  
    focusNodePieChartData.value = generateChartData(focusNodeVerteilung.value)
    resultPathPieChartData.value = generateChartData(resultPathVerteilung.value)
    severityPieChartData.value = generateChartData(severityVerteilung.value)
    sourceConstraintComponentPieChartData.value = generateChartData(sourceConstraintComponentVerteilung.value)




  } catch (e: any) {
    error.value = e?.response?.data?.detail || e?.message || 'Konnte Daten nicht laden'
  } finally {
    isLoading.value = false
  }
})



function generateChartData(dynamicData) {

    const backgroundColors = [];
    const labels = [];
    const dataValues = [];

    dynamicData.forEach((item, index) => {
        labels.push(item.key);
        dataValues.push(parseFloat(item.value)); 
        
        const colorIndex = index % chartFarben.length;
        backgroundColors.push(chartFarben[colorIndex]);
    });

    return {
        labels: labels,
        datasets: [{
            backgroundColor: backgroundColors,
            data: dataValues,
            borderColor: '#FFFFFF', 
            borderWidth: 2
        }]
    };
}


// 5. Lifecycle Hook: Daten beim Erstellen der Komponente laden



function kürzen(uri: string) {
    if (!uri) return 'N/A';

    const hashIndex = uri.lastIndexOf('#');
    const slashIndex = uri.lastIndexOf('/');
    const index = Math.max(hashIndex, slashIndex);

    return index > 0 ? uri.substring(index + 1) : uri;
}



async function filtern(){

  const pathValue = resultPathFilterInput.value.trim();
  const focusValue = focusNodeFilterInput.value.trim();
  const severityValue = severityFilterInput.value.trim();
  let ausgewählterFilter: string | null = null;
  let filterWert: string | null = null;

  if (pathValue.length > 0){
    ausgewählterFilter = "resultPath";
    filterWert = pathValue;
    if(focusValue.length > 0 || severityValue.length > 0 ){
      return;
    }
  }
    
    
  if (focusValue.length > 0){
     ausgewählterFilter = "focusNode";
    filterWert = focusValue;


    if(severityValue.length > 0 ){
      return;
    }
      
  }
     
  
  if (severityValue.length > 0){
      filterWert = severityValue;
      ausgewählterFilter = "severity"; 
  }



  const input = {
    "ausgewählterFilter": ausgewählterFilter, 
    "filterValue": filterWert,
    "graph": graphData.value
  }

  const filterData = await filterAndAnalyze(input);
} 


</script>

<template>

  <header>

    <div class = "überschrift">
      <h1>Invoice Dashboard </h1>
    </div>

  </header>


  <main>
      
    <div v-if="isLoading" class="status-message loading">
      Daten werden geladen... bitte warten...
    </div>
    
    <div v-else-if="error" class="status-message error">
       {{ error }}
    </div>
    
    <div v-else>
      <div class="anzeigeBoxContainer">

        <div class="anzeigeBox">
          <p class="title">Total Violations</p>
          <h3 class="value"><span>{{ totalViolationCount }}</span></h3>
        </div>

         <div class="anzeigeBox">
          <p class="title">Error Rate</p>
          <h3 class="value">23,7%</h3>

        </div> <div class="anzeigeBox">
          <p class="title">Affected Suppliers </p>
          <h3 class="value"><span>{{ anzahlAffectedSuppliers }}</span></h3>
        </div>

      </div>
        
      <div class="ChartBoxContainer">
    
        <div class="chart-container">
            <Pie :data="focusNodePieChartData"/>
        </div>
     
        <div class="chart-container">
            <Pie :data="resultPathPieChartData"/>
        </div>

      </div>

      <div class="ChartBoxContainer">
    
        <div class="chart-container">
            <Pie :data="severityPieChartData"/>
        </div>
     
        <div class="chart-container">
            <Pie :data="sourceConstraintComponentPieChartData"/>
        </div>

      </div>

      <div class = "FilterAußenContainer">


        <div class = "filterÜberschrift">
         <h2>Filter</h2>
        </div>

        
        <div class="FilterAuswahlContainer"> 
              
                <div class = "einzelnerFilter">
                  <h3>Typ of violation</h3>
                  <input type="text" class = "filterInput" v-model = "resultPathFilterInput">
                </div>

                <div class = "einzelnerFilter">
                  <h3>Supplier</h3>
                  <input type="text" class = "filterInput" v-model = "focusNodeFilterInput">

                </div>

                <div class = "einzelnerFilter">
                  <h3>Invoice Dashboard </h3>
                  <input type="text" class = "filterInput"  v-model = "severityFilterInput">
                </div>

                <div class = "einzelnerFilter">
                  <h3>Date</h3>
                  <input type="text" class = "filterInput">
                </div>
          </div>

          <button class = "filterButton" @click="filtern"> Jetzt Filtern </button>
      </div>

      



    </div>

<div class="scrollbareViolationListe">

    <div v-for="(violation, index) in violationList" :key="index" 
         class="violation-item-wrapper" 
         :class="`severity-${violation.severity.toLowerCase()}`"> 
        
        <div class="violation-detail-grid">
            
            <span class="grid-item severity-tag">
                {{ kürzen(violation.severity) }}
            </span>
            
            <span class="grid-item message-text">
                {{ violation.result_message }}
            </span>

            <span class="grid-item result-path">
                Pfad: {{ violation.result_path }}
            </span>
            
            <span class="grid-item focus-node">
                Knoten: {{ violation.focus_node }}
            </span>
        </div>
        
    </div>

    <p v-if="violationList.length === 0" class="no-violations">Keine kritischen Verstöße gefunden.</p>

</div>

  </main>


</template>

<style scoped>

html, body {
  margin: 0;
  padding: 0;
}

h1 {
  font-size:50px;
}

h3 {
    font-size:20px;
    display:grid;
    margin-left: auto;
    margin-right: auto;

}

h2 {

    font-size:35px;
    display:grid;
    margin-left: auto;
    margin-right: auto;

}



main {
  width: 100%;
  padding: 20px; 
  margin-top: 100px;
  background-color: #f0f0f0;
}


.dashboard-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.status-message {
  padding: 20px;
  margin: 20px 0;
  border-radius: 5px;
}

.loading {
  background-color: #e0f7fa;
  color: #00796b;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}



.überschrift {
  position: fixed;
  height: 100px; 
  background-color: #19B2FF;
  padding: 15px;
  border-radius: 8px;
  top: 0px;
  width: 100%;
  text-align: center;
  z-index: 1000;

}


/*Anzeige*/

.anzeigeBox {

    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    position: relative;
    background-color: #19B2FF
}

.anzeigeBoxContainer{
    display: grid;
    grid-template-columns: repeat(3, 1fr); 
    gap: 80px;
    margin-top:30px;
    width:60%;
    margin-left: auto;
    margin-right: auto;

}







/* Diagramme */


.ChartBoxContainer{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-top: 30px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}

.chart-container {
  height: 400px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;

  display: flex;
  flex-direction: column;  
  justify-content: center; 
  align-items: center;
  text-align: center; 
}





/* Filter */

.FilterAuswahlContainer {
  display:grid;
  grid-template-columns: repeat(4, 1fr); 
  width:75%;
  gap: 40px;
  margin-left: auto;
  margin-right: auto;
}

.FilterAußenContainer{
  background-color: white;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
  border-radius:5px;
}

.einzelnerFilter {
  background-color: #19B2FF;
  border-radius:5px;
}

.filterInput {
    display:grid;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10px;
    margin-top: 10px;
    padding: 10px;
    font-size: 16px;
    font-family: Arial;
    color: #333;
    border-radius: 6px; 
    border: 1px solid #ccc; 
    background-color: #fff;
    transition: all 0.3s ease;

}

.filterÜberschrift {
  display:grid;
  margin-left: auto;
  margin-right: auto;
}

.filterButton {
  display:grid;
  margin-left: auto;
  margin-right: auto;
  margin-top: 10px;
}






/*Liste*/
.scrollbareViolationListe {
    height: 400px; /* Hält die Liste scrollbar */
    overflow-y: scroll;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 0; /* Entferne Padding, um Platz zu sparen */
    background-color: #white;
    color: #black;
    margin-top: 30px;
}

.violation-item-wrapper {
    color: #black;
    border-bottom: 1px solid #333;
    padding: 10px;
}

.violation-detail-grid {
    display: grid;
    /*  4 Spalten,15% für Severity, 45% für Message, 20% pro Detail*/
    grid-template-columns: 100px 1.5fr 1fr 1fr; 
    gap: 15px; /* Abstand zwischen den Spalten */
    align-items: center;
    font-size: 0.9em;
    overflow-wrap: break-word;}

.severity-tag {
    font-weight: bold; 
    text-align: center;
    padding: 2px 5px;
    border-radius: 4px;
        overflow: hidden;
    text-overflow: ellipsis; 
}


.message-text {
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis; 
}

.result-path, .focus-node {
    color: #black; 
    font-size: 0.8em;
}

.no-violations {
    text-align: center;
    padding: 20px;
    color: #black;
}

</style>