import os
import json
import datetime
from CausationExtractor import CausationExtractor
from SalientArtifact import SalientArtifact

def main():
    ce = CausationExtractor()

    # Change the directories
    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\ECELd_Project\ecel-export_16046064")
    ce.set_output_folder(r"C:\Users\valma\OneDrive\Desktop\TestOutputCE")
    
    ce.import_events()

    # Groups by time
    ce.set_time_frame('00:00:02')
    ce.group_by_time() # Outputs timed groups in JSON files in output folder
    
    # Groups by salient artifact
    ce.add_salient_artifact(SalientArtifact("clicks", "desktop"))
    ce.add_salient_artifact(SalientArtifact("auditd", "localuser"))
    ce.add_salient_artifact(SalientArtifact("keypresses", "Return"))
    ce.add_salient_artifact(SalientArtifact("traffic", "icmp"))
    ce.add_salient_artifact(SalientArtifact("trafficThroughput", 129))
    ce.add_salient_artifact(SalientArtifact("traffic", "172.217.12.78"))
    ce.add_salient_artifact(SalientArtifact("traffic", "tcp"))
    ce.group_by_salient_artifacts() # Outputs salient artifacts into json files in output folder
    

'''
    # Test setter/getter for time_frame
    ce.set_time_frame(5)
    print(ce.get_time_frame())


    # Test setter/getter for eceld_project_root
    # note: remove one slash
    ce.set_eceld_project_root(r"C:\\Users\\valma\\OneDrive\\Desktop")
    print("print", ce.get_eceld_project_root())   

    path = ce.get_eceld_project_root()
    path = os.path.realpath(path)
    os.startfile(path)

    # Test setter/getter for output_folder
    # note: remove one slash
    ce.set_output_folder(r"C:\\Users\\valma\\OneDrive\\Desktop\\TestCE")
    print("print", ce.get_output_folder())

    path = ce.get_output_folder()
    path = os.path.realpath(path)
    os.startfile(path)

    # Test setter/getter for project_name
    ce.set_project_name("TestCE")
    print(ce.get_project_name())

    # Test get sa
    print(ce.get_salient_artifacts())

    # Test add/delete salient_artifact
    for a in ce.get_salient_artifacts():
        print(a)
    ce.add_salient_artifact(SalientArtifact("click", "terminal"))
    ce.add_salient_artifact(SalientArtifact("traffic", "tcp"))
    print("added terminal and tcp")
    for a in ce.get_salient_artifacts():
        print(a.get_description())
    ce.remove_salient_artifact("test1")
    print("removed test1")
    for a in ce.get_salient_artifacts():
        print(a.get_description())


    #Test import events and get events
    ce.set_eceld_project_root(r"C:\\Users\valma\\OneDrive\\Desktop\\TestCE")

    #imports events
    ce.import_events("auditdData.JSON")
    ce.import_events("click.JSON")
    ce.import_events("keypressData.JSON")
    ce.import_events("networkDataAll.JSON")
    ce.import_events("networkDataXY.JSON")
    ce.import_events("timed.JSON")

    
    # prints all events in events list
    event_list = ce.get_event_list()
    for event in event_list:
        for obj in event_list[event]:
            print(event, obj.get_id(), obj.get_start())



'''
if __name__ == "__main__":
    main()