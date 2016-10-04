import simpy

def create_queue_list(env,num_resources,resource_capacity):
    """This function creates a list with two different resources,
    each with a given capacity for expansion technologies"""

    list_of_resources = [simpy.Resource(env,resource_capacity) for res in range(num_resources)]
        
    return list_of_resources