Code for RFID debugging and data collection

There's an example of both curl and python for both Keon and Impinj devices 

The Keon data_collection_VERSIO_keon.py file will only show on screen the amount of tags detected.
Complete the code with the data collected to use with other data protocols, audio etc.

# Keon

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
