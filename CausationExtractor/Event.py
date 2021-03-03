import datetime

class Event:
    def __init__(self):
        self._id = 0
        self._content = ""
        self._className = ""
        self._start = None
    
    def set_id(self,id):
        self._id = id 
    def get_id(self):
        return self._id 

    def set_content(self,content):
        self._content = content 
    def get_content(self):
        return self._content 

    def set_className(self, className):
        self._className = className 
    def get_className(self):
        return self._className 
    
    def set_start(self, start):
        self._start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    def get_start(self):
        return self._start
    def get_start_tostring(self):
        return self._start.strftime("%m/%d/%YT%H:%M:%S")

class Auditd(Event):
    def __init__(self, id, content, className, start):
        self.set_id(id)
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
    def tojson(self):
        return {'auditd_id' : self.get_id(), 'content' : self.get_content(), 'className' : self.get_className(), 'start' : self.get_start_tostring()}

class Clicks(Event):
    def __init__(self, id, content, type, className, start):
        self.set_id(id)
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
        self._type = type
    def get_type(self):
        return self._type
    def tojson(self):
        return {'clicks_id' : self.get_id(), 'content' : self.get_content(), 'type' : self.get_type(), 'classname' : self.get_className(), 'start' : self.get_start_tostring()}

class Keypresses(Event):
    def __init__(self, id, content, className, start):
        self.set_id(id)
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
    def tojson(self):
        return {'keypresses_id' : self.get_id(), 'content' : self.get_content(), 'className' : self.get_className(), 'start' : self.get_start_tostring()}

class Traffic(Event):
    def __init__(self, id, content, className, title, start):
        self.set_id(id)
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
        self._title = title
    def get_title(self):
        return self._title
    def tojson(self):
        return {'traffic_all_id' : self.get_id(), 'content' : self.get_content(), 'className' : self.get_className(), 'title' : self.get_title(), 'start' : self.get_start_tostring()}

class TrafficThroughput(Event):
    def __init__(self, id, className, start, y):
        self.set_id(id)
        self.set_className(className)
        self.set_start(start)
        self._y = y
    def get_y(self):
        return self._y
    def tojson(self):
        return {'traffic_xy_id' : self.get_id(), 'className' : self.get_className(), 'start' : self.get_start_tostring(), 'y' : self.get_y()}

class Timed(Event):
    def __init__(self, id, type, className, content, start):
        self.set_id(id)
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
        self._type = type 
    def get_type(self):
        return self._type
    def tojson(self):
        return {'timed_id' : self.get_id(), 'type' : self.get_type(), 'classname' : self.get_className(), 'content' : self.get_content(), 'start' : self.get_start_tostring()}

class Suricata(Event):
    def __init__(self, id, rule, content, className, start):
        self.set_id(id)
        self._rule = rule
        self.set_content(content)
        self.set_className(className)
        self.set_start(start)
    def get_rule(self):
        return self._rule
    def tojson(self):
        return {"suricata_id" : self.get_id(), "suricata_rule_id" : self.get_rule(), "content" : self.get_content(), "className" : self.get_className(), "start" : self.get_start_tostring()}
   