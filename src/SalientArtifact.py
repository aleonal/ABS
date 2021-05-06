class SalientArtifact:

    def __init__(self, type, artifact):
        self._type = type
        self._artifact = artifact

    # This is the key word that the user is looking for within the event type
    def get_artifact(self):
        return self._artifact

    # Event type can be auditd, clicks, keypresses, traffic, trafficThroughput or Suricata
    def get_type(self):
        return self._type

    # Returns a string description of the salient artifact object
    def to_str(self):
        return "Type: " + str(self._type) + ", Artifact: " + str(self._artifact)
    
