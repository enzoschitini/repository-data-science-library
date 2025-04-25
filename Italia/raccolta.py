import pandas as pd
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from memoria import guida as gd

class Differenza(object):
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe

class IntervalloCV(object):
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe