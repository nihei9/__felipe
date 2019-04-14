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
