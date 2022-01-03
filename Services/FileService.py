from _Service import Service
import os
import csv

class FileService(Service):
    def __init__(self, name: str, scope: str) -> None:
        super(FileService, self).__init__(name)
        if isinstance(scope, str) and len(scope) > 0:
            os.chdir(scope)
            self.__scope = scope
        else:
            self.__scope = os.getcwd()
        
    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, path: str) -> None:
        if isinstance(path, str) and len(path) > 0:
            os.chdir(path)
            self.__scope = path

    def addToCsv(self, path: str, data: list[dict], delimiter: str = '|') -> None:
        writeHeader = not os.path.isfile(path) or os.stat(path).st_size == 0
        with open(path, newline='') as file:
            fields = data[0].keys()
            writer = csv.DictWriter(file, delimiter, quotechar="\'", quoting=csv.QUOTE_MINIMAL, fieldnames=fields)

            if writeHeader:
                writer.writeheader()

            for row in data:
                writer.writerow(row)

    

