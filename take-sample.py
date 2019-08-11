import serial
from timeit import default_timer as timer
from tqdm import tqdm, trange
import pandas as pd
import plotly.express as px

port = "/dev/ttyACM0"
rate = 115200
samples = 16000
file = "samples/sample.csv"

ser = serial.Serial(port, rate)


def getmeasure():
    try:
        amplitude = int(ser.readline().decode(
            "ascii").strip("\r\n").strip("S"))
    except:
        amplitude = None
    return timer(), amplitude

print('\x1b[2J')

time = timer()
print("\nGetting", str(samples), "samples from", port + ".")
data = [getmeasure() for i in trange(samples)]
time = timer() - time
broken = [value for value in data if value[1] == None]
print("Taken", len(data)-len(broken), "samples in",
      str(round(time, ndigits=2)) + "s.\n")
print("\nInterpolating", len(broken), "broken bytes.\n")

df = pd.DataFrame(data, columns=["time", "amplitude"])
df = df.interpolate(method='spline', order=3)

# Deprecated, remove broken values
# data = [value for value in tqdm(data) if value[1] != -1]

fig = px.line(df, x="time", y="amplitude", title='Heartbeats')
fig.show()

df.to_csv(file, index=False)
