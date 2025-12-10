# Digital Alarm Clock

A simple but stylish digital alarm clock built with Python and Tkinter.  
Features multiple color themes, 12 or 24 hour mode, snooze, and a flashing visual alarm.

> I created this alarm clock because... why not?

---

## Features

- Large digital clock display using the Digital-7 font  
- 12 hour and 24 hour display modes  
- Set alarm with hour and minute input  
- AM / PM selector in 12 hour mode  
- Snooze, dismiss, and cancel controls  
- Visual flashing effect when the alarm is active  
- Custom alarm sound (looped)  
- Multiple built in color themes:
  - Default  
  - Matrix  
  - Retro Blue  
  - Red Alert  
  - Neon Purple  
  - Synthwave  
  - Terminal Green  
  - Deep Ocean  
  - Amber Glow  
- Optional weather widget:
  - Enter a city name and get current temperature and conditions
  - Uses the free OpenWeather API if configured
---

## Screenshot Preview

<img width="400" height="304" alt="image" src="https://github.com/user-attachments/assets/b633c1c4-b58c-40ab-9d40-85181881a480" />

---

## Installation (conda for simplicity) 
1. Download or clone repo into designated folder 
2. Run this command in prompt

```
cd path\to\alarmclock #Adjust to the repo path
conda create -n alarmclock python=3.14
conda activate alarmclock
pip install requests
python alarm_clock.py
```
## Weather API setup (optional but recommended)
The clock can show live weather using the OpenWeather API.
If you do not set up an API key, the clock still works, but the weather panel will show a message like “No API key set (see config.py)”. 

### 1. Sign up for a free API key
1. Go to https://openweathermap.org/
2. Create a free account and log in.
3. Go to the API keys section of your account.
4. Copy your API key.
   - New keys can take 2 to 3 hours to fully activate on their servers.
     
### 2. Create your config.py
In the repo you will see a file named config_example.py:
```
"""
config_example.py

1. Rename this file to: config.py
2. Sign up for a weather API key at https://openweathermap.org/ (Free tier is fine)
3. Paste your API key into WEATHER_API_KEY below (inside the quotes)

Note: Weather API keys can take a couple of hours to activate.
"""

WEATHER_API_KEY = "PUT_YOUR_OPENWEATHER_KEY_HERE"
```
Once you rename the file and add your API key, you’ll have access to weather updates.
Just type in a city and click Get Weather.

## Troubleshooting

- **401 Invalid API key** → Your key may not be activated yet (can take 2–3 hours).
- **City not found** → Make sure you type a valid city name (e.g., "Toronto").
- **Network error** → Your internet connection or the API service may be temporarily unavailable.


---
> ## Font Credits

> Digital-7 font by Sizenko Alexander (Style-7), used under the Digital-7 freeware license for non-commercial use.  
http://www.styleseven.com

