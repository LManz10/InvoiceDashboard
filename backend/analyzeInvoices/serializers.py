from rest_framework import serializers
from .models import Report
from .models import Filter



class ReportSerializer(serializers.ModelSerializer):

    focus_node_verteilung = serializers.JSONField()
    result_path_verteilung = serializers.JSONField()
    severity_verteilung = serializers.JSONField()
    list_of_violations = serializers.JSONField()
    source_constraint_component_verteilung = serializers.JSONField()
    correlationData = serializers.JSONField()
    allPaths = serializers.JSONField()
    entropy_statistik = serializers.JSONField()
    
    class Meta:
        model = Report
        fields = ['id', 'violation_count', 'status', 'name', 'most_violated_node', 'most_violated_path', 'most_violated_source_constraint_component', 'focus_node_verteilung', 'result_path_verteilung', 'severity_verteilung', 'source_constraint_component_verteilung', 'anzahl_betroffener_nodes', 'anzahl_betroffener_shapes', 'list_of_violations', 'graph', 'datengraph', 'edi_content', 'correlationData', 'allPaths', 'anteil_betroffener_shapes', 'entropy_statistik', 'focusNodeEntropy', 'resultPathEntropy', 'sourceConstraintComponentEntropy']

    
    def validate_status(self, value):
        if value not in ['SUCCESS', 'FAILURE', 'PENDING']:
            raise serializers.ValidationError("Ungültiger Statuswert.")
        return value

    def validate_error_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Die Fehleranzahl darf nicht negativ sein.")
        return value
    


class FilterSerializer(serializers.ModelSerializer):

    focus_node_verteilung = serializers.JSONField()
    result_path_verteilung = serializers.JSONField()
    severity_verteilung = serializers.JSONField()
    list_of_violations = serializers.JSONField()
    source_constraint_component_verteilung = serializers.JSONField()
    correlationData = serializers.JSONField()
    allPaths = serializers.JSONField()
    entropy_statistik = serializers.JSONField()

    filterID = serializers.ReadOnlyField()
    
    class Meta:
        model = Filter
        fields = ['filterID', 'originalReportID', 'violation_count', 'status', 'name', 'focus_node_verteilung', 'result_path_verteilung','source_constraint_component_verteilung', 'severity_verteilung', 'anzahl_betroffener_nodes', 'list_of_violations', 'most_violated_node', 'most_violated_path', 'most_violated_source_constraint_component', 'graph', 'correlationData', 'allPaths', 'entropy_statistik', 'focusNodeEntropy', 'resultPathEntropy', 'sourceConstraintComponentEntropy', 'datengraph']
