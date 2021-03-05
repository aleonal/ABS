import json, datetime
from pathlib import Path
from CausationExtractor.SalientArtifact import SalientArtifact

""" This class is based off of the current Causation Extractor class, but only handles project information. Causation Extractor will handle salient artifacts and event grouping.
    This file stores info in project_config so it can be loaded later on.
 """
class ProjectController:
    _time_frame = 0
    _eceld_project_root = ""
    _project_directory = ""
    _project_name = ""
    _project_info = {"time_frame": "", "eceld_root": "", "project_directory": "", "project_name": "",
                          "salient_artifact": ""}

    # Setters
    @classmethod
    def set_project_name(cls, projectname):
        try:
            with open('project_config.JSON', 'r') as f:
                json_data = json.load(f)
                json_data['name'] = projectname
                cls._project_name = projectname
            with open('project_config.JSON', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.JSON")

    @classmethod
    def set_root_directory(cls, root_directory):
        try:
            with open('project_config.JSON', 'r') as f:
                json_data = json.load(f)
                json_data['eceld_root'] = root_directory
                cls._eceld_project_root = root_directory
            with open('project_config.JSON', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.JSON")

    @classmethod
    def set_project_directory(cls, project_directory):
        try:
            with open('project_config.JSON', 'r') as f:
                json_data = json.load(f)
                json_data['project_directory'] = project_directory
                cls._project_directory = project_directory
            with open('project_config.JSON', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.JSON")


    @classmethod
    def set_time_frame(cls,t):
        tf = datetime.datetime.strptime(t, '%H:%M:%S')
        cls._time_frame = datetime.timedelta(hours=tf.hour, minutes=tf.minute, seconds=tf.second)
        try:
            with open('project_config.JSON', 'r') as f:
                json_data = json.load(f)
                json_data['timeframe'] = cls._time_frame
            with open('project_config.JSON', 'w') as f:
                f.write(json.dumps(json_data))
        except FileNotFoundError:
            print("Could not locate file project_config.JSON")


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
    def get_project_info(cls):
        cls._project_info["time_frame"] = str(cls._time_frame)
        cls._project_info["eceld_root"] = cls._eceld_project_root
        cls._project_info["project_directory"] = cls._project_directory
        cls._project_info["project_name"] = cls._project_name
        count = 1
        for sa in cls._salient_artifacts:
            cls._project_info["salient_artifact"] += (str(count) + ") " + sa.to_str() + "\n")
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
    def load_salient_artifacts_objects(cls):
        fileObject = open("/testRoot/salientArtifacts.JSON", "r")
        jsonContent = fileObject.read()
        tempList = json.loads(jsonContent)
        for artifact in tempList:
            newArtifact = SalientArtifact(artifact['type'], artifact['content'])
            add_salient_artifact(newArtifact)

    @classmethod
    def get_salient_artifacts_json(cls):
        try:
            full_directory = Path(cls._project_directory)
            with open(full_directory / 'salientArtifacts.JSON', 'r') as fileObject:
                jsonContent = fileObject.read()
                artifactList = json.loads(jsonContent)
            return artifactList
        except FileNotFoundError:
            print("Could not locate file salientArtifacts.JSON")
            return []

    @classmethod
    def load_project(cls, directory):
        full_directory = Path(directory)
        # TODO: Check that directory contains project_config, salientArtifacts and other files before loading
        try:
            with open(full_directory / 'project_config.JSON', 'r') as f:
                json_data = json.load(f)
                cls._time_frame = json_data['timeframe']
                cls._eceld_project_root = json_data['eceld_root']
                cls._project_directory = json_data['project_directory']
                cls._project_name = json_data['name']

        except FileNotFoundError:
            print("File not found")

    @classmethod
    def create_project(cls, eceld_root, project_directory, project_name, timeframe):
    # set all variables
        cls._time_frame = timeframe
        cls._eceld_project_root = eceld_root
        cls._project_directory = project_directory
        cls._project_name = project_name

        #create directory in file system

        #create a new project file in the directory and appennd json object
        try:
            with open('project_config.JSON', 'w') as f:
                f.write(json.dumps(json_data))
                #need to update all components with current project info

        except FileNotFoundError:
            print("Error")






