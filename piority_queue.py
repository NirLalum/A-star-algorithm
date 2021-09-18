# implementations of different generic queues queues

class PiorityQueue():

    # piority_func args: list, node
    # find_elem_func args: list, node
    def __init__(self, piority_func, del_elem_func):  
        self._queue = []
        self._piority_func = piority_func
        self._del_elem_func = del_elem_func

    # enqueue the new node according to the user supllied function piority_func
    def enqueue(self, new_node) -> bool:
        self._piority_func(self._queue, new_node)
    
    # remove a node
    def dequeue(self, removed_node) -> bool:
        self._del_elem_func(self._queue, removed_node)

    # get the highest piority node
    def Front(self):
        return self._queue.pop()
    
    # get the lowest piority node
    def Rear(self):
        return self._queue.pop(0)

    # check if queue is empty
    def isEmpty(self):
        if not self._queue:
            return True
        else:
            return False


    
