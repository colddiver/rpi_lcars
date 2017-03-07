#!/usr/bin/env python
# Supervisor script, makes sure all sub-scripts are running on schedule
# and monitors main LCARS interface
import time
import subprocess

# Command to start LCARS
LCARS_EXE = "./lcars.py"

def checkLCARS():
    ps = subprocess.Popen("ps -ef | grep lcars.py | wc -l", shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    # Nasty hack here, if multiple results are returned one of them should be
    # what we're actually looking for.
    if output[0] >= "3":
        return 1
    else:
        return 0

def startupAlert():
    print "Init alert."
    alertfile = open("/opt/local/var/lib/lcars/alert", 'w')
    alertfile.write("SYSTEM ALERT\n")
    alertfile.write("System startup in process.\n")
    alertfile.write("Sensor and network data may be\n")
    alertfile.write("incomplete.\n")

def createAlert():
    print "Writing alert."
    alertfile = open("/opt/local/var/lib/lcars/alert", 'w')
    alertfile.write("RANDOM THOUGHT\n")
    alertfile.write("The first time any man's freedom\n")
    alertfile.write("is trodden on, we're all damaged.\n")
    alertfile.write("                         -Jean-Luc Picard\n")

# Time-based functions

# Will be called for first few seconds
def startup():
    startupAlert()

# Called every 30 seconds
def thirty():
    print("30 Seconds")
    subprocess.Popen(["./scripts/ipscan.py", "routers"])
    subprocess.Popen(["./scripts/ipscan.py", "sensors"])
    subprocess.Popen(["./scripts/ipscan.py", "printers"])

def sixty():
    print("1 Minute")
    subprocess.Popen(["./scripts/ipscan.py", "sites"])

# Main loop
print("Starting...")
tick = 0
while True:
    print "Heartbeat"

    # Tasks for initial startup
    if tick < 5:
        startup()
    else:
        createAlert()

    # Every 30 seconds
    if (tick % 15) == False:
        thirty()

    # Every 60 seconds
    if (tick % 30) == False:
        sixty()

    # See if LCARS needs to be launched
    if checkLCARS() == True:
        print("LCARS Online")
    else:
        print("Launching LCARS")
        subprocess.Popen([LCARS_EXE])

    # Tick, wait for 2 seconds
    tick += 1
    time.sleep(2)
