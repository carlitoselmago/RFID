Code for RFID debugging and data collection

There's an example of both curl and python for both Keon and Impinj devices 

The Keon data_collection_VERSIO_keon.py file will only show on screen the amount of tags detected.
Complete the code with the data collected to use with other data protocols, audio etc.

# Keon

## How to setup the reader:

- First connect the antenna to the RF 1 port.
- Connect the LAN IN ethernet port to the PoE power unit OUT port. Then connect the IN port to a computer o a switch/router so You can acces the reader thru an IP.
- Get the IP of the reader thru the router admin page. Usually thru http://192.168.1.1
- Access the reader's config web page just using the IP obtained, usually something such as http://192.168.1.139/
- Go to the Monitor page and click on the big red "STOPPED" button to start the reading.
- You can configure other settings in the RFID section. The most important is the "Power (dBm)" which will control the range of the tags being read.
- You can also connect other antennas to the RF2 port and configure it in the same page. Other antennas will make the reading process twice as slow.

### Important note

It is recommended that you don't connect or disconnect other antennas while the power in on, connect the antennas before connecting to power.

Keon python data stream test, it can be adapted to connect to other protocols 

Keon data stream test (update ip of Keon device)

´´´

watch -n 1 "curl -s 192.168.4.139/devices/AdvanReader-m2-70-76af/jsonMinLocation | grep '<result>' | sed 's/.*<status>\(.*\)<\/result>.*/\1/'"

´´´

Python version , get the IP of the Keon reader accesing the router connected to the LAN IN port and put it with the argument --IP 

```
python data_collection_VERSIO_keon.py --IP 192.168.4.139
```

# impinj

impinj data stream test

´´´

curl -G -4 http://192.168.123.163/api/v1/data/stream/

´´´
