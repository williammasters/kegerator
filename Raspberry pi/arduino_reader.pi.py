import serial
import time

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import start_http_server


# Arduino setup
# Ocasionally this value is ACM1
port = "/dev/ttyACM0"
# serial port should be the same in arduino code
s1 = serial.Serial(port, 9600)

# Prometheus Setup
start_http_server(8000)
# v1_counter = Counter('V1', 'Volume in Liters from F1 sensor')
v1_gauge = Gauge('V1', 'Flowrate in Liters per min from F1 sensor')
t1_gauge = Gauge('T1', 'Current Temperature in F from T1 sensor')

s1.flushInput()


def V1(value):
    v1_gauge.set(float(value))
    return


def T1(value):
    t1_gauge.set(float(value))
    return


def update_prometheus_metrics(metric, value):
    switcher = {
    'V1': V1,
    'T1': T1
    }
    func = switcher.get(metric, lambda: "Unsupported Metric")
    if func != "Unsupported Metric":
        func(value)
    return


while True:
    if s1.inWaiting()>0:
        inputValue = s1.read(7)
        # get timestamp, device, and reading value
        metrics = [time.time()]+inputValue.decode('utf-8').split('_')
        print(metrics)
        update_prometheus_metrics(metrics[1], metrics[2])
