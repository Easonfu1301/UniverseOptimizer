import matplotlib
matplotlib.use('Agg')  # Must be set before any pyplot import to avoid tkinter thread errors

from .paths import *
from .cal_pareto_front import calculate_pareto_front, calculate_pareto_front_indices


