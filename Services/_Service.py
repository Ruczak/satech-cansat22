class Service():   
    _services = {}

    def __init__(self, name: str) -> None:
        self.name = name
        Service.__add_service(self.name, self)

    # private static: adds service to the list of services
    @staticmethod
    def __add_service(name: str, service) -> None:
        Service._services[name] = service
