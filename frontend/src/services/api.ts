import { http } from "./https"




export async function analyzeOneShot(sourceFile: File) {
  const datei = new FormData()
  datei.append("source_file", sourceFile)

  const { data } = await http.post("/analyze/", datei)
  
  return data
}


export async function getAnalysisData(runId: string | number) {

  const { data } = await http.get(`/runs/${runId}/`) 
  return data
}


export async function filterAndAnalyze(filterParams: any) {

  const { data } = await http.post("/filtered-runs/", filterParams)
  
  return data

}




export async function getFilterRun(runId: string | number) {

  const { data } = await http.get(`/filtered-runs/${runId}/`) 
  return data
}


export async function callEdiAnzeigeBerechnenFunction(data: any) {


  console.log("Aufruf der edi-anzeige Funktion mit Daten in der frontend api.ts:");





  const res  = await fetch("http://localhost:8000/api/v1/edi-anzeige/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },  

  
    body: JSON.stringify(data),
  })


  console.log("Response Status:", res.status);

  const antwort = await res.json();


  return antwort;
}



export async function  callModellUpdatenFunction(neuerWert: any, attribut: any, node:any, runID:any, status: any, fullUri: any) {


  try {
    const r = await http.post("modell-updaten/", {
      newValue: neuerWert,
      attribute: attribut,
      focusNode: node,
      runID: runID,
      status: status,
      fullUri: fullUri,
    });

    return r.data.neueErgebnisse;

  } catch (error) {
    console.error("Fehler beim Aufruf der modell-updaten Funktion:", error);
    throw error;
  }}