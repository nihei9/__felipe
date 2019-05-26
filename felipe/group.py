from . import component
import json

class Group:
    def __init__(self):
        self.__kind = "group"
        self.__components = {}
    
    def append(self, component):
        self.__components[component.component_id] = component
    
    @property
    def kind(self):
        return self.__kind
    
    @property
    def components(self):
        return self.__components

def load(filename, conf):
    with open(filename, mode = 'r') as f:
        data = json.load(f)
        kind = data.get("kind")
        if (kind != "group"):
            return None
        
        g = Group()

        for cdata in data["group"]["components"]:
            c = component.Component(conf.components[cdata["type"]], cdata)
            g.append(c)
        
        return g
