import sys
import os


def append_dirs_to_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    append_child(current_dir, 'pid_controller')
    append_child(current_dir, 'adaptive_pid_controller')
    append_child(current_dir, 'envs')
    append_child(current_dir, 'interfaces')


def append_child(directory, child):
    child = os.path.join(directory, child)
    sys.path.append(child)
