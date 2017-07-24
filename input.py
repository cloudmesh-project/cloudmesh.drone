import re

def get_input():
    while True:
        cur_input = input("[drone command]> ")
        
        m = re.match('^move to ([0-9]+),([0-9]+),([0-9]+)', cur_input)
        if(m):
            x, y, z = m.group(1, 2, 3)
            print(x,y,z)

            # check bounds of input
            check_bounds(x, y, z)
            
            return
        elif(cur_input == 'land'):
            return
        else:
            continue
            
get_input()
