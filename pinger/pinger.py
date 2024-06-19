import subprocess
import re
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "pinger"
token="j_uucRAE7Gnmw1uUnwrCatOpwDsokSRQi6fYxy0OYPLXfm99NW0VH2JmHMGCdcb8NXfO5RexrqQSNjhQs2v1qw=="
host="influxdb"
port=8086
client = InfluxDBClient(url=f"http://{host}:{port}", token=token, org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

interval_s = 30

def ping(host):
    """return ms time for pinging host or None if error"""
    timeout_s = 5
    command = ['ping', '-c', '1', '-W', str(timeout_s), host]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
        return None

    # Extract duration from the output
    duration_regex = re.compile(r'time=(\d+.\d+) ms')
    durations = duration_regex.findall(stdout.decode())

    if durations:
        return float(durations[0])
    else:
        return None
        

hosts = ["192.168.1.1", "google.com"]

def perform_measurement():
    points = []
    for host in hosts:
        try:
            ping_time = ping(host)
            p = Point("ping").tag("host", host).field("duration_ms", ping_time).field("error", 0 if ping_time is not None else 1)
            points.append(p)
        except Exception as e:
            print(f"Error pinging host {host}: {e}")

    for p in points:
        write_api.write(bucket=bucket, record=p)

def main():
    print("Starting pinger")
    while True:
        try:
            perform_measurement()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(interval_s)

if __name__ == "__main__":
    main()
