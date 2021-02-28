class SalientArtifact:

    def __init__(self, type, artifact):
        self._type = type
        self._artifact = artifact

    def get_artifact(self):
        return self._artifact

    def get_type(self):
        return self._type

    def to_str(self):
        return "Type: " + str(self._type) + ", Artifact: " + str(self._artifact)
    
