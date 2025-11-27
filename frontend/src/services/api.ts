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