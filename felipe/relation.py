class Config:
    def __init__(self, rtype, base, direction, appearance):
        self.__type = rtype
        self.__base = base
        self.__direction = direction
        self.__appearance = appearance
    
    @property
    def relation_type(self):
        return self.__type
    
    @property
    def base(self):
        return self.__base
    
    @property
    def direction(self):
        return self.__direction
    
    @property
    def appearance(self):
        return self.__appearance

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
