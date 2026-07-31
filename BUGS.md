# COMP90100: Assessment 3 - Weather app

- Student: Raphael Barbosa Maciel
- Subject: COMP90100 - AI Programming Fundamentals (COMP90100_2026_OT4_UMO_1)
- Repository URL: https://github.com/raphaelmaciel-unimelb/Assessment-3

## List of issues and fixes

+ [X] BUG 001
    - Name: SyntaxError '==' instead of '='
    - Description: SyntaxError: cannot assign to attribute here. Maybe you meant '==' instead of '='?
    - Issue Line number: 30
    - How it was found: runtime error when trying to run the python weather.py for the first time
    - How it was fixed: replacing '=' by '=='
        - Commit Hash: a588a88bf6a747110c8bbd0dd18936c9f4810c27
        - Commit message: "Fixing bug 001"

---
+ [X] BUG 002
    - Name: inverted parameters Latitude and Longitude
    - Description: API error: 400 due to inverted parameters Latitude and Longitude
    - Issue Line number: 23, 24
    - How it was found: started by investigating the runtime error API error 400, using the print(response.text) function just after the requests.get() call and checking the response content. The error message in the response was "Latitude must be in range of -90 to 90°. Given: 151.21.". With that I went back to the check the paramerters and found the parameters inverted in the dict value assignement for the respective keys.
    - How it was fixed: manually changed the parameter order
        - Commit Hash: b8b40f1762b96a612c9d8fe5d1ab9f169a3ebae9
        - Commit message: "Fixing bug 002"

---
+ [X] BUG 003
    - Name: Return args
    - Description: the function is not returning the full current-weather dict (temperature, windspeed, winddirection, time, ...) exactly as the API returns it
    - Issue Line number: 33
    - How it was found: by analysing the implemented code vs the requirements described in the Docstring 
    - How it was fixed: manually changing the return arg by removing the ["temperature"]
        - Commit Hash: 183f917f020b3124119a62be051d9d3e0b46b599
        - Commit message: "Fixing bug 003"


---
+ [X] BUG 004
    - Name: Temperature unit
    - Description: the temperature unit should be in Celsius instead of fahrenheit
    - Issue Line number: 26
    - How it was found: by analysing the implemented code vs the requirements described in the Docstring
    - How it was fixed: manually updated the temperatue_unit to "Celsius"
        - Commit Hash: 
        - Commit message: "Fixing bug 004"

---
+ [ ] BUG 005
    - Name:
    - Description:
    - Issue Line number:
    - How it was found:
    - How it was fixed: 
        - Commit Hash:
        - Commit message: