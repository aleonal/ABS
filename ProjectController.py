import json, datetime
from pathlib import Path

""" This class is based off of the current Causation Extractor class, but only handles project information. Causation Extractor will handle salient artifacts and event grouping.
    This file stores info in project_config so it can be loaded later on.
 """
class ProjectController:

    def __init__(self):

        self._time_frame = 0
        self._eceld_project_root = ""
        self._output_folder = ""
        self._project_name = ""
        self._project_info = {"time_frame": "", "project_root": "", "output_folder": "", "project_name": "",
                              "salient_artifact": ""}

    # Setters
    def set_project_name(self, projectname):
        with open('project_config.JSON', 'r') as f:
            json_data = json.load(f)
            json_data['name'] = projectname
            self._project_name = projectname
        with open('project_config.JSON', 'w') as f:
            f.write(json.dumps(json_data))

    def set_root_directory(self, root_directory):
        with open('project_config.JSON', 'r') as f:
            json_data = json.load(f)
            json_data['eceld_root'] = root_directory
            self._eceld_project_root = root_directory
        with open('project_config.JSON', 'w') as f:
            f.write(json.dumps(json_data))

    def set_output_directory(self, output_directory):
        with open('project_config.JSON', 'r') as f:
            json_data = json.load(f)
            json_data['output_directory'] = output_directory
            self._output_folder = output_directory
        with open('project_config.JSON', 'w') as f:
            f.write(json.dumps(json_data))

    def set_time_frame(self, t):
        tf = datetime.datetime.strptime(t, '%H:%M:%S')
        self._time_frame = datetime.timedelta(hours=tf.hour, minutes=tf.minute, seconds=tf.second)
        with open('project_config.JSON', 'r') as f:
            json_data = json.load(f)
            json_data['timeframe'] = self._time_frame
        with open('project_config.JSON', 'w') as f:
            f.write(json.dumps(json_data))

    # Getters
    def get_salient_artifacts(self):
        return self._salient_artifacts

    def get_time_frame(self):
        return self._time_frame

    def get_eceld_project_root(self):
        return self._eceld_project_root

    def get_output_folder(self):
        return self._output_folder

    def get_project_name(self):
        return self._project_name

    def get_project_info(self):
        self._project_info["time_frame"] = str(self._time_frame)
        self._project_info["project_root"] = self._eceld_project_root
        self._project_info["output_folder"] = self._output_folder
        self._project_info["project_name"] = self._project_name
        count = 1
        for sa in self._salient_artifacts:
            self._project_info["salient_artifact"] += (str(count) + ") " + sa.to_str() + "\n")
            count += 1
        return self._project_info

    # adds salient artifact object to list of artifacts
    def add_salient_artifact(self, salient_artifact):
        self._salient_artifacts.append(salient_artifact)

    # removes salient artifact object from list of artifacts
    def remove_salient_artifact(self, artifact):
        for i in range(len(self._salient_artifacts)):
            if self._salient_artifacts[i].get_artifact() == artifact:
                del self._salient_artifacts[i]
                break

    def load_salient_artifacts(self):
        fileObject = open("/home/kali/Desktop/practicum/testRoot/salientArtifacts.JSON", "r")
        jsonContent = fileObject.read()
        tempList = json.loads(jsonContent)
        for artifact in tempList:
            newArtifact = SalientArtifact(artifact['type'], artifact['content'])
            self.add_salient_artifact(newArtifact)

    def load_project(self, directory):
        full_directory = Path(directory)
        # return dictionary with information from loaded JSON
        with open(full_directory / 'project_config.JSON', 'r') as f:
            json_data = json.load(f)
            self._time_frame = json_data['timeframe']
            self._eceld_project_root = json_data['eceld_root']
            self._output_folder = json_data['output_directory']
            self._project_name = json_data['name']
            #need to update all components with current project info, maybe a reload function or something?

    def create_project(self, eceld_root, output_directory, project_name, timeframe):
    # set all variables
        self._time_frame = timeframe
        self._eceld_project_root = eceld_root
        self._output_folder = output_directory
        self._project_name = project_name

        #create directory in file system

        #create a new project file in the directory and appennd json object
        with open('project_config.JSON', 'w') as f:
            f.write(json.dumps(json_data))
            #need to update all components with current project info





