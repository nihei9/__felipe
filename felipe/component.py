import json

class Component:
    def __init__(self, conf, attributes):
        """
        Parameters
        ----------
        conf : Config
            Configration of component
        attributes : Dict
            Attributes of component
        """

        self.__kind = "component"
        self.__conf = conf
        self.__id = self.__gen_component_id(conf, attributes)
        self.__label = self.__gen_component_label(conf, attributes)
        self.__attributes = attributes
        self.__dependencies = []
        self.__relations = {}
    
    def __gen_component_id(self, conf, attributes):
        arr = [conf.component_type]
        for k in conf.unique_keys:
            v = attributes.get(k) or ""
            arr.append(v)
        
        return "/".join(arr)

    def __gen_component_label(self, conf, attributes):
        arr = []
        for k in conf.label_keys:
            v = attributes.get(k) or ""
            arr.append(v)
        
        return "\\n".join(arr)
    
    @property
    def kind(self):
        return self.__kind
    
    @property
    def component_id(self):
        return self.__id
    
    @property
    def component_type(self):
        return self.__conf.component_type
    
    @property
    def label(self):
        return self.__label
    
    @property
    def attributes(self):
        return self.__attributes
    
    @property
    def dependencies(self):
        return self.__dependencies
    
    @property
    def relations(self):
        return self.__relations
    
    def relate_to(self, component, *relations):
        self.__dependencies.append(component)
        if (not self.__relations.get(component.component_id)):
            self.__relations[component.component_id] = []
        self.__relations[component.component_id].extend(relations)

class Relation:
    def __init__(self, conf, attributes):
        """
        Parameters
        ----------
        conf : Config
            Configration of relation
        attributes : Dict
            Attributes of relation
        """

        self.__conf = conf
        self.__attributes = attributes
    
    @property
    def relation_type(self):
        return self.__conf.relation_type
    
    @property
    def attributes(self):
        return self.__attributes

def load(filename, conf):
    with open(filename, mode = 'r') as f:
        data = json.load(f)
        kind = data.get("kind")
        if (kind != "component"):
            return None
        
        c = Component(conf.components[data["component"]["type"]], data["component"])
        
        for ddata in data["dependencies"]:
            dc = Component(conf.components[ddata["type"]], ddata)
            
            for rdata in ddata["relations"]:
                r = Relation(conf.relations[rdata["type"]], rdata)
                c.relate_to(dc, r)
        
        return c
