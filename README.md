# CP4S Prometheus Exporter

IBM Cloud Pak for Security Prometheus Exporter.

This code relies on the Cloud Pak for Security Health Check Playbook running on the CP4S Cases app (to be published sometime later).

# Configuration

Before configuring the Exporter, you need to `git clone` the project to your target machine. Then you can modify the files in the cloned folder.

- ./store/config.yml
  - Configure the CP4S to be monitored
    - url, keys
    - polling interval
    - cleanup target
  - CP4S Cases app must have a specific playbook installed and configured (will be published on GitHub sometime later)
- ./crontab.txt
  - You can change the Health Check Case creation interval (polling interval above is just to retrieve the latest data from the past closed Case and returns the same value until the new Case is created and the metrics are updated)
- ./Dockerfile
  - No need to change basically
- ./docker-compose.yml
  - No need to change basically


# Running the exporter

Run the following command on the same folder as the docker-compose.yml resides

docker compose up -d

# Running the image

docker run -p 5000:5000 -d cp4s-pm-exporter:1.0.0

# Accessing the Exporter

Access the following url:

http://your_host_name:5000/metrics

The metrics you'll get is based on the ./app/templates/metrics.txt file and the sample output is the following:

```
# HELP up Value is 1 if summary is 'successful', 0 otherwise.
# TYPE up gauge
up{index="1",name="qradar_offense"} 1
up{index="2",name="de"} 1
up{index="3",name="tii"} 1
up{index="4",name="ldap"} 1
# HELP last_udpate_epoc_ms Last update time in msec since epoch (1970).
# TYPE last_udpate_epoc_ms gauge
last_udpate_epoc_ms{index="1",name="qradar_offense"} 1682035218176.9695
last_udpate_epoc_ms{index="2",name="de"} 1682035226402.2593
last_udpate_epoc_ms{index="3",name="tii"} 1682035220305.668
last_udpate_epoc_ms{index="4",name="ldap"} 1682035212282.2903
# HELP execution_time_ms Check execution time spent in msec.
# TYPE execution_time_ms gauge
execution_time_ms{index="1",name="qradar_offense"} 11874.163389205933
execution_time_ms{index="2",name="de"} 19680.180549621582
execution_time_ms{index="3",name="tii"} 12672.38712310791
execution_time_ms{index="4",name="ldap"} 5136.6565227508545
```

