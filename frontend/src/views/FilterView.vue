<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Bar,Pie } from 'vue-chartjs'
import { useRoute, useRouter } from 'vue-router'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import {getAnalysisData, filterAndAnalyze, getFilterRun, callModellUpdatenFunction, callEdiAnzeigeBerechnenFunction} from '../services/api'
import infoCard from '../components/infoCard.vue'
import filterKomponente from '../components/filterKomponente.vue'

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import violationDetailModal from '../components/violationDetailModal.vue'


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)
const chartData = ref<any>(null)
const pieChartData = ref<any>(null)

const focusNodePieChartData = ref<any>(null)
const resultPathPieChartData = ref<any>(null)
const severityPieChartData = ref<any>(null)
const sourceConstraintComponentPieChartData = ref<any>(null)

const isLoading = ref(true)
const route = useRoute()

const router = useRouter();

const runId = route.params.runId as string
const originalReportID = ref("")
const error = ref<string | null>(null)
const dashboardData = ref<any>(null)

const totalViolationCount = ref<number | null>(null)
const anzahlAffectedSuppliers = ref<number | null>(null)
const focusNodeVerteilung = ref<number | null>(null)
const resultPathVerteilung = ref<number | null>(null)
const severityVerteilung = ref<number | null>(null)
const sourceConstraintComponentVerteilung = ref<number | null>(null)
const violationDetailViewAnzeige = ref(false);

const zwischenGraph = ref<string | null>(null);
const ediText = ref<string | null>(null);




const meistBetroffenerFocusNode = ref<number | null>(null)
const meistBetroffenerResultPath = ref<number | null>(null)
const meistBetroffenerSourceConstraint = ref<number | null>(null)

const violationList = ref([]);

const resultPathFilterInput = ref(''); 
const focusNodeFilterInput = ref(''); 
const severityFilterInput = ref('');

const graphData = ref<string | null>(null);


const focusNodeEntropy = ref<number | null>(null)
const resultPathEntropy = ref<number | null>(null)
const sourceConstraintComponentEntropy = ref<number | null>(null)


let aktuellerPath = null;
const detailViewAusgabeVariable = ref("")
const subjectAusgabeVariable = ref("")
const objectAusgabeVariable = ref("")

const attributes = ref([])
const shaclAttributes = ref([])
const violationMessage = ref("")



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
  
    const data = await getFilterRun(runId)

    console.log( "oid:" + originalReportID.value)

  try {


    const data = await getFilterRun(runId)
    originalReportID.value = data.originalReportID
    totalViolationCount.value = data.violation_count
    violationList.value = data.list_of_violations || [];
    graphData.value = data.graph;
    anzahlAffectedSuppliers.value= data.anzahl_betroffener_suppliers;

    focusNodeVerteilung.value = data.focus_node_verteilung;
    resultPathVerteilung.value = data.result_path_verteilung;
    severityVerteilung.value = data.severity_verteilung;
    sourceConstraintComponentVerteilung.value = data.source_constraint_component_verteilung;
    ediText.value = " ";
    zwischenGraph.value = data.datengraph;

    console.log(totalViolationCount.value)
    console.log(anzahlAffectedSuppliers.value)
    console.log(sourceConstraintComponentVerteilung.value)


    console.log('jooooooooooooooooooooo4')
    console.log(focusNodeVerteilung.value)
    console.log('jooooooooooooooooooooo4')

    focusNodeEntropy.value = data.focusNodeEntropy;
    resultPathEntropy.value = data.resultPathEntropy;
    sourceConstraintComponentEntropy.value = data.sourceConstraintComponentEntropy;

    
    meistBetroffenerSourceConstraint.value = data.most_violated_source_constraint_component;
    meistBetroffenerFocusNode.value = data.most_violated_node;
    meistBetroffenerResultPath.value = data.most_violated_path;



  
    focusNodePieChartData.value = generateChartData(focusNodeVerteilung.value)

    console.log(focusNodePieChartData.value)

    resultPathPieChartData.value = generateChartData(resultPathVerteilung.value)

    console.log(resultPathPieChartData.value)

    severityPieChartData.value = generateChartData(severityVerteilung.value)

    console.log(severityPieChartData.value)

    sourceConstraintComponentPieChartData.value = generateChartData(sourceConstraintComponentVerteilung.value)
    
    console.log(sourceConstraintComponentPieChartData.value)





  } catch (e: any) {
    error.value = e?.response?.data?.detail || e?.message || 'Konnte Daten nicht laden'
  } finally {
    isLoading.value = false
  }
})

const chartOptionsFokusNodes = {
  responsive: true,
  plugins: {
    title:{
      display: true,
      text: 'FocusNode Distrinbution',
      font: {
        size: 15
      }
    }
  }
}

const chartOptionsSourceConstraint = {
  responsive: true,
  plugins: {
    title:{
      display: true,
      text: 'Source Constraint Component Distrinbution',
      font: {
        size: 15
      }
    }
  }
}

const berecheZeilenStyle = (rowData) => {

  let gekürzt = aktuellerPath.split('#').pop();


  if(gekürzt == rowData.predicate){
    return "markedRow"
  }

  return null;
}




async function ediAnzeigen(focus_node, result_path, kg, edi, message, scc, shape, severity){
  aktuellerPath = result_path;


  violationDetailViewAnzeige.value = true;


  const data = {
    "focusNode": focus_node,
    "resultPath": result_path,
    "kg": kg,
    "edi": edi
  }
  
  try{
      const r = await callEdiAnzeigeBerechnenFunction(data);
      console.log("in der Funktion")
      console.log(r)

    //  detailViewAusgabeVariable.value = r.edi;




      subjectAusgabeVariable.value = r.subject;
      //predicateAusgabeVariable.value = r.predicate;
      objectAusgabeVariable.value = r.object;
      attributes.value = r.attributes;
      violationMessage.value = message;

      console.log("geht noch")

      shaclAttributes.value = [
        {attribut: 'focusNode', value: focus_node }, 
        {attribut: 'resultPathAnzeige',  value: result_path  },
        {attribut: 'severitynzeige',  value: severity  },
        {attribut: 'sourceConstraintComponentAnzeige',  value: scc  },
        {attribut: 'sourceShapeAnzeige',  value: shape},
        {attribut: 'message',  value: message },
      ]
      console.log("shaclAttributes")
      console.log(shaclAttributes)


  }
  catch(error) {
    console.log("fehlerrrrrrrrrrrrrr")
    console.log(error)
  }

}





const chartOptionsResultPath = {
  responsive: true,
  plugins: {
    title:{
      display: true,
      text: 'ResultPath Distrinbution',
      font: {
        size: 15
      }
    }
  }
}

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


const cellBearbeiten = (w) => {

  let {data, field, newValue} = w;
  data[field] = newValue;

}

const changeOfInput = async(data, field) => {
  try {

  const neuerWert = data[field]

  const attribut = data.predicate

  const node = subjectAusgabeVariable.value


  violationDetailViewAnzeige.value = false;

  console.log("uri : "+ data.fullUri)

  const newData = await callModellUpdatenFunction(neuerWert, attribut, node, originalReportID.value, data.status, data.fullUri)


  router.push({name:'dashboard', params: {runId: originalReportID.value}})
    
  }catch(e){
    console.log("error: " + e)
  }

 



}





function kürzen(uri: string) {
    if (!uri) return 'N/A';

    const hashIndex = uri.lastIndexOf('#');
    const slashIndex = uri.lastIndexOf('/');
    const index = Math.max(hashIndex, slashIndex);

    return index > 0 ? uri.substring(index + 1) : uri;
}

const backToFullDashboard = () =>{
  router.back();
}

const backToFullDashboard2 = () =>{
  history.go(-2)
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

    <button @click = "backToFullDashboard" class="backButton">
        Back <--
      </button>

      
  <div class="anzeigeBoxContainer1">

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Number of violations"
                :value= "totalViolationCount"
            />
            </template>
        
        <span>Number of violations found.</span>
        
    </v-tooltip>


    

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Number of suppliers"
                :value= "anzahlAffectedSuppliers"
            />
            </template>
        
        <span>Number of suppliers with incorrect invoices</span>
        
    </v-tooltip>



          

      </div>





          







      

  <div class="anzeigeBoxContainer2">

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Most Violated FocusNode"
                :value= "meistBetroffenerFocusNode"
            />
            </template>
        
        <span></span>
        
    </v-tooltip>


    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Most Violated ResultPath"
                :value="meistBetroffenerResultPath"
            />
            </template>
        
        <span></span>
        
    </v-tooltip>

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Most Violated sourceConstraintComponent"
                :value= "meistBetroffenerSourceConstraint" 
            />
            </template>
        
        <span></span>
        
    </v-tooltip>



          

  </div>



      

  <div class="anzeigeBoxContainer2">

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="FocusNode Entropy"
                :value= "focusNodeEntropy"
            />
            </template>
        
        <span>The entropy shows the spread of the distribution</span>
        
    </v-tooltip>


    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="ResultPath Entropy"
                :value="resultPathEntropy"
            />
            </template>
        
        <span>The entropy shows the spread of the distribution</span>
        
    </v-tooltip>

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="SourceConstraintComponent Entropy"
                :value= "sourceConstraintComponentEntropy" 
            />
            </template>
        
        <span>The entropy shows the spread of the distribution </span>
    </v-tooltip>
</div>


        
  <div class="ChartBoxContainer">
    
        <div class="chart-container">
            <Pie :data="focusNodePieChartData"
                  :options="chartOptionsFokusNodes"/>
          
        </div>
     
        <div class="chart-container">
            <Pie :data="resultPathPieChartData"
                :options="chartOptionsResultPath"/>

        </div>

      </div>

      <div class="ChartBoxContainer">
    
        <div class="chart-container">
            <Pie :data="severityPieChartData"/>
        </div>
     
        <div class="chart-container">
            <Pie :data="sourceConstraintComponentPieChartData"
                  :options="chartOptionsSourceConstraint"/>

        </div>

      </div>

    </div>

<div class="scrollbareViolationListe">

    <div v-for="(violation, index) in violationList" :key="index" 
         class="violation-item-wrapper" 
         :class="`severity-${violation.severity.toLowerCase()}`"> 
        
        <div class="violation-detail-grid">
            
            <v-btn class="edit-button" @click = "ediAnzeigen(violation.focus_node, violation.result_path, zwischenGraph, ediText, violation.result_message, violation.sourceConstraintComponent,  violation.sourceShape, violation.severity )">
              edit  
            </v-btn>
            
            <span class="grid-item message-text">
                {{ violation.result_message }}
            </span>

            <span class="grid-item result-path">
                Path: {{ violation.result_path }}
            </span>
            
            <span class="grid-item focus-node">
                Node: {{ violation.focus_node }}
            </span>
        </div>
        
    </div>

    <p v-if="violationList.length === 0" class="no-violations">Keine kritischen Verstöße gefunden.</p>

</div>


<Teleport to="body">
  <violationDetailModal :anzeigen="violationDetailViewAnzeige" @close="violationDetailViewAnzeige = false">

    <div class = "violationDetailModalContent">

      <DataTable :value="attributes" editMode="cell" tableStyle="min-width: 50rem" @cell-edit-complete = "cellBearbeiten" :rowClass = "berecheZeilenStyle">
          <Column field="predicate" header="Attribute"></Column>
          <Column field="object" header="Value">
            <template #editor="{ data, field }">
    <input 
        type="text" 
        v-model="data[field]" 
        style="border: 2px solid white; background-color: white; color: black; width: 100%; display: block; height: 30px;"
        @change="changeOfInput(data, field)"
    /> 
</template>
          </Column> </DataTable>

      <br>
      <br>
      <br>

      <DataTable :value = "shaclAttributes">
        <Column field="attribut" header="Attribut"></Column>
        <Column field="value" header="value"></Column>
      </DataTable>

    </div>


  </violationDetailModal>


  <button class = "filterButton" @click="graphExportieren" >Export the graph</button>

</Teleport>


  </main>


</template>

<style scoped>

html, body {  
  margin: 0;
  padding: 0;
}

p {
  font-family: inter;
  font-weight: 700;
  font-size: 20px}

h1 {
  font-size:50px;
}

h3 {
    font-size:20px;
    font-family: Inter;
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

anzeigeBoxInhalt {
  text-align: center;
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


.backButton {
  margin-top: -10px;
  margin-left: -10px;
  display: relative;
  z-index: 99999;
  justify-content: space-between;
  background-color:#FFFFFF;
  color: rgb(255, 255, 255); font-size: 17px; line-height: 17px; padding: 11px; border-radius: 10px; font-family: Georgia, serif; font-weight: normal; text-decoration: none; font-style: normal; font-variant: normal; text-transform: none; background-image: linear-gradient(to right, rgb(164, 164, 41) 0%, rgb(35, 136, 203) 0%, rgb(20, 78, 117) 100%); box-shadow: rgba(0, 0, 0, 0.28) 2px -7px 15px 0px; border: 2px solid rgb(28, 110, 164); display: inline-block;}
.backButton:hover {
background: #white; }
.backButton:active {
background: #19B2FF;
}



/*Anzeige*/


.anzeigeBoxContainer1{
    display: flex;
    justify-content: center;
    grid-template-columns: repeat(2, 1fr); 
    gap: 80px;
    margin-top:30px;
    width:60%;
    margin-left: auto;
    margin-right: auto;

}


.anzeigeBoxContainer2{
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


:deep(.markedRow ){
  background-color: #eb4634 !important;
  color: white !important;
}



/*   Filter */

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
  justify-content:center;
  display: flex;
  width: 100%;
  flex-direction: column;
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
  display:flex;
  flex-direction: horizontal;
  margin-left: auto;
  margin-right: auto;
  margin-top: 10px;


  
  color: rgb(100, 101, 99); 
  font-size: 15px; line-height: 15px; 
  padding: 6px; 
  border-radius: 11px; 
  font-family: Georgia, serif; 
  font-weight: normal; text-decoration: none; 
  font-style: normal; 
  font-variant: normal; 
  text-transform: none; 
  box-shadow: rgba(0, 0, 0, 0.4) 5px 5px 15px 5px; 
  border: 2px solid rgba(2, 12, 19, 1); 
  }


  .filterButton:hover {
  background: #1C6EA4; 
  }

  .filterButton:active {
  background: #144E75; }
  






/*Liste*/
.scrollbareViolationListe {
    height: 400px; /* Hält die Liste scrollbar */
    overflow-y: scroll;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 0; 
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


.edit-button {
  color: #black;
  background-color: #9EA09D;
}


.chart-container-entropyStatistik{
    height: 400px;
    width : 80%;
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    margin: 20px auto 0 auto;
    display: flex;
    flex-direction: column;  
    justify-content: center; 
    align-items: center;
    text-align: center; 
}


</style>