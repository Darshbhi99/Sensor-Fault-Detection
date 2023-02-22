class TargetValueMapping:
    def __init__(self):
        self.neg:int = 0
        self.pos:int = 1

    def to_dict(self)->dict:
        return self.__dict__
    
    def reverse_mapping(self) -> dict:
        mapping_response:dict = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))

class SensorModel:
    def __init__(self):
        pass

    def bestModel(self) ->dict:
        summary = {}
        return summary