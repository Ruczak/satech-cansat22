class Service():   
    _services = {}

    def __init__(self, name):
        self.name = name
        Service.__addService()

    @staticmethod
    def __addService(name, service):
        Service._services[name] = service