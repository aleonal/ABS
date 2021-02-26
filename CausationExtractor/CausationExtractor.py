import json, datetime
from Event import Event, auditd, clicks, keypresses, traffic, trafficThroughput, timed, suricata

class CausationExtractor:

    def __init__(self):
        self._salient_artifacts = []
        self._time_frame = 0
        self._eceld_project_root = ""
        self._output_folder = ""
        self._project_name = ""
        self._event_list = {} # event_list = {type : [obj, obj, obj]}
        self._sorted_by_time = []
        self._grouped_by_salient_artifact = [] #grouped_by_salient_artifact = [[obj_sa1, ob_sa1, obj_sa1], [obj_sa2, obj_sa2]]
        self._grouped_by_time = [] # grouped_by_time = [[obj_group1, ob_group1, obj_group1], [obj_group2, obj_group2]]

    #Setters    
    def set_time_frame(self, t):
        tf = datetime.datetime.strptime(t, '%H:%M:%S')
        self._time_frame = datetime.timedelta(hours=tf.hour, minutes=tf.minute, seconds=tf.second)
    def set_eceld_project_root(self, project_root):
        self._eceld_project_root = project_root
    def set_output_folder(self, output_folder):
        self._output_folder = output_folder
    def set_project_name(self, project_name):
        self._project_name = project_name

    #Getters
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
    
    # adds salient artifact object to list of artifacts
    def add_salient_artifact(self, salient_artifact):
        self._salient_artifacts.append(salient_artifact)
    # removes salient artifact object from list of artifacts
    def remove_salient_artifact(self, artifact):
        for i in range(len(self._salient_artifacts)):
            if self._salient_artifacts[i].get_artifact() == artifact:
                del self._salient_artifacts[i]
                break

    #Import events
    def import_events(self):
        self._import_event("auditd", "/parsed/auditd/auditdData.JSON")
        self._import_event("clicks", "/parsed/pykeylogger/click.JSON")
        self._import_event("keypresses", "/parsed/pykeylogger/keypressData.JSON")
        self._import_event("timed", "/parsed/pykeylogger/timed.JSON")
        self._import_event("traffic", "/parsed/tshark/networkDataAll.JSON")
        self._import_event("trafficThroughput", "/parsed/tshark/networkDataXY.JSON")
        self._import_event("suricata", "")

    def _import_event(self, type, directory):
        try:
            with open(self._eceld_project_root+directory) as f:
                data = json.load(f)
                for d in data:
                    e = d
                    if type == "auditd":
                        obj = auditd(e['auditd_id'], e['content'], "auditd", e['start'])
                    elif type == "clicks":
                        obj = clicks(e['clicks_id'], e['content'], e['type'], e['classname'], e['start'])
                    elif type == "keypresses":
                        obj = keypresses(e['keypresses_id'], e['content'], e['className'], e['start'])
                    elif type == "timed":
                        obj = timed(e["timed_id"], e['type'], e['classname'], e['content'], e['start'])
                    elif type == "traffic":
                        obj = traffic(e['traffic_all_id'], e['content'], e['className'], e['title'], e['start'])
                    elif type == "trafficThroughput":
                        obj = trafficThroughput(e['traffic_xy_id'], e['className'], e['start'], e['y'])
                    elif type == "suricata":
                        obj = suricata(e['suricata_id'], e['suricata_rule_id'], e['content'], e['className'], e['start'])
            if type not in self._event_list:
                self._event_list[type] = [obj]
            else:
                self._event_list[type].append(obj)
        except Exception:
            pass

    def get_event_list(self):
        return self._event_list

    #sort all events by time
    def _sort_by_time(self):
        self._sorted_by_time = []
        for event in self._event_list:
            for obj in self._event_list[event]:
                self._sorted_by_time.append(obj)
        self._sorted_by_time.sort(key=lambda x: x.get_start())
            
    #group all events by time
    #outputs groupings into .JSON files in output folder
    def group_by_time(self):
        self._sort_by_time()
        self._grouped_by_time = [[self._sorted_by_time[0]]]
        index = 0
        for i in range(1, len(self._sorted_by_time)):
            if self._sorted_by_time[i].get_start() - self._sorted_by_time[i-1].get_start() <= self._time_frame:
                self._grouped_by_time[index].append(self._sorted_by_time[i])
            else:
                self._grouped_by_time.append([self._sorted_by_time[i]])
                index += 1
        self._output_to_json(self._grouped_by_time, "timed_" + str(self._time_frame).replace(":", "_"))
    
    def _output_to_json(self, l, type):
        n = 1
        for group in l:
            with open(self._output_folder+"/"+type+"_group" + str(n) + '.JSON', 'w') as json_file:
                for obj in group:
                    json.dump(obj.tojson(), json_file, indent=2)
            n+=1

    #group all events by salient artifacts
    def group_by_salient_artifacts(self):
        self._grouped_by_salient_artifact = [[]]
        index = 0
        for sa in self._salient_artifacts:
            if sa.get_type() in self._event_list:
                for obj in self._event_list[sa.get_type()]:
                    obj_dict = obj.tojson()
                    for element in obj_dict:
                        if type(sa.get_artifact()) == type(obj_dict[element]):
                            try:
                                if sa.get_artifact() in obj_dict[element]:
                                    self._grouped_by_salient_artifact[index].append(obj)
                            except TypeError:
                                if sa.get_artifact() == obj_dict[element]:
                                    self._grouped_by_salient_artifact[index].append(obj)
                            else:
                                pass
            self._grouped_by_salient_artifact.append([])
            self._output_to_json([self._grouped_by_salient_artifact[index]], sa.get_type() + "_" + str(sa.get_artifact())) 
            index += 1
