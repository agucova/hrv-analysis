import csv
import pandas as pd
import datetime
from os import listdir
from os.path import isfile, join
import glob
import re
import plotly.express as px

file = "samples/example.csv"
df = pd.read_csv(file, names=['time', 'amplitude'], header=None)
fig = px.line(df, x="time", y="amplitude", title='Heartbeats')
fig.show()
