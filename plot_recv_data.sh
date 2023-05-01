#!/bin/bash
source pyvenv/bin/activate
python live_plot.py data.csv 100 &
python recv_data.py
