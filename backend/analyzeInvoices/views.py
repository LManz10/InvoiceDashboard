from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Report
from .models import Filter
from .serializers import FilterSerializer
from .serializers import ReportSerializer
import rdflib
import uuid
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rdflib.graph import Graph

from .services import analyze, filterFocusNode, filterResultPath, filterSeverity,filterSourceConstraintComponent, analyzeFilterResult, ediAnzeigeBerechnen


#def runShaclAnalysis(data_file):



class AnalyzeView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data_file = request.FILES.get("source_file")

        if not data_file:
            return Response(
                {"detail": "source_file fehlt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            result = analyze(data_file)  
  
            report_data = {
                'id': result['run_id'],           # Die generierte UUID
                'name': data_file.name,
                'status': result.get('status', 'SUCCESS'), 
                'violation_count': result.get('anzahl_fehler', 0),
                'anzahl_betroffener_nodes': result.get('anzahl_betroffener_nodes', 0),
                'focus_node_verteilung': result.get('focus_node_verteilung', {}),
                'source_constraint_component_verteilung': result.get('source_constraint_component_verteilung', {}),
                'severity_verteilung': result.get('severity_verteilung', {}),
                'result_path_verteilung': result.get('result_path_verteilung', {}),
                'severity_verteilung': result.get('severity_verteilung', {}),
                'most_violated_node': result.get('most_violated_node', ""),
                'most_violated_path': result.get('most_violated_path', ""),
                'most_violated_source_constraint_component': result.get('most_violated_source_constraint_component', ""),
                'list_of_violations': result.get('list_of_violations', []),
                'graph': result.get('graph', ""),
                'datengraph': result.get('datengraph', ""), 
                'correlationData': result.get('correlationData', []),
                'allPaths': result.get('allPaths', []),
                'anzahl_betroffener_shapes': result.get('anzahl_betroffener_shapes', 0),
                'anteil_betroffener_shapes': result.get('anteil_betroffener_shapes', 0.0),
                'entropy_statistik': result.get('entropy_statistik', []),
                'focusNodeEntropy': result.get('focusNodeEntropy', 0.0),
                'resultPathEntropy': result.get('resultPathEntropy', 0.0),
                'sourceConstraintComponentEntropy': result.get('sourceConstraintComponentEntropy', 0.0)
            }
    

            #speicherung und validierung durch serializer
            serializer = ReportSerializer(data=report_data)
            serializer.is_valid(raise_exception=True)
            report_instance = serializer.save()



            return Response({'run_id': str(report_instance.id)}, status=status.HTTP_200_OK)        
        
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)






class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class FilterViewSet(viewsets.ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer


    def create(self, request, *args, **kwargs):
        original_report_id = request.data.get("originalReportID")
        name = request.data.get("name")
        graphString = request.data.get("graph")
        filternNach = request.data.get("ausgewählterFilter")
        neuer_graph = Graph()
        alter_graph = Graph()
      
        if('focusNode' == filternNach):
            alter_graph.parse(data=graphString, format='turtle')

            neuer_graph = filterFocusNode(alter_graph, request.data.get('filterValue'))

        elif ('resultPath' == filternNach):
            alter_graph.parse(data=graphString, format='turtle')
            neuer_graph = filterResultPath(alter_graph, request.data.get('filterValue'))

        elif('severity' == filternNach):
            alter_graph.parse(data=graphString, format='turtle')

            #neuer_graph = filter(alter_graph, request.data.get('filterValue'))
        elif('sourceConstraintComponent' == filternNach):
            alter_graph.parse(data=graphString, format='turtle')
            neuer_graph = filterSourceConstraintComponent(alter_graph, request.data.get('filterValue'))

            #neuer_graph = filter(alter_graph, request.data.get('filterValue'))
        else:   
            return
        

      #  print("in python views: " + str(neuer_graph) + "länge: " + str(len(neuer_graph)))
                                         

        result = analyzeFilterResult(neuer_graph)

        print("test c " + str(result['anzahl_fehler']))

        filter_data = {
            "originalReportID": uuid.UUID(original_report_id),
            "name": name,
            "status": "PENDING",
            "violation_count": result['anzahl_fehler'],
            "anzahl_betroffener_suppliers": result['anzahl_betroffener_suppliers'],
            "source_constraint_component_verteilung": result['source_constraint_component_verteilung'],
            "focus_node_verteilung": result['focus_node_verteilung'],
            "result_path_verteilung": result['result_path_verteilung'],
            "severity_verteilung": result['severity_verteilung'],
            "list_of_violations": result['list_of_violations'],
            "most_violated_node": result['most_violated_node'],
            "most_violated_path": result['most_violated_path'],
            "most_violated_source_constraint_component": result['most_violated_source_constraint_component'], 
            "entropy_statistik": result['entropy_statistik'],
            "focusNodeEntropy": result['focusNodeEntropy'],
            "resultPathEntropy": result['resultPathEntropy'],
            "sourceConstraintComponentEntropy": result['sourceConstraintComponentEntropy'], 
            "correlationData": result['correlationData'],
            "allPaths": result['allPaths'],
            "datengraph": request.data.get("datengraph")
            }

    


        try:
            serializer = self.get_serializer(data=filter_data)
            serializer.is_valid(raise_exception=True)
            ri = serializer.save()

       #     self.perform_create(serializer)



            headers = self.get_success_headers(serializer.data)

            return Response({'run_id': str(ri.filterID)}, status=status.HTTP_200_OK)        

        except Exception as fehler:
            print("fehler:" + str(fehler))

            return Response({"detail": str(fehler)}, status=status.HTTP_400_BAD_REQUEST)

        





class ValidationRunViewSet(viewsets.ViewSet):
   def list(self, request):
      return Response([], status=status.HTTP_200_OK)
    


@csrf_exempt
@require_POST
def edi_anzeige_berechnen(request):
    try:
        d = json.loads(request.body)
        focusNode = d.get("focusNode")
        resultPath = d.get("resultPath")
        kg = d.get("kg")
        edi = "" #d.get("edi")


        print("in views edi lenge: " + str(len(edi)))
        print(type(kg))

        print(edi[:500])
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Ungültige JSON-Daten."}, status=400)
   
    r = ediAnzeigeBerechnen(focusNode, resultPath, kg, edi)

    print(r.items())

    return JsonResponse({"subject": r["subject"], "predicate": r["predicate"], "object": r["object"], "attributes": r["attributes"]}, status=200)



   # return JsonResponse({"edi": r["edi_segment"], "subject": r["subject"], "predicate": r["predicate"], "object": r["object"], 
    #                     "currency": r["currency"], "dateOrderNumberSupplier": r["dateOrderNumberSupplier"], "documentDate": r["documentDate"],
     #                    "hasDiscountPercentage": r["hasDiscountPercentage"], "hasDiscountPercentagePaymentConditions": r["hasDiscountPercentagePaymentConditions"],
      #                   "hasDocumentFunction": r["hasDocumentFunction"], "hasDocumentNumber": r["hasDocumentNumber"], "hasDocumentType": r["hasDocumentType"],
      #                   "hasInvoiceAmount": r["hasInvoiceAmount"], "hasTaxAmount": r["hasTaxAmount"], "hasTaxableAmount": r["hasTaxableAmount"],
       #                  "hasTotalAmountUnderPaymentReduction": r["hasTotalAmountUnderPaymentReduction"], "hasTotalDutyTaxFeeAmount": r["hasTotalDutyTaxFeeAmount"],
        ##                 "hasTotalLineItemAmount": r["hasTotalLineItemAmount"], "hasVATrate": r["hasVATrate"], "invoiceCurrency": r["invoiceCurrency"],
          #               "orderNumberBuyer": r["orderNumberBuyer"], "orderNumberSupplier": r["orderNumberSupplier"], "paymentCondition": r["paymentCondition"],
           #              "paymentReferenceDate": r["paymentReferenceDate"], "actualDeliveryDate": r["actualDeliveryDate"]}, status=200)



@csrf_exempt
@require_POST
def modellUpdateView(request):

    print("Aufruf der modellUpdateView Funktion in views.py            hhhhhhhhhhhhhh")

    try:
        d = json.loads(request.body)
        node = d.get("focusNode")
        attribut = d.get("attribute")
        neuerWert = d.get("newValue")
        runID = d.get("runID")
        status = d.get("status")
        fullUri = d.get("fullUri")



        print("---------------------------------------------------")
        print("in views.py erhaltene daten:"
              "\n node: " + str(node) +
              "\n attribut: " + str(attribut) +
              "\n neuerWert: " + str(neuerWert) +
              "\n runID: " + str(runID))
        print("---------------------------------------------------")

        try:
            report = Report.objects.get(id=runID)
        except Report.DoesNotExist:
            return JsonResponse({"detail": "Bericht mit der angegebenen ID existiert nicht."}, status=404)

        modellDaten = report.datengraph


      

        node = rdflib.URIRef(node)

        g = rdflib.Graph()
        g.parse(data=modellDaten, format='turtle')


        if status == "not found":
            print("Knoten wurde nicht gefunden, füge neuen Knoten hinzu.")
            tripleZuHinzufuegen = (node, rdflib.URIRef(fullUri), rdflib.Literal(neuerWert))
            g.add(tripleZuHinzufuegen)

            neueGraphDaten = g.serialize(format='turtle')
            report.datengraph = neueGraphDaten

            neueErgebnisse = analyze(g.serialize(format='turtle'))

            report.save()

            print("Speichere aktualisiertes Modell im Bericht mit runID: " + str(runID))
            return JsonResponse({"detail": "Modell erfolgreich aktualisiert.","neueErgebnisse": neueErgebnisse }, status=200)


        predicate = rdflib.URIRef(fullUri)
        fNode = rdflib.URIRef(node)

        old = None
        type = None

        old = g.value(fNode, predicate)
        

        if old is not None:
            type = old.datatype
        else:
            print("Kein alter Wert gefunden für den Knoten " + str(node) + " und das Attribut " + str(fullUri))
            type = rdflib.XSD.string
        
        g.remove((fNode, predicate, None))


        g.add((fNode, predicate, rdflib.Literal(neuerWert, datatype=type)))
        
        neueGraphDaten = g.serialize(format='turtle')
        report.datengraph = neueGraphDaten

        neueErgebnisse = analyze(g.serialize(format='turtle'))

        report.save()

        print("Speichere aktualisiertes Modell im Bericht mit runID: " + str(runID))
        return JsonResponse({"detail": "Modell erfolgreich aktualisiert.","neueErgebnisse": neueErgebnisse }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"detail": "Ungültige JSON-Daten."}, status=400)
   
