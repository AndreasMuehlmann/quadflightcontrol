import config as conf
from pid_controller import PidController
from adaptive_pid_controller import AdaptivePidController


def init_controller():
    if conf.controller == 'pid_controller':
        return PidController(conf.p_faktor, conf.i_faktor, conf.d_faktor,
                            conf.iir_faktor, conf.iir_order, conf.max_output_controller)
    if conf.controller == 'adaptive_pid_controller':
        return AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                    conf.max_output_controller)
    else:
        raise Exception(f'no controller with name {conf.env} defined.')
