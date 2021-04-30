import json, datetime
import os
import pathlib

from pathlib import Path
from src.SalientArtifact import SalientArtifact
from src.Event import *


""" This class is based off of the current Causation Extractor class, but only handles project information. Causation Extractor will handle salient artifacts and event grouping.
    This file stores info in project_config so it can be loaded later on.
 """
class ProjectController:
    _time_frame = 0
    _eceld_project_root = ""
    _project_directory = ""
    _project_name = ""
    _dependencies_file = ""
    _project_info = {"time_frame": "", "eceld_root": "", "project_directory": "", "project_name": "", "dependencies_file": "",
                          "salient_artifacts": []}
    _salient_artifacts = []
    _artifact_color = "#FF0000"

    # Setters
    @classmethod
    def set_project_name(cls, projectname):
        try:
            with open('project_config.json', 'r') as f:
                json_data = json.load(f)
                json_data['project_name'] = projectname
                cls._project_name = projectname
            with open('project_config.json', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.json")

    @classmethod
    def set_root_directory(cls, root_directory):
        try:
            with open('project_config.json', 'r') as f:
                json_data = json.load(f)
                json_data['eceld_root'] = root_directory
                cls._eceld_project_root = root_directory
            with open('project_config.json', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.json")

    @classmethod
    def set_project_directory(cls, project_directory):
        try:
            with open('project_config.json', 'r') as f:
                json_data = json.load(f)
                json_data['project_directory'] = project_directory
                cls._project_directory = Path(project_directory)
            with open('project_config.json', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.json")


    @classmethod
    def set_time_frame(cls,t):
        tf = cls.parse_timestamp(t)
        cls._time_frame = datetime.timedelta(hours=tf.hour, minutes=tf.minute, seconds=tf.second)
        try:
            with open('project_config.json', 'r') as f:
                json_data = json.load(f)
                json_data['time_frame'] = cls._time_frame
            with open('project_config.json', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.json")
    
    @classmethod
    def set_artifact_color(cls, artifact_color):
        cls._artifact_color = artifact_color

    @classmethod
    def set_dependencies_file(cls, file_path):
        cls._dependencies_file = file_path

    # Getters
    @classmethod
    def get_salient_artifacts(cls):
        return cls._salient_artifacts

    @classmethod
    def get_time_frame(cls):
        return cls._time_frame

    @classmethod
    def get_eceld_project_root(cls):
        return cls._eceld_project_root

    @classmethod
    def get_project_directory(cls):
        return cls._project_directory

    @classmethod
    def get_project_name(cls):
        return cls._project_name

    @classmethod
    def get_artifact_color(cls):
        return cls._artifact_color

    @classmethod
    def get_dependencies_file(cls):
        return cls._dependencies_file

    @classmethod
    def get_project_info(cls):
        cls._project_info["time_frame"] = str(cls._time_frame)
        cls._project_info["eceld_root"] = cls._eceld_project_root
        cls._project_info["project_directory"] = cls._project_directory
        cls._project_info["project_name"] = cls._project_name
        cls._project_info["dependencies_file"] = cls._dependencies_file
        
        count = 1
        for sa in cls._salient_artifacts:
            cls._project_info["salient_artifacts"].append((str(count) + ") " + sa.to_str()))
            count += 1
        return cls._project_info

    @classmethod
    def is_project_loaded(cls):
        if (cls._project_directory != ""):
            return True
        return False

    # adds salient artifact object to list of artifacts
    @classmethod
    def add_salient_artifact(cls, salient_artifact):
        cls._salient_artifacts.append(salient_artifact)

    # removes salient artifact object from list of artifacts
    @classmethod
    def remove_salient_artifact(cls, artifact):
        for i in range(len(cls._salient_artifacts)):
            if cls._salient_artifacts[i].get_artifact() == artifact:
                del cls._salient_artifacts[i]
                break
    
    @classmethod
    def get_salient_artifacts_json(cls):
        try:
            full_directory = Path(cls._project_directory)
            with open(full_directory / 'salientArtifacts.json', 'r') as fileObject:
                jsonContent = fileObject.read()
                artifactList = json.loads(jsonContent)
            return artifactList
        except FileNotFoundError:
            print("Could not locate file salientArtifacts.json")
            return []

    @classmethod
    def load_salient_artifacts_objects(cls):
        try:
            with open(cls._project_directory / 'salientArtifacts.json', 'r') as f:
                artifacts = json.load(f)

                for item in artifacts:
                    artifact = SalientArtifact(item['type'], item['artifact'])
                    ProjectController.add_salient_artifact(artifact)
        except FileNotFoundError as err:
            raise FileNotFoundError("Salient Artifacts file not found")

                
    @classmethod
    def load_project(cls, directory):
        
        full_directory = Path(directory)
        print(full_directory)
        try:
            with open(full_directory / 'project_config.json', 'r') as f:

                # check if file is project config
                #if directory.split("/")[-1] != "project_config.json":
                #    raise TypeError("Not a project configuration file")

                json_data = json.load(f)
                cls._time_frame = json_data['time_frame']
                cls._eceld_project_root = json_data['eceld_root']
                cls._project_name = json_data['project_name']
                if 'dependencies_file' in json_data.keys():
                    cls._dependencies_file = json_data['dependencies_file']

                # project root is based on the directory of "project_config", so I made it so it works in any directory
                cls._project_directory = full_directory
            
            # load salient artifacts
            ProjectController.load_salient_artifacts_objects()

        except FileNotFoundError:
            raise FileNotFoundError("Project Configuration file not found")
        except TypeError:
            raise TypeError("Not a project configuration file")

    @classmethod
    def create_project(cls, eceld_root, project_directory, project_name, timeframe):
    # set all variables
        cls._time_frame = timeframe
        cls._eceld_project_root = eceld_root
        cls._project_directory = Path(project_directory)
        cls._project_name = project_name
        cls._dependencies_file = ""

        #Create project_config file
        data = {}
        data['project_name'] = cls._project_name
        data['project_root'] = str(cls._project_directory)
        data['eceld_root'] = str(cls._eceld_project_root)
        data['time_frame'] = cls._time_frame
        data['dependencies_file'] = cls._dependencies_file
        base_dir = cls._project_directory
        filename = r'project_config.json'
        fullfilename = os.path.join(base_dir, filename)
        with open(fullfilename, 'w') as outfile:
            json.dump(data, outfile)
        # Checks if salientArtifacts.json file exists before creating an empty one
        filename = r'salientArtifacts.json'
        fullfilename = os.path.join(base_dir, filename)
        file = pathlib.Path(fullfilename)
        if not file.exists():
            #Create empty salientArtifacts file
            data = []
            filename = r'salientArtifacts.json'
            fullfilename = os.path.join(base_dir, filename)
            with open(fullfilename, 'w') as outfile:
                json.dump(data, outfile)
        ProjectController.load_salient_artifacts_objects()

        #Create events folder
        events_directory = r'events'
        full_path = os.path.join(base_dir, events_directory)
        try:
            os.mkdir(full_path)
        except OSError as error:
            print(error)


        ProjectController.load_salient_artifacts_objects()

    #TODO: We should maybe remove this method. create project will handle all this.
    @classmethod
    def save_project(cls):
        data = {}
        data['project_name'] = cls._project_name
        data['project_root'] = str(cls._project_directory)
        data['eceld_root'] = str(cls._eceld_project_root)
        data['time_frame'] = cls._time_frame
        if cls._dependencies_file is not None:
            data['dependencies_file'] = cls._dependencies_file
        base_dir = cls._project_directory
        filename = r'project_config.json'
        fullfilename = os.path.join(base_dir, filename)
        with open(fullfilename, 'w') as outfile:
            json.dump(data, outfile)
        return 0
    
    #Writes salient artifacts list to salientArtifacts.json
    @classmethod
    def overwrite_salient_artifacts(cls, artifactsList):
        filename = r'salientArtifacts.json'
        fullfilename = os.path.join(cls._project_directory, filename)
        file = pathlib.Path(fullfilename)

        try:
            with open(file, 'w') as outfile:
                json.dump(artifactsList, outfile)
        except FileNotFoundError:
            print("Could not locate salientArtifacts.json")
            
    @classmethod
    def parse_timestamp(cls, timestamptStr):
        formats = {'%H:%M:%S','%H:%M:%S.%f','%Y-%m-%dT%H:%M:%S','%Y/%m/%dT%H:%M:%S', '%d/%m/%YT%H:%M:%S', '%m/%d/%YT%H:%M:%S','%Y-%m-%dT%H:%M:%S.%f','%Y/%m/%dT%H:%M:%S.%f', '%d/%m/%YT%H:%M:%S.%f', '%m/%d/%YT%H:%M:%S.%f'}
        for format in formats:
            try:
                time = datetime.datetime.strptime(timestamptStr, format)
                return time
            except:
                print(format + " format does not match " + timestamptStr)

    # Loads events from timed groups, assuming that's the only files in the folder
    @classmethod
    def load_event_list(cls):
        try:
            timed_groups = []

            for file in os.listdir(cls._project_directory  / 'events'):
                event_list = {}

                with open(os.path.join(cls._project_directory  / 'events', file), 'r') as f:
                    events = json.load(f)

                    for e in events:
                        k = list(e.keys())

                        if 'auditd_id' in k:
                            obj = Auditd(e['auditd_id'], e['content'], "auditd", e['start'])
                        elif 'clicks_id' in k:
                            obj = Clicks(e['clicks_id'], e['content'], e['type'], e['classname'], e['start'])
                        elif 'keypresses_id' in k:
                            obj = Keypresses(e['keypresses_id'], e['content'], e['className'], e['start'])
                        elif 'timed_id' in k:
                            obj = Timed(e["timed_id"], e['type'], e['classname'], e['content'], e['start'])
                        elif 'traffic_all_id' in k:
                            obj = Traffic(e['traffic_all_id'], e['content'], e['className'], e['title'], e['start'])
                        elif 'traffic_xy_id' in k:
                            obj = TrafficThroughput(e['traffic_xy_id'], e['className'], e['start'], e['y'])
                        elif 'suricata_id' in k:
                            obj = Suricata(e['suricata_id'], e['suricata_rule_id'], e['content'], e['className'], e['start'])
                        
                        if k[0] not in event_list:
                            event_list[k[0]] = [obj]
                        else:
                            event_list[k[0]].append(obj)
                            
                timed_groups.append(events)
            
            return timed_groups     
        except FileNotFoundError as err:
            raise FileNotFoundError("Error loading event lists!")
