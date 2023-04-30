import sys
import os


def append_dirs_to_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    _append_child(current_dir, 'controllers')
    _append_child(current_dir, 'controllers/adaptive_pid_controller')
    _append_child(current_dir, 'envs')
    _append_child(current_dir, 'interfaces')
    _append_child(current_dir, 'filters')


def _append_child(directory, child):
    child = os.path.join(directory, child)
    sys.path.append(child)
