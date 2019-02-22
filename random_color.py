import random


def random_color():
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return(color)