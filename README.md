# CP4S Prometheus Exporter

IBM Cloud Pak for Security Prometheus Exporter.

This code relies on the Cloud Pak for Security Health Check Playbook running on the CP4S Cases app (to be published sometime later).

# Configuration

Before configuring the Exporter, you need to `git clone` the project to your target machine. Then you can modify the files in the cloned project folder.

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

# Building the image

Run the following command on the same folder as the Dockerfile resides

docker image build -t cp4s-pm-exporter:1.0.0 .

# Running the image

docker run -p 5000:5000 -d cp4s-pm-exporter:1.0.0

# Accessing the Exporter

Access the following url:

http://your_host_name:5000/metrics

The metrics you'll get is in the ./app/templates/metrics.txt file.