from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Report
from .models import Filter
from .serializers import FilterSerializer
from .serializers import ReportSerializer
import rdflib
from rdflib.graph import Graph

from .services import analyze, filterFocusNode, filterResultPath, filterSeverity, analyzeFilterResult

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

            print("wir sind in der view erfolgreich angekommen")
            result = analyze(data_file)  

            print(data_file.name)
            print(result['run_id'])
            print(result.get('status', 'SUCCESS'))
            

            report_data = {
                'id': result['run_id'],           # Die generierte UUID
                'name': data_file.name,
                'status': result.get('status', 'SUCCESS'), 
                'violation_count': result.get('anzahl_fehler', 0),
                'anzahl_betroffener_suppliers': result.get('anzahl_betroffener_suppliers', 0),
                'focus_node_verteilung': result.get('focus_node_verteilung', {}),
                'source_constraint_component_verteilung': result.get('source_constraint_component_verteilung', {}),
                'severity_verteilung': result.get('severity_verteilung', {}),
                'result_path_verteilung': result.get('result_path_verteilung', {}),
                'severity_verteilung': result.get('severity_verteilung', {}),
                'list_of_violations': result.get('list_of_violations', []),
                'graph': result.get('graph', "")
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
      
        print("jaaaaaaaaaaaaa " + filternNach)
        if('focusNode' == filternNach):
            print("hieeeeeeeer1")
            alter_graph.parse(data=graphString, format='turtle')

            neuer_graph = filterFocusNode(alter_graph, request.data.get('filterValue'))
            print("hieeeeeeeer2: " + str(len(neuer_graph)))

        elif ('resultPath' == filternNach):
            neuer_graph = filterResultPath(graph, request.data.get('filterValue'))
        elif('severiy' == filternNach):
            neuer_graph = filterSeverity(graph, request.data.get('filterValue'))
        else:   
            return
        

        print("in python views: " + str(neuer_graph) + "länge: " + str(len(neuer_graph)))
                                         

        result = analyzeFilterResult(neuer_graph)

        filter_data = {
           # "originalReportID": str(original_report.id),
            "name": name,
            "status": "PENDING",
            "violation_count": result['anzahl_fehler'],
            "anzahl_betroffener_suppliers": result['anzahl_betroffener_suppliers'],
            "focus_node_verteilung": result['focus_node_verteilung'],
            "result_path_verteilung": result['result_path_verteilung'],
            "severity_verteilung": result['severity_verteilung'],
            "list_of_violations": result['list_of_violations'],
           # "graph": result['graph']
        }

        serializer = self.get_serializer(data=filter_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        print("Filter erfolgreich erstellt und gespeichert.")


        return


class ValidationRunViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response([], status=status.HTTP_200_OK)