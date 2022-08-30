import sys
import os

def append_dirs_to_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    _append_child(current_dir, 'pid_controller')
    _append_child(current_dir, 'adaptive_pid_controller')
    _append_child(current_dir, 'envs')
    _append_child(current_dir, 'interfaces')


def _append_child(directory, child):
    child = os.path.join(directory, child)
    sys.path.append(child)
