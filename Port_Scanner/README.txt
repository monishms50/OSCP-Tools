Step 1:
Use pingsweep on a given network to get IP addresses of all connected devices on the network.


Step 2:
Use python3 port_scanner.py <target_host> <Port_min_range> <Port_max_range> to run the tool and the best way to 
use it is to redirect the output to a text file so that it gets easier to work with the scan report further.

   # python3 port_scanner.py  192.168.1.1 20 1024  >> Results.txt
