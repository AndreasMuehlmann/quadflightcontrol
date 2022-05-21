from random import random
import time
import os


path = os.path.join('/home', 'andi', 'interface_sim-control', 'measurements.txt')
while True:
    try:
        with open(path, 'w') as file:
            time.sleep(1/100)
            for i in range(4):
                file.write(f'{random()}\n')
    except IOError as error:
        print(error)

