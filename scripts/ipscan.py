#!/usr/bin/env python
# Script to scan IPs and record their status to file.
import subprocess
import argparse

# Output directory
OUTDIR = "/opt/local/var/lib/lcars"

# Static target lists
routers = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]
sensors = ["WXStation"]
sites = ["digifail.com", "google.com", "reddit.com", "github.com"]
printers = ["HPD4802B"]

# Process arguments
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Scan static list of IPs and save status to file.')
parser.add_argument("target")
args = parser.parse_args()

# Probably more Python-y way of doing this...
if args.target == "routers":
    targets = routers
    heading_string = "IP ADDRESS, STATUS\n"
elif args.target == "sensors":
    targets = sensors
    heading_string = "SENSOR, STATUS\n"
elif args.target == "sites":
    targets = sites
    heading_string = "WEBSITE, STATUS\n"
elif args.target == "printers":
    targets = printers
    heading_string = "PRINTER, STATUS\n"
else:
    print "Unknown target!"
    exit()

# Change filename depending on argument
log_file = OUTDIR + "/" + args.target

# Open log file for writing
print "Writing to log file %s..." % log_file
logfile = open(log_file, 'w')
logfile.write(heading_string)

# Scan and log
for target in targets:
    ret = subprocess.call("ping -c 1 %s" % target,
        shell=True,
        stdout=open('/dev/null', 'w'),
        stderr=subprocess.STDOUT)
    if ret == 0:
        status = "ONLINE"
    else:
        status = "OFFLINE"

    condition_string = target + ", " + status
    print(condition_string)
    logfile.write(condition_string)
    logfile.write("\n")

# Close file and print message
logfile.close()
print("Done")
