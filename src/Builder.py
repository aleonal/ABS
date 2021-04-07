    import json
import datetime
from .Event import Event, Auditd, Clicks, Keypresses, Traffic, TrafficThroughput, Timed, Suricata
from .SalientArtifact import SalientArtifact
from .ProjectController import ProjectController

class Builder:
    def __init__(self):
        self.project_data = ProjectController.get_project_info()
        self.events = ProjectController.load_event_list()
        self.dependencies = DependencyTree()

    # SORTING FUNCTIONS CAN PROBABLY BE IMPLEMENTED IN THE FRONTEND? TALK ABOUT THIS

    #TODO: sort events by salient artifacts
    def sort_by_salient_artifacts(self):
        raise NotImplementedError

    #TODO: sort events by timeframe, in milliseconds. 2000 is default.
    def sort_by_timeframe(self, timeframe=2000):
        raise NotImplementedError
        
    #TODO: given a keyword, return a lsit of events that contain the keyword.
    #      This can be turned into a 'highlight events with keyword' type of thing in front-end, idk
    def filter_by_keyword(self, keyword):
        raise NotImplementedError

    #TODO: create script based on dependencies
    def create_script(self):
        raise NotImplementedError

class Dependency:
    def __init__(self, event):
        self.event = event
        self.dependencies = DependencyTree()

class DependencyTree:
    def __init__(self):
        self.dependencies = []

    # when user removes an event as a dependency, delete it and make children standalone dependencies if any
    def delete_dependency(self, dependency):
        if isinstance(dependency, Dependency):
            for response in dependency.response_list:
                self.dependencies.append(response)

            list.remove(dependency)
        else:
            raise TypeError("Object is not a dependency. Please check object type.")
        
    # Appends given dependency to tree
    def add_dependency(self, dependency):
        if isinstance(dependency, Dependency):
            self.dependencies.append(dependency)
        else:
            raise TypeError("Object is not a dependency. Please check object type.")

    # If a user wants to move the dependency to another slot, call this method with the dependency and the index (from GUI) of where it's to be placed
    def move_dependency(self, dependency, index):
        self.dependencies.insert(index, self.dependencies.remove(dependency))

    # Wrapper for sorting by time
    def sort_by_time(self):
        self.dependencies.sort(key=lambda dependency: dependency.event.get_start)
    
