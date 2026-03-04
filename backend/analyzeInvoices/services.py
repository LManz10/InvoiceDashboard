
from django.http import JsonResponse
from rest_framework.views import APIView           #die beiden auskommentieren wenn man es lokal ausprobieren will 
from rest_framework.response import Response   
#from src2.edifact_val import ediToShacl
from os.path import join
import sys, os
import rdflib,uuid
from rdflib.graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, RDFS, XSD
from django.core.files.uploadedfile import UploadedFile
from collections import defaultdict
import itertools
import math
import time
import tracemalloc
import functools


pfad1 = r"C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\backend\analyzeInvoices"
pfad2 = r"C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\backend"
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

EDI_pfad = join(
    pfad2, 
    'EDIFACT-VAL-main', 
    'EDIFACT-VAL-main', 
    'src2'
)

sys.path.append(EDI_pfad)

from edifact_val import ediToShacl, graphToShacl

queryGesamtAnzahl= """
SELECT (COUNT(?result) AS ?violationCount)
WHERE {
    ?result a sh:ValidationResult .
    }
    """


queryAnzahlBetroffenerNodes= """
SELECT (COUNT(DISTINCT ?focusNode) as ?anzahl)
WHERE {
    ?report sh:result ?result .
    ?result sh:focusNode ?focusNode .

}
    """





queryAnzahlBetroffenerShapes= """
SELECT (COUNT(DISTINCT ?sourceShape) as ?anzahl)
WHERE {
    ?report sh:result ?result .
    ?result sh:sourceShape ?sourceShape .

}
    """


queryMostViolatedNodes= """
SELECT ?focusNode (COUNT(*) as ?count) 
WHERE {
    ?report sh:result ?result .
    ?result sh:focusNode ?focusNode .
}
GROUP BY ?focusNode
ORDER BY DESC(?count)
LIMIT 1
"""

queryMostViolatedPath= """
SELECT ?resultPath (COUNT(*) as ?count) 
WHERE {
    ?report sh:result ?result .
    ?result sh:resultPath ?resultPath .
}
GROUP BY ?resultPath
ORDER BY DESC(?count)
LIMIT 1
"""

queryMostSoureceConstraintComponent= """
SELECT ?sourceConstraintComponent (COUNT(*) as ?count) 
WHERE {
    ?report sh:result ?result .
    ?result sh:sourceConstraintComponent ?sourceConstraintComponent .
}
GROUP BY ?sourceConstraintComponent
ORDER BY DESC(?count)
LIMIT 1
"""


EntropyStatistikQuery = """
SELECT ?focusNode ?resultPath (COUNT(?result) AS ?count)
WHERE {
    ?report sh:result ?result .
    ?result sh:focusNode ?focusNode .
    ?result sh:resultPath ?resultPath .
}
GROUP BY ?focusNode ?resultPath
    """


queryFürKorrelationsMatrix = """
SELECT ?focusNode ?resultPath
WHERE {
    ?result a sh:ValidationResult .
    ?result sh:focusNode ?focusNode .
    optional {?result sh:resultPath ?resultPath .}
}
""" 





def queryFocusNodeVerteilungsFunktion(graph):
    queryFocusNodeDistribution = """
    SELECT ?focusNode (COUNT(*) as ?count)
    WHERE {
        ?result a sh:ValidationResult .
        ?result sh:focusNode ?focusNode .
    }
    GROUP BY ?focusNode
    ORDER BY DESC(?count)
    """
    results = graph.query(queryFocusNodeDistribution)

    return [
    {
        "key": str(row[0]),
        "value": row[1].value
    }

    for row in results
    ]

def querySourceConstraintComponentVerteilungsFunktion(graph):
    queryResultPathVerteilung = """
    SELECT ?sourceConstraintComponent (COUNT(*) as ?count)
    WHERE {
        ?result a sh:ValidationResult .
        ?result sh:sourceConstraintComponent ?sourceConstraintComponent .
    }
    GROUP BY ?sourceConstraintComponent
    ORDER BY DESC(?count)
    """
    results = graph.query(queryResultPathVerteilung)

    return [
    {
        "key": str(row[0]),
        "value": row[1].value
    }

    for row in results
    ]

def queryResultPathVerteilungsFunktion(graph):

    queryResultPathVerteilung = """
    SELECT ?resultPath (COUNT(*) as ?count)
    WHERE {
        ?result a sh:ValidationResult .
        ?result sh:resultPath ?resultPath .
    }
    GROUP BY ?resultPath
    ORDER BY DESC(?count)
    """
    results = graph.query(queryResultPathVerteilung)

    return [
    {
        "key": str(row[0]),
        "value": row[1].value
    }

    for row in results
    ]


def querySeverityVerteilungsFunktion(graph):
    querySeverityVerteilung = """
    SELECT ?severity (COUNT(*) as ?count)
    WHERE {
        ?result a sh:ValidationResult .
        ?result sh:severity ?severity .
    }
    GROUP BY ?severity
    ORDER BY DESC(?count)
    """

    results = graph.query(querySeverityVerteilung)

    if len(results) == 0 or all(row[0] == 0 for row in results):
        return [
            {"key": "Violation", "value": "1"}
        ]

    return [
    {
        "key": str(row[0]),
        "value": str(row[1].value)
    }

    for row in results
    ]


def queryListOfViolationsFunktion(graph): 
    queryListOfViolations = """

    SELECT ?result ?focusNode ?resultPath ?severity ?resultMessage ?sourceConstraintComponent ?sourceShape
    WHERE {
        ?result a sh:ValidationResult .
        ?result sh:focusNode ?focusNode ;
                sh:resultPath ?resultPath ;
                sh:resultMessage ?resultMessage ;
                sh:sourceShape ?sourceShape ;
                sh:sourceConstraintComponent ?sourceConstraintComponent .
        OPTIONAL {
            ?result sh:severity ?severity .}
    }
            """
    
    results = graph.query(queryListOfViolations)

    rückgabeListe = []

    for row in results:
        violation = {
            "result": str(row.result),
            "focus_node": str(row.focusNode),
            "result_path": str(row.resultPath),
            "severity": str(row.severity),
            "result_message": str(row.resultMessage),
            "sourceConstraintComponent": str(row.sourceConstraintComponent),
            "sourceShape": str(row.sourceShape)
        }
        rückgabeListe.append(violation)


    return rückgabeListe



def dataForKorrelationMatrix(graph):

    pathsProFocusNode = defaultdict(set)
    b = graph.query(queryFürKorrelationsMatrix, initNs={"sh": SH})

    for row in b:
        fn = str(row.focusNode)
        rp = str(row.resultPath).split('#')[1] if '#' in str(row.resultPath) else str(row.resultPath).split('/')[-1]

        pathsProFocusNode[fn].add(rp)


    coOc = defaultdict(int)
    allePfade = set()   


    for fehler in pathsProFocusNode.values():
        if len(fehler) > 1:
            sortiert = sorted(list(fehler))

            for combination in itertools.combinations(sortiert, 2):
                coOc[combination] += 1

    allePfade.update(fehler)
    grouped = defaultdict(list)
         
    for (a,b), count in coOc.items():
        grouped[a].append({"x": b,"y": count})
        grouped[b].append({"x": a,"y": count})


    returnData = []

    for a, b in grouped.items():
        returnData.append({
            "name": a,
            "data": b,
        })
    
    return returnData, allePfade

                             
                                



def performanceTest(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        tracemalloc.start()

        result = func(*args, **kwargs)

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Execution time: {end_time - start_time:.4f} seconds")
        print(f"Current memory usage: {current / 10**6:.4f} MB; Peak memory usage: {peak / 10**6:.4f} MB")

        return result
    return wrapper



@performanceTest
def analyze(hochgeladeneDatei: UploadedFile, existing_id = None):

    pfad = r'C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\beispielShaclReportBearbeitet.ttl'
   
    report_format = "turtle" 
    content = "hat nicht funktioniert"


    
    if type(hochgeladeneDatei) == str:
        content = hochgeladeneDatei

        graph = rdflib.Graph()
        datengraph = rdflib.Graph()

        datengraph.parse(data=hochgeladeneDatei, format= 'ttl')
        graph = graphToShacl(datengraph)

    elif hochgeladeneDatei.name.endswith('.ttl'):
        content = hochgeladeneDatei.read().decode('utf-8')
        graph = rdflib.Graph()

        graph = graphToShacl(content) 

        
        datengraph = rdflib.Graph()

        try:
            datengraph.parse(data=content, format= 'turtle')
            print(f"SHACL-Report erfolgreich aus EDIFACT-Datei generiert. Anzahl Triplets: {len(graph)}")
        except Exception as e:
            return JsonResponse({"detail": f"Fehler beim Parsen der generierten SHACL-Daten: {e}"}, status=400)

    elif hochgeladeneDatei.name.endswith('.edi'): 
        content = hochgeladeneDatei.read().decode('utf-8')  
        finalttl = ediToShacl(content)[1].decode('utf-8')
        zwischenttl = ediToShacl(content)[0] #.decode('utf-8')

        graph = rdflib.Graph()
        datengraph = rdflib.Graph()

        try:
            graph.parse(data=finalttl, format= 'turtle')
            datengraph.parse(data=zwischenttl, format= 'turtle')
        except Exception as e:
            print(f"Fehler beim Parsen der generierten SHACL-Daten: {e}") 
        
    else:
        return Response(
            {"detail": "Ungültiges Dateiformat. Bitte laden Sie eine .ttl oder .edi Datei hoch."},)

    
    

    result_set = graph.query(queryGesamtAnzahl, initNs={"sh": SH})
    
    anzahlS = graph.query(queryAnzahlBetroffenerNodes, initNs={"sh": SH})
    anzahlBetrofferenerShapes = graph.query(queryAnzahlBetroffenerShapes, initNs={"sh": SH})



#---------------------entropy statistik berechnen -----------------------
    
    zwischenRechnung = {}
    shapedata = defaultdict(list)
    entropy_statistik = []

    listeNodePath = graph.query(EntropyStatistikQuery, initNs={"sh": SH}) 

    for row in listeNodePath:
        node = str(row.focusNode)
        result_path = str(row.resultPath)
        count = int(row['count'].value)

      #  print("node: " + node + " result_path: " + result_path + " count: " + str(count))

        shapedata[node].append(count)

    for node, counts in shapedata.items():
        violations = sum(counts)

        entropy = 0

        if violations > 0: 
            for count in counts:
                p = count / violations
                entropy -= p * (0 if p == 0 else math.log2(p))

        zwischenRechnung[node] = {
            "violations": violations,
            "entropy": entropy
        }
    

    
    for node, data in zwischenRechnung.items():
    #    print(f"Node: {node}, Anzahl Violations: {data['violations']}, Entropy: {data['entropy']}") 
        entropy_statistik.append({
            "node": node,
            "anzahl_violations": data["violations"],
            "entropy": round(data["entropy"], 4)
        })
#---------------------ende entropy statistik berechnen -----------------------



    correlationsResult = dataForKorrelationMatrix(graph)

    data = {
        "anzahl_fehler": list(result_set)[0].violationCount.value,
        "run_id": str(uuid.uuid4()),
        "anzahl_betroffener_nodes": list(anzahlS)[0].anzahl.value,  
        "anzahl_betroffener_shapes": list(anzahlBetrofferenerShapes)[0].anzahl.value,
        "anteil_betroffener_shapes": str(round(float(list(anzahlBetrofferenerShapes)[0].anzahl.value) / 89, 4)*100)[:5] + "%",        #hier benutze ich noch konstante -> ändern
        "focus_node_verteilung": queryFocusNodeVerteilungsFunktion(graph),
        "result_path_verteilung": queryResultPathVerteilungsFunktion(graph),
        "source_constraint_component_verteilung": querySourceConstraintComponentVerteilungsFunktion(graph),
        "severity_verteilung": querySeverityVerteilungsFunktion(graph),
        "most_violated_node": str(list(graph.query(queryMostViolatedNodes, initNs={"sh": SH}))[0].focusNode),
        "most_violated_path": str(list(graph.query(queryMostViolatedPath, initNs={"sh": SH}))[0].resultPath),
        "most_violated_source_constraint_component": str(list(graph.query(queryMostSoureceConstraintComponent, initNs={"sh": SH}))[0].sourceConstraintComponent),

        "list_of_violations": queryListOfViolationsFunktion(graph),
        "graph": graph.serialize(format='turtle'),
        "datengraph": datengraph.serialize(format='turtle'), 
        "edi_content": content ,
        "correlationData": correlationsResult[0],
        "allPaths": list(correlationsResult[1]),
        "entropy_statistik": entropy_statistik
    }


    data["focusNodeEntropy"] = entropyAnzeigeBerechnen(data["focus_node_verteilung"])
    data["resultPathEntropy"] = entropyAnzeigeBerechnen(data["result_path_verteilung"])
    data["sourceConstraintComponentEntropy"] = entropyAnzeigeBerechnen(data["source_constraint_component_verteilung"])
        



    return data




def entropyAnzeigeBerechnen(verteilung):
    if not verteilung:
        return 0
    
    erg = 0
    summe = sum(i['value'] for i in verteilung)

    for item in verteilung:
        p = item['value'] / summe
        erg -= p * (0 if p == 0 else math.log2(p))

    

    return round(erg, 4)    


def analyzeFilterResult(neuerGraph: rdflib.graph.Graph):
    report_format = "turtle" 


    graph = rdflib.Graph()



    turtle_output = graph.serialize(format='turtle') 


    result_set = neuerGraph.query(queryGesamtAnzahl, initNs={"sh": SH})

    
    anzahlS = neuerGraph.query(queryAnzahlBetroffenerNodes, initNs={"sh": SH})



    data1 = {
        "anzahl_fehler": list(result_set)[0].violationCount.value,
        "run_id": str(uuid.uuid4()),
        "anzahl_betroffener_nodes": list(anzahlS)[0].anzahl.value,  
        "focus_node_verteilung": queryFocusNodeVerteilungsFunktion(neuerGraph),
        "result_path_verteilung": queryResultPathVerteilungsFunktion(neuerGraph),
        "source_constraint_component_verteilung": querySourceConstraintComponentVerteilungsFunktion(neuerGraph),
        "severity_verteilung": querySeverityVerteilungsFunktion(neuerGraph),
        "list_of_violations": queryListOfViolationsFunktion(neuerGraph),
        "graph": neuerGraph.serialize(format='turtle')

    }


        
    anzahlS = neuerGraph.query(queryAnzahlBetroffenerNodes, initNs={"sh": SH})
    anzahlBetrofferenerShapes = neuerGraph.query(queryAnzahlBetroffenerShapes, initNs={"sh": SH})



#---------------------entropy statistik berechnen -----------------------
    
    zwischenRechnung = {}
    shapedata = defaultdict(list)
    entropy_statistik = []

    listeNodePath = neuerGraph.query(EntropyStatistikQuery, initNs={"sh": SH}) 

    for row in listeNodePath:
        node = str(row.focusNode)
        result_path = str(row.resultPath)
        count = int(row['count'].value)

      #  print("node: " + node + " result_path: " + result_path + " count: " + str(count))

        shapedata[node].append(count)

    for node, counts in shapedata.items():
        violations = sum(counts)

        entropy = 0

        if violations > 0: 
            for count in counts:
                p = count / violations
                entropy -= p * (0 if p == 0 else math.log2(p))

        zwischenRechnung[node] = {
            "violations": violations,
            "entropy": entropy
        }
    

    
    for node, data in zwischenRechnung.items():
    #    print(f"Node: {node}, Anzahl Violations: {data['violations']}, Entropy: {data['entropy']}") 
        entropy_statistik.append({
            "node": node,
            "anzahl_violations": data["violations"],
            "entropy": round(data["entropy"], 4)
        })
#---------------------ende entropy statistik berechnen -----------------------


    l1 = list(neuerGraph.query(queryMostViolatedNodes, initNs={"sh": SH}))
    l2 = list(neuerGraph.query(queryMostViolatedPath, initNs={"sh": SH}))
    l3 = list(neuerGraph.query(queryMostSoureceConstraintComponent, initNs={"sh": SH}))
    

    data = {
        "anzahl_fehler": list(result_set)[0].violationCount.value,
        "run_id": str(uuid.uuid4()),
        "anzahl_betroffener_suppliers": list(anzahlS)[0].anzahl.value,  
        "focus_node_verteilung": queryFocusNodeVerteilungsFunktion(neuerGraph),
        "result_path_verteilung": queryResultPathVerteilungsFunktion(neuerGraph),
        "source_constraint_component_verteilung": querySourceConstraintComponentVerteilungsFunktion(neuerGraph),
        "severity_verteilung": querySeverityVerteilungsFunktion(neuerGraph),
        "most_violated_node": str(l1[0].focusNode) if len(l1) > 0 else "N/A",
        "most_violated_path": str(l2[0].resultPath) if len(l2) > 0 else "N/A",
        "most_violated_source_constraint_component": str(l3[0].sourceConstraintComponent) if len(l3) > 0 else "N/A",
        "list_of_violations": queryListOfViolationsFunktion(neuerGraph),
        "graph": neuerGraph.serialize(format='turtle'),
        "correlationData": dataForKorrelationMatrix(neuerGraph)[0],
        "allPaths": list(dataForKorrelationMatrix(neuerGraph)[1]),
        "entropy_statistik": entropy_statistik
    }


    data["focusNodeEntropy"] = entropyAnzeigeBerechnen(data["focus_node_verteilung"])
    data["resultPathEntropy"] = entropyAnzeigeBerechnen(data["result_path_verteilung"])
    data["sourceConstraintComponentEntropy"] = entropyAnzeigeBerechnen(data["source_constraint_component_verteilung"])

    return data




def searchNode(kg_graph, node_to_search, resultPath):

    node = URIRef(node_to_search)

    data = {
        "node": str(node),
        "attributes": [],
        "connections": []

    }

    for p, o in kg_graph.predicate_objects(subject=node):   
        if isinstance(o, Literal):
            data["attributes"].append({
                "predicate": str(p).split('#')[-1] if '#' in str(p) else str(p).split('/')[-1],
                "object": str(o),
                "fullUri": str(p),
                "status": "found"
            })

        elif isinstance(o, URIRef) or isinstance(o, BNode):
            data["connections"].append({
                "predicate": str(p),
                "object": str(o),
                "fullUri": str(p), 
                "status": "found"
            })  

    return data












def filterFocusNode(original_graph, focus_node_to_filter):

    queryFilterFocusNode= f"""
    CONSTRUCT {{
        ?result ?p ?o .
    }}
    WHERE {{
        ?result sh:focusNode <{focus_node_to_filter}> .
        ?result ?p ?o .
    }}
    """

    neuerGraph = original_graph.query(
        queryFilterFocusNode,
     #   resultMethod='graph' 
      #  initNs={"sh": SH}
      ).graph



    return neuerGraph

def filterSourceConstraintComponent(original_graph, source_constraint_component_to_filter):
    queryFilterSourceConstraintComponent= f"""
    CONSTRUCT {{
        ?result ?p ?o .
    }}
    WHERE {{
        ?result sh:sourceConstraintComponent <{source_constraint_component_to_filter}> .
        ?result ?p ?o .
    }}
    """

    neuerGraph = original_graph.query(
        queryFilterSourceConstraintComponent,
     #   resultMethod='graph' 
      #  initNs={"sh": SH}
      ).graph
    


    return neuerGraph







def filterResultPath(original_graph, result_path_to_filter):
    queryFilterResultPath= f"""
    CONSTRUCT {{
        ?result ?p ?o .
    }}
    WHERE {{
        ?result sh:resultPath <{result_path_to_filter}> .
        ?result ?p ?o .
    }}
    """

    neuerGraph = original_graph.query(
        queryFilterResultPath,
      ).graph



    return neuerGraph



def filterSeverity(original_graph, focus_node_to_filter):
    return




def ediAnzeigeBerechnen(focusNode, resultPath, kg, ediContent):

    EDIFACT = rdflib.Namespace("https://purl.org/edifact/ontology#")
    schonGefunden = False


    kg_graph = rdflib.Graph()
    kg_graph.parse(data=kg, format='turtle')






    fn = URIRef(focusNode)



    l = list(kg_graph.triples((fn, URIRef(resultPath), None)))
    rückgabe = {
    #    "edi_segment": ganzes,
        "subject": str(focusNode),
        "predicate": str(resultPath), 
    #    "object": str(object), 
        }




    result = searchNode(kg_graph, fn, resultPath)


    rückgabe["attributes"] = result['attributes']


    for attr in result['attributes']:
        if attr['predicate'] == resultPath.split('#')[-1] or attr['predicate'] == resultPath.split('/')[-1]:
            schonGefunden = True
        rückgabe[attr['predicate']] = str(attr['object'])



    if not schonGefunden:
        rückgabe["attributes"].append({
                "predicate": resultPath.split('#')[-1] if '#' in resultPath else resultPath.split('/')[-1],
                "object": "",
                "fullUri": str(resultPath), 
                "status": "not found"

            })


    if len(l) > 0:
        rückgabe["object"] = str(l[0][2])
    else:
        rückgabe["object"] = "Kein Objekt gefunden"

  
        
        

    return rückgabe

