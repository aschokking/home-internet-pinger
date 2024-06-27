This is a little toy project to try and log how my home internet is doing over time. 

On a configurable interval, the script will ping a configurable list of hosts and log the results to a influxdb database. You can then view the results in grafana.

![image](https://github.com/aschokking/home-internet-pinger/assets/399279/d553b50d-b4b7-4250-9c8c-0e6ef3d61308)

There's lost to do still in terms of:
- [ ] credentials not stored in code
- [ ] grafana data source config stored in code
- [ ] grafana dashboard definition stored in code (or at least backed up so it can be initialized)
