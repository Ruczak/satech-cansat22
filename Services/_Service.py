class Service():   
    _services = {}

    def __init__(self, name: str) -> None:
        self.name = name
        Service.__addService()

    @staticmethod
    def __addService(name, service) -> None:
        Service._services[name] = service