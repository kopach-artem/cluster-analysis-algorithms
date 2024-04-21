import os
import random

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

target_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', 'data_bank', 'results'))

def find_next_file_number(algorithm_name):
    files = os.listdir(target_directory)
    count = 1
    for file in files:
        if file.startswith(algorithm_name) and file.endswith('.png'):
            count += 1
    return count