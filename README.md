# Network Capture

This script allows the user to capture network packets through a specified
port over a duration of time. The source and destination IP addresses are
extracted and converted to a geo location (longitude/latitude) and returned as a
kml file which can be dsipalyed in GIS software.

This project is based on the article, https://medium.com/vinsloev-academy/python-cybersecurity-network-tracking-using-wireshark-and-google-maps-2adf3e497a93.

## Requirements

This project requires that Tshark, https://tshark.dev/, be installed. It also requires that the GeoLiteCity database be available in the root folder, https://github.com/mbcc2006/GeoLiteCity-data.

This project requires the us of poetry dependency management, https://python-poetry.org/. To initialise the environment use 

'''bash
poetry init
'''

and then run the script using

'''bash
poetry run ip_geo_conversion.py
'''

There are variables in the script that need to be updated before runing. These are, home IP address, user, port name.

## License
MIT (https://choosealicense.com/licenses/mit/)
