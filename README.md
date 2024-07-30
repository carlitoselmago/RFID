Code for RFID debugging and data collection

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

It is recommended that you don't connect or disconnect the antennas while the power is on, turn off the power of the reader before connecting or disconnecting antennas.

## Code available

### Software install

You need to install Python 3 and pip
run on terminal:
```
pip install python-osc
```

Keon data stream test (update ip of Keon device)

```
watch -n 1 "curl -s 192.168.4.139/devices/AdvanReader-m2-70-76af/jsonMinLocation | grep '<result>' | sed 's/.*<status>\(.*\)<\/result>.*/\1/'"

```

Python version , get the IP of the Keon reader accesing the router connected to the LAN IN port and put it with the argument --IP 
In this example, the tag data is printed on screen and sent thru OSC on local network on port 7500

```
python data_collection_VERSIO_keon.py --IP 192.168.4.139
```

### MAX patches to use along with other software such as ableton live:

https://github.com/carlitoselmago/Keonn

# impinj

impinj data stream test

```
curl -G -4 http://192.168.123.163/api/v1/data/stream/

```
