from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import subprocess
import time

app = Flask(__name__)

gpu_util = Gauge("gpu_utilization_percent", "GPU Utilization")
gpu_temp = Gauge("gpu_temperature_celsius", "GPU Temperature")
gpu_mem_used = Gauge("gpu_memory_used_mb", "GPU Memory Used")
gpu_mem_total = Gauge("gpu_memory_total_mb", "GPU Memory Total")
gpu_power = Gauge("gpu_power_draw_watts", "GPU Power Draw")


def update_metrics():
    cmd = [
        "nvidia-smi",
        "--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total,power.draw",
        "--format=csv,noheader,nounits"
    ]

    output = subprocess.check_output(cmd).decode().strip()

    util, temp, mem_used, mem_total, power = output.split(",")

    gpu_util.set(float(util))
    gpu_temp.set(float(temp))
    gpu_mem_used.set(float(mem_used))
    gpu_mem_total.set(float(mem_total))
    gpu_power.set(float(power))


@app.route("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(), mimetype="text/plain")


@app.route("/")
def home():
    return "GPU Exporter Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9835)