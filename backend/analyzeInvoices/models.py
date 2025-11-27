from django.db import models
import uuid
    
class Report(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # automatische generierung
        editable=False      #nicht ännderbar
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="PENDING")
    violation_count = models.IntegerField(default=0) 
    
    anzahl_betroffener_suppliers = models.IntegerField(default=0)  
    focus_node_verteilung = models.JSONField(default=dict)
    result_path_verteilung = models.JSONField(default=dict)
    severity_verteilung = models.JSONField(default=dict)
    source_constraint_component_verteilung = models.JSONField(default=dict)

    list_of_violations = models.JSONField(default=list, blank=True)
    graph = models.TextField(default="")  


    
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
    
    anzahl_betroffener_suppliers = models.IntegerField(default=0)  
    focus_node_verteilung = models.JSONField(default=dict)
    result_path_verteilung = models.JSONField(default=dict)
    severity_verteilung = models.JSONField(default=dict)
    list_of_violations = models.JSONField(default=list, blank=True)