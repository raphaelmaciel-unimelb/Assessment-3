<!-- 
#Bug ID : 001
#Description: SyntaxError: cannot assign to attribute here. Maybe you meant '==' instead of '='?
#Line number: File "/home/weather.py", line 30
#How it was foud: error when trying to run the python weather.py for the first time
#How it was fixed: replacing '=' by '==' 

#Bug ID : 002
#Description: API error: 400 "Latitude must be in range of -90 to 90°. Given: 151.21." due to inverted parameters
#Line number: File "/home/weather.py", line 28, 29
#How it was foud: using the function print(response.text) after the requests.get() and 
                    comparing with the parameters use in the line 62 result = get_weather(-33.87, 151.21)  # Sydney  
#How it was fixed: first I have fixed the order of the parameters
                    second, created a protection using a if clause before the requests.get() 
                    to make sure the range for Latitude and Longitude parameters are in the correct range, 
                    if not in the range, print an error message and return None
                    






-->


