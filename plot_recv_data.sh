#!/bin/bash
source pyvenv/bin/activate
python live_plot.py measurements.csv 100 &
python live_plot.py outputs.csv 100 &
python recv_data.py
