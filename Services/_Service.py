class Service():   
    _services = {}

    def __init__(self, name: str) -> None:
        self.name = name
        Service.__addService(self.name, self)

    @staticmethod
    def __addService(name: str, service) -> None:
        Service._services[name] = service