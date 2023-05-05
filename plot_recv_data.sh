#!/bin/bash
source pyvenv/bin/activate
python live_plot.py measurements.csv 200 &
python live_plot.py outputs.csv 200 &
python recv_data.py
