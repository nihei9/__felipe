class Config:
    def __init__(self, ctype, base, unique_keys, label_keys, appearance):
        self.__type = ctype
        self.__base = base
        self.__unique_keys = unique_keys
        self.__label_keys = label_keys
        self.__appearance = appearance
    
    @property
    def component_type(self):
        return self.__type
    
    @property
    def base(self):
        return self.__base
    
    @property
    def unique_keys(self):
        return self.__unique_keys
    
    @property
    def label_keys(self):
        return self.__label_keys
    
    @property
    def appearance(self):
        return self.__appearance

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
