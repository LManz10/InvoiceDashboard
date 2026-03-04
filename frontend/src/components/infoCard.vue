<template>
  <v-card 
    class="kpi-card" 
    :elevation="3" 
    rounded="lg"
  >

    <div class="titelInfoCard">
      {{ title }}
    </div>

    <div 
      class="InfoCardWert" 
    >
      {{ value }}
    </div>


  </v-card>
</template>


<script setup lang = "ts">
    interface Props{
        title: string
        value: string | number
    }

    const {title, value} = defineProps<Props>()
</script>



<style scoped>

.kpi-card {
    transition: 0.2s;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 150px;
    padding: 16px;
    width: 300px;
    color: white;
    background-color: #19B2FF;
    
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
}

.titelInfoCard {
    font-size: 20px; 
    font-weight: 600;
    color: black;
    margin-bottom: 4px;
}

.InfoCardWert {
    line-height: 1.1;
    font-size: 14px;
    word-break:break-all;
    color: black;
}

</style>