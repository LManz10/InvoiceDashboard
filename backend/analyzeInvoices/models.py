from django.db import models
import uuid
    
class Report(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # automatische generierung
        editable=False      #nicht änderbar
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="PENDING")
    violation_count = models.IntegerField(default=0) 

    anzahl_betroffener_nodes = models.IntegerField(default=0)  
    anzahl_betroffener_shapes = models.IntegerField(default=0)
    anteil_betroffener_shapes = models.TextField(default="0%")
    focus_node_verteilung = models.JSONField(default=dict)
    result_path_verteilung = models.JSONField(default=dict)
    severity_verteilung = models.JSONField(default=dict)
    source_constraint_component_verteilung = models.JSONField(default=dict)
    most_violated_node = models.TextField(default="")
    most_violated_path = models.TextField(default="")
    most_violated_source_constraint_component = models.TextField(default="")

    list_of_violations = models.JSONField(default=list, blank=True)
    graph = models.TextField(default="")  
    datengraph = models.TextField(default="")
    edi_content = models.TextField(default="")
    correlationData = models.JSONField(default=list)
    allPaths = models.JSONField(default=list)
    entropy_statistik = models.JSONField(default=dict)
    focusNodeEntropy = models.FloatField(default=0.0)
    resultPathEntropy = models.FloatField(default=0.0)  
    sourceConstraintComponentEntropy = models.FloatField(default=0.0)

    
   


    
class Filter(models.Model):
    filterID = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # automatische generierung
        editable=False      
    )

    originalReportID = models.UUIDField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="PENDING")
    violation_count = models.IntegerField(default=0) 
    
    anzahl_betroffener_nodes = models.IntegerField(default=0)  
    focus_node_verteilung = models.JSONField(default=dict)
    result_path_verteilung = models.JSONField(default=dict)
    severity_verteilung = models.JSONField(default=dict)
    list_of_violations = models.JSONField(default=list, blank=True)
    source_constraint_component_verteilung = models.JSONField(default=dict)
    
    most_violated_node = models.TextField(default="")
    most_violated_path = models.TextField(default="")
    most_violated_source_constraint_component = models.TextField(default="")

    graph = models.TextField(default="") 
    datengraph = models.TextField(default="") 
    correlationData = models.JSONField(default=list)
    allPaths = models.JSONField(default=list)
    entropy_statistik = models.JSONField(default=dict)
    focusNodeEntropy = models.FloatField(default=0.0)
    resultPathEntropy = models.FloatField(default=0.0)  
    sourceConstraintComponentEntropy = models.FloatField(default=0.0)
