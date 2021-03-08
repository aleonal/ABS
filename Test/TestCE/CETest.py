import os
import json
import datetime
from CausationExtractor import CausationExtractor
from SalientArtifact import SalientArtifact

def main():
    test_var_setters_getters()
    test_artifacts()
    test_import_events()
    test_output_sorted_by_time_to_json()
    test_group_by_time()
    test_group_by_salient_artifacts()

def test_var_setters_getters():
    ce = CausationExtractor()

    ce.set_time_frame("00:00:2")
    ce.set_eceld_project_root('C:/Test_Root')
    ce.set_output_folder('C:/Test_Output')
    ce.set_project_name("Test Name")

    if ce.get_time_frame() != datetime.timedelta(hours=0, minutes=0, seconds=2):
        print("set_time_frame: FAIL")
    else:
        print("set_time_frame: PASS")

    if ce.get_eceld_project_root() != 'C:/Test_Root':
        print("set_eceld_project_root: FAIL")
    else:
        print("set_eceld_project_root: PASS")

    if ce.get_output_folder() != 'C:/Test_Output':
        print("set_output_folder: FAIL")
    else:
        print("set_output_folder: PASS")

    if ce.get_project_name() != "Test Name":
        print("set_project_name: FAIL")
    else:
        print("set_project_name: PASS")
    
def test_artifacts():
    #(!) ENSURE salientArtifacts.JSON is in root directory and contains [{"type" : "traffic", "artifact" : "icmp"}, {"type" : "clicks", "artifact" : "terminal"}]
    ce = CausationExtractor()

    ce.add_salient_artifact(SalientArtifact("clicks", "desktop"))
    ce.add_salient_artifact(SalientArtifact("traffic", "tcp"))
    sa_l = ce.get_salient_artifacts()

    if sa_l[0].get_type() != "clicks":
        print("salient_artifact list: FAIL")
    if sa_l[0].get_artifact() != "desktop":
        print("salient_artifact list: FAIL")
    if sa_l[1].get_type() != "traffic":
        print("salient_artifact list: FAIL")
    if sa_l[1].get_artifact() != "tcp":
        print("salient_artifact list: FAIL")
    else:
        print("salient_artifact list: PASS")

    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.load_salient_artifacts()
    sa_l2 = ce.get_salient_artifacts()

    if sa_l2[2].get_type() != "traffic":
        print("load salient artifacts: FAIL")
    if sa_l2[2].get_artifact() != "icmp":
        print("load salient artifacts: FAIL")
    if sa_l2[3].get_type() != "clicks":
        print("load salient artifacts: FAIL")
    if sa_l2[3].get_artifact() != "terminal":
        print("load salient artifacts: FAIL")
    else:
        print("load salient artifacts: PASS")
    
def test_import_events():
    ce = CausationExtractor()

    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.import_events()

    e_l = ce.get_event_list()

    if len(e_l["auditd"]) != 9:
        print("import_events() auditd: FAIL")
    if len(e_l["clicks"]) != 19:
        print("import_events() clicks: FAIL")
    if len(e_l["keypresses"]) != 5:
        print("import_events() keypresses: FAIL")
    if len(e_l["timed"]) != 4:
        print("import_events() timed: FAIL")
    if len(e_l["traffic"]) != 18:
        print("import_events() traffic: FAIL")
    if len(e_l["trafficThroughput"]) != 18:
        print("import_events() trafficThroughput: FAIL")
    if len(e_l["suricata"]) != 2:
        print("import_events() suricatad: FAIL")
    else:
        print("import_events(): PASS")

def test_output_sorted_by_time_to_json():
    ce = CausationExtractor()

    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.set_output_folder(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.import_events()
    ce.output_sorted_by_time_to_json()

    print("Check test folder for eventsSortedByTime.JSON and check if contents are sorted by time")

def test_group_by_time():
    ce = CausationExtractor()
    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.set_output_folder(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.import_events()
    ce.set_time_frame("00:00:02")
    ce.group_by_time()
    print("Check test folder for 6 groupings by 00:00:02 seconds")

def test_group_by_salient_artifacts():
    ce = CausationExtractor()
    ce.set_eceld_project_root(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.set_output_folder(r"C:\Users\valma\OneDrive\Desktop\TestABS\TestCE")
    ce.import_events()
    ce.add_salient_artifact(SalientArtifact("traffic", "tcp"))
    ce.add_salient_artifact(SalientArtifact("keypresses", "Return"))
    ce.group_by_salient_artifacts()
    print("Check test folder for traffic tcp and keypreses Return salient artifact groupings")
  

if __name__ == "__main__":
    main()
