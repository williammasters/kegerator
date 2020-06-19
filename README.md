# kegerator
Arduino and pi monitored kegerator

# Setup Steps

## Arduino
Arduino Wiring Diagram 

![Wiring Diagram] (https://github.com/williammasters/kegerator/tree/master/images/wiringdiagram.png)

Note: LCD optional, mainly used for debugging

Arduino Libraries Needed:
Dallas Temperature
One Wire

## Rasberry Pi 

Specs:
Raspberry pi 4 GB RAM
64GB microSD (can probably be fine with 32)

Pi setup:

Install Grafana and enable launch on startup

    wget https://dl.grafan.com/oss/release/grafana_6.6.1_armhf.deb
    sudo dpkg -i grafan_6.6.1_armf.deb
    sudo systemctl enable grafan-server
    sudo systemctl start grafana-server
    
Install Prometheus 
Note: Check for update release version, only the most current will be available

    wget https://github.com/promethus/prometheus/releases/download/v2.19.0/prometheus-2.19.0.linux-arm7.tar.gz
    tar xfz prometheus-2.19.0.linux-armv7.tar.gz
    mv prometheus-2.19.0.linux-armv7/ prometheus/
    
Create Prometheus Service File

    sudo nano /etc/systemd/system/prometheus.service   

    [Unit]
    Description=Prometheus Server
    Documentation=https://prometheus.io/docs/introduction/overview/
    After=network-online.target

    [Service]
    User=pi
    Restart=on-failure

    #Change this line if Prometheus is somewhere different
    ExecStart=/home/pi/prometheus/prometheus \
    --config.file=/home/pi/prometheus/prometheus.yml \
    --storage.tsdb.path=/home/pi/prometheus/data

    [Install]
    WantedBy=multi-user.target 
    
    
Enable starting prometheus on boot 
    
    sudo systemctl daemon-reload   
    sudo systemctl start prometheus 
    sudo systemctl enable prometheus 

Enable Python scripts to run on boot by adding them to /etc/rclocal be sure to include & after the file path or the process will hang
