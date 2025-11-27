import platform
import os
import shutil
from os import path
from django.core.files.uploadedfile import UploadedFile


from general_edifact_to_enriched_xml import (
    EDIFACTToEnrichedXMLConverter,
    yarrrmlparser_bash, rmlmapper_bash,
    yarrrmlparser_batch, rmlmapper_batch,
    validates
)

def ediToShacl(edi_data: str) -> tuple[str, str]:
        

        script_dir = path.dirname(path.abspath(__file__))

     
        parent_dir_1 = path.dirname(script_dir)
        parent_dir_2 = path.dirname(parent_dir_1)
        backend_dir = path.dirname(parent_dir_2)

        TTL_FILE_PATH_IN_BACKEND = path.join(backend_dir, "invoice.ttl")

        ttl_file_base = "ProcessExample"
        xml_file = "enriched_output.xml"
        zwischen_ttl_file = "invoice.ttl"

        converter = EDIFACTToEnrichedXMLConverter(edi_data)
        converter.convert()
        enriched_xml = converter.to_string()

        
            


        with open(xml_file, "w", encoding="utf-8") as f:
            f.write(enriched_xml)



        print("Running transformation and validation")
        if platform.system() == "Windows":
            yarrrmlparser_batch()
            rmlmapper_batch()
        elif platform.system() in ["Darwin", "Linux"]:
            yarrrmlparser_bash()
            rmlmapper_bash()
        else:
            print("Unsupported platform")


        print("hier scheint alles geklappt zu haben1")
        print(f"TTL_FILE_PATH_IN_BACKEND: {TTL_FILE_PATH_IN_BACKEND}")
            
        with open(TTL_FILE_PATH_IN_BACKEND, "r", encoding="utf-8") as fin:
            kg_output = fin.read()

        validation_report = validates(ttl_file_base, TTL_FILE_PATH_IN_BACKEND)


        print("hier scheint alles geklappt zu haben2")


     #   if os.path.isfile(TTL_FILE_PATH_IN_BACKEND):
       #     os.remove(TTL_FILE_PATH_IN_BACKEND)



     #   if os.path.isfile(xml_file):            
         #   os.remove(xml_file)

        print("hier scheint alles geklappt zu haben3")


        return kg_output, validation_report







def read_edi_file_as_string(file_path: str) -> str:

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"UTF-8 Dekodierung fehlgeschlagen für Datei: {file_path}. Versuche ISO-8859-1 Dekodierung.")

    try:
        with open(file_path, "r", encoding="iso-8859-1") as f:
            return f.read()
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            f"Weder UTF-8 noch ISO-8859-1 konnten '{file_path}' erfolgreich dekodieren: {e}"
        )
    


if __name__ == '__main__':
    meineFile = r'C:\Users\User\OneDrive\BachelorArbeitProjekt\InvoiceDashboard\backend\EDIFACT-VAL-main\EDIFACT-VAL-main\example\Anonymized.edi'


    try:
        edi_inhalt = read_edi_file_as_string(meineFile)
        print(edi_inhalt[:500]) 
        print("EDIFACT-Datei erfolgreich gelesen.")
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Fehler beim Lesen der EDIFACT-Datei: {e}")


    x = ediToShacl(edi_inhalt)

    report = x[0]

    finalttl = x[1]

    print("EDIFACT zu SHACL-Konvertierung abgeschlossen.")

    print(finalttl)


