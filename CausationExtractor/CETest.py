import os
import json
import datetime
from CausationExtractor import CausationExtractor
from SalientArtifact import SalientArtifact

def main():
    test_var_setters_getters()
    #test_list_getters()
    #test_add_salient_artifact()
    #test_load_salient_artifacts()
    #test_import_events()
    #test_output_sorted_by_time_to_json()
    #test_group_by_time()
    #test_group_by_salient_artifacts
    pass

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
    
def test_list_getters():
    pass 
def test_add_salient_artifact():
    pass 
def test_load_salient_artifacts():
    pass 
def test_import_events():
    pass 
def test_output_sorted_by_time_to_json():
    pass 
def test_group_by_time():
    pass 
def test_group_by_salient_artifacts():
    pass

if __name__ == "__main__":
    main()
