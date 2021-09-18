import time
from piority_queue import PiorityQueue

# for the piority queue: order is according f-value
def piority_func(queue_list, node):
    queue_list.append(node)
    queue_list.sort(reverse = True, key = lambda node : node.f)

# for the piority queue
def del_elem_func(queue_list, node):
    index = [i for i, elem in enumerate(queue_list) if elem.point == node.point][0] # find the index of the element
    del queue_list[index]

# A star algorithms implementation
def A_star_algo(draw_func, huristic_func , reconstruct_path, grid, start, end):
    # define the open list for the fringe and the close set
    OPEN = PiorityQueue(piority_func, del_elem_func)
    CLOSE = set()
    
    # calculate g,h and f for start node and enqueue to the fringe:
    start.g = 0
    start.f = start.g + huristic_func(start.point, end.point)
    OPEN.enqueue(start)
    
    while not OPEN.isEmpty():
        current_spot = OPEN.Front() # pop the fringe
        CLOSE.add(current_spot)
        
        # check if the goal reached
        if current_spot == end:
            reconstruct_path(draw_func, CLOSE,start, end) 
            return True
    
        for spot in current_spot.neighbors:
            new_g = current_spot.g + 1
            if not spot in CLOSE and not spot in OPEN._queue:
                spot.g = new_g
                spot.f = new_g + huristic_func(spot.point,end.point)
                OPEN.enqueue(spot)
                if spot != start and spot != end:        
                    spot.make_open() # color the spot
            
            elif spot in OPEN._queue:
                if new_g < spot.g: # if so then a better path found
                    spot.g = new_g
                    spot.f = new_g + huristic_func(spot.point,end.point)

            else: # spot belongs to CLOSE
                if new_g < spot.g: # if so then a better path found
                    OPEN.enqueue(spot)
                    CLOSE.remove(spot)

        if current_spot != start:
            current_spot.make_closed() # color the spot to red
        
        draw_func() # color the spots
   
    return False

    


