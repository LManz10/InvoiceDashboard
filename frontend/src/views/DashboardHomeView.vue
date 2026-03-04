<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Bar,Pie } from 'vue-chartjs'
import { useRouter, useRoute } from 'vue-router'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import {getAnalysisData, filterAndAnalyze, callEdiAnzeigeBerechnenFunction, callModellUpdatenFunction} from '../services/api'
import VueApexCharts from 'vue3-apexcharts';
import infoCard from '../components/infoCard.vue'

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   
import Row from 'primevue/row';                  
import InputText from 'primevue/InputText'; 

import violationDetailModal from '../components/violationDetailModal.vue'



import filterKomponente from '../components/filterKomponente.vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)
const chartData = ref<any>(null)
const pieChartData = ref<any>(null)

const route = useRoute();
const apexchart = VueApexCharts


const focusNodePieChartData = ref<any>(null)
const resultPathPieChartData = ref<any>(null)
const severityPieChartData = ref<any>(null)
const sourceConstraintComponentPieChartData = ref<any>(null)

const isLoading = ref(true)


const runId = route.params.runId as string
const error = ref<string | null>(null)
const dashboardData = ref<any>(null)

const totalViolationCount = ref<number | null>(null)
const anzahl_betroffener_nodes = ref<number | null>(null)
const anzahlBetroffenerShapes = ref<number | null>(null)
const anteilBetroffenerShapes = ref<number | null>(null)

const focusNodeEntropy = ref<number | null>(null)
const resultPathEntropy = ref<number | null>(null)
const sourceConstraintComponentEntropy = ref<number | null>(null)



const meistBetroffenerFocusNode = ref<number | null>(null)
const meistBetroffenerResultPath = ref<number | null>(null)
const meistBetroffenerSourceConstraint = ref<number | null>(null)


const focusNodeVerteilung = ref<number | null>(null)
const resultPathVerteilung = ref<number | null>(null)
const severityVerteilung = ref<number | null>(null)
const sourceConstraintComponentVerteilung = ref<number | null>(null)
const correlationData = ref([])
const entropyStatistikData = ref([])
const entropyStatistikDataSeries = ref([])

const violationList = ref([]);

const resultPathFilterInput = ref(''); 
const focusNodeFilterInput = ref(''); 
const severityFilterInput = ref('');
const sourceConstraintComponentFilterInput = ref('');

const router = useRouter();

const graphData = ref<string | null>(null);
const zwischenGraph = ref<string | null>(null);
const ediText = ref<string | null>(null);
let aktuellerPath = null;



const detailViewAusgabeVariable = ref("")
const subjectAusgabeVariable = ref("")
const predicateAusgabeVariable = ref("")
const objectAusgabeVariable = ref("")
const violationMessage = ref("")
const focusNodeAnzeige = ref("")
const resultPathAnzeige = ref("")
const severitynzeige = ref("")
const sourceConstraintComponentAnzeige = ref("")
const sourceShapeAnzeige = ref("")
const attributes = ref([])


const violationDetailViewAnzeige = ref(false);

const shaclAttributes = ref([]);





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
    zwischenGraph.value = data.datengraph;
    ediText.value = data.edi_content;

    anzahl_betroffener_nodes.value = data.anzahl_betroffener_nodes;
    anzahlBetroffenerShapes.value = data.anzahl_betroffener_shapes;
    anteilBetroffenerShapes.value = data.anteil_betroffener_shapes;

    focusNodeVerteilung.value = data.focus_node_verteilung;
    resultPathVerteilung.value = data.result_path_verteilung;
    severityVerteilung.value = data.severity_verteilung;
    sourceConstraintComponentVerteilung.value = data.source_constraint_component_verteilung;
    correlationData.value = data.correlationData;

    meistBetroffenerSourceConstraint.value = data.most_violated_source_constraint_component;
    meistBetroffenerFocusNode.value = data.most_violated_node;
    meistBetroffenerResultPath.value = data.most_violated_path;


    focusNodeEntropy.value = data.focusNodeEntropy;
    resultPathEntropy.value = data.resultPathEntropy;
    sourceConstraintComponentEntropy.value = data.sourceConstraintComponentEntropy;


    focusNodePieChartData.value = generateChartData(focusNodeVerteilung.value)
    resultPathPieChartData.value = generateChartData(resultPathVerteilung.value)
    severityPieChartData.value = generateChartData(severityVerteilung.value)
    sourceConstraintComponentPieChartData.value = generateChartData(sourceConstraintComponentVerteilung.value)
    entropyStatistikData.value = data.entropy_statistik
    entropyStatistikDataSeries.value = generateentropyStatistikDataSeries(entropyStatistikData.value)




  } catch (e: any) {
    error.value = e?.response?.data?.detail || e?.message || 'Konnte Daten nicht laden'
  } finally {
    isLoading.value = false
  }
})




async function statistikenNeuLadenNachKorrektur(neueDaten){

    totalViolationCount.value = neueDaten.anzahl_fehler
    violationList.value = neueDaten.list_of_violations || [];
    graphData.value = neueDaten.graph;
    zwischenGraph.value = neueDaten.datengraph
    ediText.value = neueDaten.edi_content;

    anzahl_betroffener_nodes.value = neueDaten.anzahl_betroffener_suppliers;
    anzahlBetroffenerShapes.value = neueDaten.anzahl_betroffener_shapes;
    anteilBetroffenerShapes.value = neueDaten.anteil_betroffener_shapes;

    focusNodeVerteilung.value = neueDaten.focus_node_verteilung;
    resultPathVerteilung.value = neueDaten.result_path_verteilung;
    severityVerteilung.value = neueDaten.severity_verteilung;
    sourceConstraintComponentVerteilung.value = neueDaten.source_constraint_component_verteilung;
    correlationData.value = neueDaten.correlationData;


    focusNodePieChartData.value = generateChartData(focusNodeVerteilung.value)
    resultPathPieChartData.value = generateChartData(resultPathVerteilung.value)
    severityPieChartData.value = generateChartData(severityVerteilung.value)
    sourceConstraintComponentPieChartData.value = generateChartData(sourceConstraintComponentVerteilung.value)
    entropyStatistikDataSeries.value = generateentropyStatistikDataSeries(entropyStatistikData.value)



    focusNodeEntropy.value = neueDaten.focusNodeEntropy;
    resultPathEntropy.value = neueDaten.resultPathEntropy;
    sourceConstraintComponentEntropy.value = neueDaten.sourceConstraintComponentEntropy;



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

      detailViewAusgabeVariable.value = r.edi;




      subjectAusgabeVariable.value = r.subject;
      predicateAusgabeVariable.value = r.predicate;
      objectAusgabeVariable.value = r.object;
      attributes.value = r.attributes;
      violationMessage.value = message;

      shaclAttributes.value = [
        {attribut: 'focusNode', value: focus_node }, 
        {attribut: 'resultPathAnzeige',  value: result_path  },
        {attribut: 'severitynzeige',  value: severity  },
        {attribut: 'sourceConstraintComponentAnzeige',  value: scc  },
        {attribut: 'sourceShapeAnzeige',  value: shape},
        {attribut: 'message',  value: message },
      ]

  }
  catch(error) {
    console.log("fehlerrrrrrrrrrrrrr")
  }

}



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


const chartOptionsSeverity = {
  responsive: true,
  plugins: {
    title:{
      display: true,
      text: 'Severity Distrinbution',
      font: {
        size: 15
      }
    }
  }
}


const changeOfInput = async(data, field) => {


  let neuerWert = data[field]

  if(!isNaN(neuerWert) && neuerWert !== ""){
    neuerWert = parseFloat(neuerWert.toString().replace(',','.'));
  }


  const attribut = data.predicate



  const node = subjectAusgabeVariable.value




  const newData = await callModellUpdatenFunction(neuerWert, attribut, node, runId, data.status, data.fullUri)


  statistikenNeuLadenNachKorrektur(newData)
    


}

const berecheZeilenStyle = (rowData) => {

  let gekürzt = aktuellerPath.split('#').pop();


  if(gekürzt == rowData.predicate){
    return "markedRow"
  }

  return null;
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


const chartOptionsCorrelationMatrix = {
  chart: {
    type: 'heatmap',
    toolbar: {show: false}
  },
  dataLabels: {
    enabled: true
  },

  xaxis: {
    type: 'category'
  },

  plotOptions: {
    heatmap: {
      colorScale: {
        ranges: [{
            from: 0,
            to: 100, 
            color: '#00A100', 
            name: 'Korrelation'
        }]
      }
    }
  }
};

const chartOptionsEntropy = {
  chart: {
    type: 'scatter'
  },
  xaxis: {
    type: 'numeric',
    title: { text: 'Entropy'}
  }, 
  yaxis: {
    type: 'numeric',
    title: { text: 'Count'}
  },
  markers: {
    size: 8, 
    hover: {size: 12}
  },


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

function generateentropyStatistikDataSeries(input){
  return [{
    name: "Entropy Analysis", 
    data: input.map(item => ({
      x: item.entropy,
      y: item.anzahl_violations,
      shapeName:item.shape
    }))
  }]
}

const cellBearbeiten = (w) => {

  let {data, field, newValue} = w;
  data[field] = newValue;




}




function kürzen(uri: string) {
    if (!uri) return 'N/A';

    const hashIndex = uri.lastIndexOf('#');
    const slashIndex = uri.lastIndexOf('/');
    const index = Math.max(hashIndex, slashIndex);

    return index > 0 ? uri.substring(index + 1) : uri;
}


async function graphExportieren(){


const blob = new Blob([zwischenGraph.value], {type: 'text/turtle;charset=utf-8'})
const fileName = "newGraph.ttl"
const url = window.URL.createObjectURL(blob)

const dl = document.createElement('a')
dl.href = url
dl.download = "newGraph.ttl"

document.body.appendChild(dl)
dl.click();

document.body.removeChild(dl)
window.URL.revokeObjectURL(url)
}



async function filtern(){

  const pathValue = resultPathFilterInput.value.trim();
  const focusValue = focusNodeFilterInput.value.trim();
  const severityValue = severityFilterInput.value.trim();
  const sourceConstraintComponentValue= sourceConstraintComponentFilterInput.value.trim();

  let ausgewählterFilter: string | null = null;
  let filterWert: string | null = null;

  if (pathValue.length > 0){
    ausgewählterFilter = "resultPath";
    filterWert = pathValue;

    if(focusValue.length > 0 || severityValue.length > 0 || sourceConstraintComponentValue.length > 0){
      return;
    }
  }
    
    
  if (focusValue.length > 0){
    ausgewählterFilter = "focusNode";
    filterWert = focusValue;


    if(severityValue.length > 0 || sourceConstraintComponentValue.length){
      return;
    }
      
  }
     
  
  if (severityValue.length > 0){
      filterWert = severityValue;
      ausgewählterFilter = "severity"; 

      if(sourceConstraintComponentValue.length){
      return;
    }
  }


if(sourceConstraintComponentValue.length > 0){
    filterWert = sourceConstraintComponentValue;
    ausgewählterFilter = "sourceConstraintComponent"
}

  const d = new Date();


  const input = {
    "name": "filter:" + d.toISOString(),
    "ausgewählterFilter": ausgewählterFilter, 
    "filterValue": filterWert,
    "graph": graphData.value,
    "originalReportID": runId, 
    "datengraph": zwischenGraph.value
  }

  console.log("in Dashboardhomeview: " + input.name + " " +  input.ausgewählterFilter + " " + input.filterValue)

  const filterData = await filterAndAnalyze(input);
  
  await router.push({ name: 'filterview', params: { runId: filterData.run_id } })




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
                title="Number of Focus Nodes"
                :value= "anzahl_betroffener_nodes"
            />
            </template>
        
        <span>Number of different FocusNodes</span>
        
    </v-tooltip>



          

      </div>




  <div class="anzeigeBoxContainer2">

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Number of Shapes"
                :value= "89"
            />
            </template>
        
        <span>Total number of Shapes.</span>
        
    </v-tooltip>


    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Number of affected shapes "
                :value="anzahlBetroffenerShapes"
            />
            </template>
        
        <span>Percentage of incorrect invoices</span>
        
    </v-tooltip>

    <v-tooltip
        location="bottom"
        open-delay="200">
        <template v-slot:activator="{ props }">
            <infoCard
                v-bind="props"
                title="Proportion of affected shapes"
                :value= "anteilBetroffenerShapes" 
            />
            </template>
        
        <span>Nxxxxxxxxxxxx</span>
        
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
        
        <span>The entropy shows the spread of the distribution</span>
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
            <Pie :data="severityPieChartData"
                  :options= "chartOptionsSeverity"/>
        </div>
     
        <div class="chart-container">
            <Pie :data="sourceConstraintComponentPieChartData"
                  :options="chartOptionsSourceConstraint"/>

        </div>

      </div>

      
      <div class="chart-container-CorrelatioMatrix">
          <apexchart
          width = "1200px"
          height="100%"
          type= "heatmap"
          :series = "correlationData"
          :options = "chartOptionsCorrelationMatrix"
          ></apexchart>
      </div>

      <div class="chart-container-entropyStatistik">
        <apexchart
          width = "1200px"
          height="100%"
          type= "scatter"
          :series = "entropyStatistikDataSeries"
          :options = "chartOptionsEntropy"
          ></apexchart>
      </div>
        



        
     




        <div class = "filterÜberschrift">
         <h2>Filter</h2>
        </div>

        
        <div class="FilterAuswahlContainer"> 
              
                <div class = "einzelnerFilter">
                  <h3>Result Path</h3>
                  <input type="text" class = "filterInput" v-model = "resultPathFilterInput">
                </div>

                <div class = "einzelnerFilter">
                  <h3>FocusNode</h3>
                  <input type="text" class = "filterInput" v-model = "focusNodeFilterInput">

                </div>

                <div class = "einzelnerFilter">
                  <h3>Severity </h3>
                  <input type="text" class = "filterInput"  v-model = "severityFilterInput">
                </div>

                <div class = "einzelnerFilter">
                  <h3>Source Constraint Component</h3>
                  <input type="text" class= "filterInput" v-model = "sourceConstraintComponentFilterInput">
                </div>
          </div>

          <button class = "filterButton" @click="filtern"> Filter</button>
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


      <h1>Shacl :</h1>
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


.violationDetailModalContent {
  max-height: 70vh;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}

.trippleAnzeige {
  display: grid;
  grid-template-columns: 1fr, 1fr, 1fr;
  gap: 10px;
}

.trippleAnzeigeEins {


}

:deep(.markedRow ){
  background-color: #eb4634 !important;
  color: white !important;
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

.chart-container-CorrelatioMatrix {
    height: 600px;
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


  font-weight: 500; 
  text-decoration: none; 
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



.downloadButton {




}





</style>