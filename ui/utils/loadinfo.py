# Read and process data from files/system
import subprocess
import forecastio
from datetime import datetime

# Return lines of text
def read_txt(filename):
    lines = []
    with open(filename, mode='r') as infile:
        lines = infile.read().splitlines()

    return lines;

# Return current uptime
def get_uptime():
    ps = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE)
    uptime = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return uptime.rstrip()[3:];

# Return system load
def get_load():
    ps = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE)
    uptime = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return uptime.rstrip()[-16:];

# Check version against GitHub
def update_available():
    ps = subprocess.Popen("git remote update >/dev/null 2>&1 && git status | grep behind | wc -l", shell=True, stdout=subprocess.PIPE)
    gitstatus = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    # Return value
    if gitstatus[0] == "0":
        return 0;
    elif gitstatus[0] == "1":
        return 1;

def get_weather():
    api_key = "ENTER_YOUR_APILKEY"
    lat = 26.000
    lng = -54.500

    current_time = datetime.now()

    forecast = forecastio.load_forecast(api_key, lat, lng, time=current_time, units="ca")
        
    return forecast.currently()
    
    #print current.summary
    #print current.temperature
    #print current.precipProbability
    #byHour = forecast.hourly()
    #print byHour.summary
    #print byHour.icon

    #for hourlyData in byHour.data:
    #    print hourlyData.temperature
        
    #currentWeather = forecast.currently()
    #print currentWeather