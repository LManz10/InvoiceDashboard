<template>
  <div class="page">
    <header class="header">
      <h1>Datei hochladen</h1>
      <p class="subtitle">Zieh deine Datei hierher oder wähle sie aus.</p>
    </header>

    <main class="container">
      <section class="card">
        <div
          class="dropzone"
          :class="{ 'dropzone--active': isDragging }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="onDrop"
        >
          <input id="fileInput" type="file" class="file-input" @change="onFileChange" />
          <label for="fileInput" class="dropzone__label">
            <strong>Datei auswählen</strong> oder hierher ziehen
            <span v-if="file" class="filechip">{{ file.name }}</span>
          </label>
        </div>

        <div class="actions">
          <button class="btn btn-primary" :disabled="!file || iSloading" @click="onSubmit">
            {{ iSloading ? "Lade hoch…" : "Hochladen" }}
          </button>

          <button class="btn btn-ghost" :disabled="iSloading" @click="clearFile" v-if="file">Zurücksetzen</button>

          <button class="btn btn-ghost" :disabled="iSloading" @click="zurAnalyse" v-if="file">weiter</button>

          
        </div>

        <p v-if="error" class="alert alert-error"> {{ error }}</p>
        <div v-if="result" class="alert alert-success">
           Upload erfolgreich: <strong>{{ result.filename }}</strong>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from 'vue-router'
import { analyzeOneShot } from "@/services/api" 

const router = useRouter()

const file = ref<File | null>(null);
const iSloading = ref(false);
const error = ref<string | null>(null);
const result = ref<any>(null);
const isDragging = ref(false);


function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement;
  file.value = input.files?.[0] ?? null;
  isDragging.value = false;
  error.value = null;
  result.value = null;
}

async function zurAnalyse(){

  iSloading.value = true
  error.value = null
  try {
    const data = await analyzeOneShot(file.value!)

    await router.push({ name: 'dashboard', params: { runId: data.run_id } })

  } catch (err: any) {
    error.value = err?.response?.data?.detail || err?.message || 'Analyse fehlgeschlagen'
  } finally {
    iSloading.value = false
  }
}

function onDrop(e: DragEvent) {
  const dt = e.dataTransfer;
  if (!dt || !dt.files || dt.files.length === 0) return;
  file.value = dt.files[0];
  isDragging.value = false;
  error.value = null;
  result.value = null;
  
}

function clearFile() {
  file.value = null;
  error.value = null;
  result.value = null;
  const input = document.getElementById("fileInput") as HTMLInputElement | null;
  if (input) input.value = "";
}

async function onSubmit() {
  if (!file.value) return;
  iSloading.value = true;
  error.value = null;
  result.value = null;

  try {
    const fd = new FormData();
    fd.append("file", file.value);
    const res = await fetch("/api/upload/", { method: "POST", body: fd });
    if (!res.ok) throw new Error(await res.text());
    result.value = await res.json();
  } catch (e: any) {
    error.value = e?.message ?? "Upload fehlgeschlagen";
  } finally {
    iSloading.value = false;
  }
}
</script>

<style scoped>


.page {
  min-height: 100vh;        
  display: flex;             
  flex-direction: column;   
  justify-content: center;    
  align-items: center;        

  background:
    radial-gradient(1200px 500px at 10% -10%, rgba(79, 140, 255, 0.10), transparent 60%),
    radial-gradient(1000px 400px at 90% 0%, rgba(116, 195, 255, 0.10), transparent 60%),
    var(--bg);
  color: var(--text);
}

.header {
  text-align: center;
  margin: 0 0 1rem 0;
  padding: 0 1rem;
}

.header h1 {
  margin: 0 0 .25rem 0;
  font-size: clamp(1.4rem, 2vw + 1rem, 2.2rem);
  font-weight: 700;
  
}

.subtitle {
  margin: 0;
  color: var(--muted);
  font-size: .95rem;
}

.container {
  width: 100%;
  max-width: 600px;           
  margin: 0 auto;            
  padding: 0 1rem;
  display: grid;
  gap: 1rem;
}

.card {
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}


.dropzone {
  position: relative;
  border: 2px dashed rgba(255,255,255,0.15);
  border-radius: 14px;
  padding: 2.25rem 1rem;
  text-align: center;
  background: rgba(255,255,255,0.02);
}

.dropzone--active {
  border-color: var(--primary);
  box-shadow: 0 0 0 6px var(--ring);
  background: rgba(79,140,255,0.06);
}

.file-input {
  display: none;
}

.dropzone__label {
  cursor: pointer;
  display: inline-block;
  font-size: 1rem;
  color: var(--text);
}

.actions {
  margin-top: 1rem;
  display: flex;
  gap: .75rem;
  flex-wrap: wrap;
}

.btn {
  appearance: none;
  border: 1px solid transparent;
  border-radius: 10px;
  padding: .65rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary);
  color: white;
}
.btn-primary:hover:not(:disabled) { background: var(--primary-600); transform: translateY(-1px); }
.btn-primary:active:not(:disabled) { transform: translateY(0); }

.btn-ghost {
  background: transparent;
  border-color: rgba(255,255,255,0.18);
  color: var(--text);
}
.btn-ghost:hover:not(:disabled) { background: rgba(255,255,255,0.08); }

.alert {
  margin-top: 1rem;
  padding: .9rem 1rem;
  border-radius: 10px;
  line-height: 1.35;
  border: 1px solid transparent;
}
.alert-success { background: rgba(46, 204, 113, 0.12); border-color: rgba(46, 204, 113, 0.35); }
.alert-error   { background: rgba(255, 92, 92, 0.12); border-color: rgba(255, 92, 92, 0.35); }


:global(html, body, #app) { height: 100%; }
:global(body) { margin: 0; background: var(--bg); color: var(--text); }





</style>
