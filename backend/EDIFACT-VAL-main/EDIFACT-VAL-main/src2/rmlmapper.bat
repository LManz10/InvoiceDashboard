@echo off 

java -jar "%~dp0rmlmapper-8.0.0-r378-all.jar" -s turtle -m "%~dp0mapping.rml.ttl" -o invoice.ttl