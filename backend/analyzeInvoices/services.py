
from rest_framework.views import APIView           #die beiden auskommentieren wenn man es lokal ausprobieren will 
from rest_framework.response import Response   
#from src2.edifact_val import ediToShacl
from os.path import join
import sys, os
import rdflib,uuid
from rdflib.graph import Graph
from django.core.files.uploadedfile import UploadedFile

pfad1 = r"C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\backend\analyzeInvoices"
pfad2 = r"C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\backend"


EDI_pfad = join(
    pfad2, 
    'EDIFACT-VAL-main', 
    'EDIFACT-VAL-main', 
    'src2'
)

sys.path.append(EDI_pfad)

from edifact_val import ediToShacl

queryGesamtAnzahl= """
SELECT (COUNT(?result) AS ?violationCount)
WHERE {
    ?result a sh:ValidationResult .}
    """


queryAnzahlBetroffenerSupplier= """
SELECT (COUNT(DISTINCT ?focusNode) as ?anzahl)
WHERE {
    ?report sh:result ?result .
    ?result sh:focusNode ?focusNode .

}
    """





def queryFocusNodeVerteilungsFunktion(graph):
    queryFocusNodeDistribution = """
    SELECT ?focusNode (COUNT(*) as ?count)
    WHERE {
        ?report sh:result ?result .
        ?result sh:focusNode ?focusNode .
    }
    GROUP BY ?focusNode
    ORDER BY DESC(?count)
    """
    results = graph.query(queryFocusNodeDistribution)

    return [
    {
        "key": str(row[0]),
        "value": str(row[1].value)
    }

    for row in results
    ]

def querySourceConstraintComponentVerteilungsFunktion(graph):
    queryResultPathVerteilung = """
    SELECT ?sourceConstraintComponent (COUNT(*) as ?count)
    WHERE {
        ?report sh:result ?result .
        ?result sh:sourceConstraintComponent ?sourceConstraintComponent .
    }
    GROUP BY ?sourceConstraintComponent
    ORDER BY DESC(?count)
    """
    results = graph.query(queryResultPathVerteilung)

    return [
    {
        "key": str(row[0]),
        "value": str(row[1].value)
    }

    for row in results
    ]

def queryResultPathVerteilungsFunktion(graph):

    queryResultPathVerteilung = """
    SELECT ?resultPath (COUNT(*) as ?count)
    WHERE {
        ?report sh:result ?result .
        ?result sh:resultPath ?resultPath .
    }
    GROUP BY ?resultPath
    ORDER BY DESC(?count)
    """
    results = graph.query(queryResultPathVerteilung)

    return [
    {
        "key": str(row[0]),
        "value": str(row[1].value)
    }

    for row in results
    ]


def querySeverityVerteilungsFunktion(graph):
    querySeverityVerteilung = """
    SELECT ?severity (COUNT(*) as ?count)
    WHERE {
        ?report sh:result ?result .
        ?result sh:severity ?severity .
    }
    GROUP BY ?severity
    ORDER BY DESC(?count)
    """
    results = graph.query(querySeverityVerteilung)

    return [
    {
        "key": str(row[0]),
        "value": str(row[1].value)
    }

    for row in results
    ]


def queryListOfViolationsFunktion(graph): 
    queryListOfViolations = """

    SELECT ?result ?focusNode ?resultPath ?severity ?resultMessage
    WHERE {
        ?report sh:result ?result .
        ?result sh:focusNode ?focusNode ;
                sh:resultPath ?resultPath ;
                sh:resultMessage ?resultMessage .
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
            "result_message": str(row.resultMessage)
        }
        rückgabeListe.append(violation)

    print(rückgabeListe)

    return rückgabeListe



def analyze(hochgeladeneDatei: UploadedFile):

    pfad = r'C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\beispielShaclReportBearbeitet.ttl'
   
    report_format = "turtle" 

    if hochgeladeneDatei.name.endswith('.ttl'):
        content = hochgeladeneDatei.read()

        graph = rdflib.Graph()

        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

        try:
            #graph.parse(pfad, format= 'turtle')
            graph.parse(data=content, format= 'turtle')
            
        except Exception as e:
            print(f"Fehler beim Parsen der Datei: {e}")   

    elif hochgeladeneDatei.name.endswith('.edi'): 
        content = hochgeladeneDatei.read().decode('utf-8')  

        

        finalttl = ediToShacl(content)[1].decode('utf-8')


        print(finalttl[:500])
        graph = rdflib.Graph()

        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

        try:
            graph.parse(data=finalttl, format= 'turtle')
            print(f"SHACL-Report erfolgreich aus EDIFACT-Datei generiert. Anzahl Triplets: {len(graph)}")
        except Exception as e:
            print(f"Fehler beim Parsen der generierten SHACL-Daten: {e}") 
    else:
        return Response(
            {"detail": "Ungültiges Dateiformat. Bitte laden Sie eine .ttl oder .edi Datei hoch."},)
    
    

    result_set = graph.query(queryGesamtAnzahl, initNs={"sh": SH})
    
    anzahlS = graph.query(queryAnzahlBetroffenerSupplier, initNs={"sh": SH})

    print("\n Auswertung des extern geladenen Reports:")
 


    data = {
        "anzahl_fehler": list(result_set)[0].violationCount.value,
        "run_id": str(uuid.uuid4()),
        "anzahl_betroffener_suppliers": 6,  
        "focus_node_verteilung": queryFocusNodeVerteilungsFunktion(graph),
        "result_path_verteilung": queryResultPathVerteilungsFunktion(graph),
        "source_constraint_component_verteilung": querySourceConstraintComponentVerteilungsFunktion(graph),
        "severity_verteilung": querySeverityVerteilungsFunktion(graph),

        "list_of_violations": queryListOfViolationsFunktion(graph),
        "graph": graph.serialize(format='turtle')

    }
        
    return data









def analyzeFilterResult(neuerGraph: rdflib.graph.Graph):

    #print("in analyze neuerGraph length1: " + str(len(graph)))

    print(type(neuerGraph))


    print("test1")
   
    report_format = "turtle" 

   # content = hochgeladeneDatei.read()

    graph = rdflib.Graph()


    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

    print("test2")


    #graph.parse(neuerGraph, format= 'turtle')

    print("in analyze neuerGraph length: " + str(len(graph)))

    turtle_output = graph.serialize(format='turtle') 

    print(turtle_output)

    result_set = neuerGraph.query(queryGesamtAnzahl, initNs={"sh": SH})
    
    anzahlS = graph.query(queryAnzahlBetroffenerSupplier, initNs={"sh": SH})

    print("\n Auswertung des extern geladenen Reports:")
 


    data = {
        "anzahl_fehler": list(result_set)[0].violationCount.value,
        "run_id": str(uuid.uuid4()),
        "anzahl_betroffener_suppliers": 6,  
        "focus_node_verteilung": queryFocusNodeVerteilungsFunktion(graph),
        "result_path_verteilung": queryResultPathVerteilungsFunktion(graph),
        "source_constraint_component_verteilung": querySourceConstraintComponentVerteilungsFunktion(graph),
        "severity_verteilung": querySeverityVerteilungsFunktion(graph),

        "list_of_violations": queryListOfViolationsFunktion(graph),
        "graph": graph.serialize(format='turtle')

    }

    print("joo" + str(list(result_set)[0].violationCount.value))
        
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

    print("neuerGraph length: " + str(len(neuerGraph)))
    print(type(neuerGraph))

    return neuerGraph




def filterResultPath(original_graph, focus_node_to_filter):
    return



def filterSeverity(original_graph, focus_node_to_filter):
    return
