from ._Service import Service
from EventBus import EventBus
from Events.UpdateCsvEvent import UpdateCsvEvent
import os
import csv


class FileService(Service):
    def __init__(self, name: str, scope: str) -> None:
        super(FileService, self).__init__(name)
        if isinstance(scope, str) and len(scope) > 0:
            if not os.path.isdir(scope):
                os.mkdir(scope)
            
            os.chdir(scope)
            self.__scope = scope
        else:
            self.__scope = os.getcwd()
    
    # defines the scope of the file system, uses current scope as a context
    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, path: str) -> None:
        if isinstance(path, str) and len(path) > 0:
            os.chdir(path)
            self.__scope = path

    # adds data rows to .csv file specified with path
    def addToCsv(self, path: str, row: dict, delimiter: str = ',') -> None:
        writeHeader = not os.path.isfile(path) or os.stat(path).st_size == 0

        with open(path, 'a', newline='') as file:
            fields = row.keys()
            writer = csv.DictWriter(file, delimiter=delimiter, quotechar="\'", quoting=csv.QUOTE_MINIMAL, fieldnames=fields)

            if writeHeader:
                writer.writeheader()

            writer.writerow(row)

            file.close()

    

