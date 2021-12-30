class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __del__(self):
        print(f"Event removed at {id(self.value)}")


    
