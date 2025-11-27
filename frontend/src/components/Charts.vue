<template>
      <Bar
    :data="chartData"
    :options="chartOptions"
  />
     
</template>



<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'





const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    default: () => ({ 
      responsive: true,
      maintainAspectRatio: false 
    })
  }
})
</script>