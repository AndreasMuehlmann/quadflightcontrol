#!/bin/bash
source pyvenv/bin/activate
python live_plot.py data.csv 50 &
python recv_data.py
