import asyncio
from ._Service import Service
import os
import csv


class FileService(Service):
    def __init__(self, name: str, scope: str, log_file='./logs.txt', delimiter=',') -> None:
        Service.__init__(name)
        if isinstance(scope, str) and len(scope) > 0:
            if not os.path.isdir(scope):
                os.mkdir(scope)
            
            os.chdir(scope)
            self.__scope = scope
        else:
            self.__scope = os.getcwd()

        self.log_file = log_file
        self.delimiter = delimiter
    
    # gets current scope of the file system, uses current scope as a context
    @property
    def scope(self) -> str:
        return self.__scope

    # sets current scope of the file system
    @scope.setter
    def scope(self, path: str) -> None:
        if isinstance(path, str) and len(path) > 0:
            os.chdir(path)
            self.__scope = path

    # logs message to file
    async def log(self, message: str):
        try:
            with open(self.log_file, 'a', newline='\r\n') as file:
                file.write(message)
                file.close()
        except asyncio.CancelledError:
            print("Cancelled logging into file.")
            raise

    # adds data rows to specified csv file
    async def add_to_csv(self, path: str, row: dict) -> None:
        try:
            write_header = not os.path.isfile(path) or os.stat(path).st_size == 0

            with open(path, 'a', newline='') as file:
                fields = row.keys()
                writer = csv.DictWriter(file, delimiter=self.delimiter, quotechar="\'", quoting=csv.QUOTE_MINIMAL, fieldnames=fields)

                if write_header:
                    writer.writeheader()

                writer.writerow(row)

                file.close()

            print(f"Added data to csv ({path}, {row})")
        except asyncio.CancelledError:
            print("Cancelled writing to csv file.")
            raise
    

