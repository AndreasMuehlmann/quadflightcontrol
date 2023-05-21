#!/bin/bash
source pyvenv/bin/activate
python live_plot.py measurements.csv 500 &
python live_plot.py outputs.csv 500 &
python recv_data.py
