# Group 8 - 95-888 Data Focused Python - Carnegie Mellon University
This readme file contains information regarding installation of the SolarRenew sourcecode.

## Authors
Jonika Rathi - jrathi@andrew.cmu.edu

Shubhang Seth - shubhans@andrew.cmu.edu

## Dependency Installation
To run this application please first install the following dependencies(assuming pip as the package manager):

```
pip install pandas
pip install fpdf
pip install -U selenium
pip install -U matplotlib
pip install requests
pip install numpy
pip install lxml
```

For convenience, we have package a Virtual Environment with our source code. This has all the set of dependencies pre-installed.
To use this virtual environment, you must use the `venv/bin/python3.9` executable.

## Chromedriver Dependency
Our application uses Chromedrvier to perform replicate automation testing with selenium and scrape data.

You will also need to install Chromedriver for either Mac or Windows.
Both are included in this zip folder.  Please copy and paste the appropriate file to the main project 
directory prior to running the application.

For MAC, `cp chromedriver\ \(Mac\)/chromedriver .`

For Windows, `cp chromedriver\ \(Windows\)/chromedriver.exe .`

## Files included in this application:
```
consumeraffairs.py
dsire.py
google.py
line.py
main.py
NSRDB_Solar_Irradiance_API_Get_Version3.py
utility.py
chromedriver.exe (for Windows)
chromedriver (for Mac)
venv (packaged dependencies)
```

## How to run the code
Use command `./venv/bin/python3.9 main.py` to run with virtual enviroment
or else `python main.py` if you wish to use your own interpreter.

## Expected Output
Once the program is started, there might be multiple automated browser windows that open using 
Google Chrome. You must not kill them or the program will be interrupted. The windows are on an auto-close
pattern and will shut down once their job is done.

After scraping all websites, the code calculates some vital information and creates a pdf file by the name
`Analysis.pdf`. This should open up in your browser, but is also accessible from the root folder of the project.

## Seen Exceptions

### Chromedriver Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: './chromedriver'
or
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```
This implies that you might have forgotten to add the chromedriver to the project main root. You must copy the correct 
executable according to the OS and paste it in the root folder.

For MAC, `cp chromedriver\ \(Mac\)/chromedriver .`

For Windows, `cp chromedriver\ \(Windows\)/chromedriver.exe .`

### Chromedriver Incorrect Permissions
Chromedriver must be set to executable permissions for the code to run correctly. IF you see any error like this 
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable may have wrong permissions. 
```

Then you must set the correct permissions. This error is expected to occur only in macs. So use this command 
to fix it `chmod +x chromedriver`.

### Chromedriver Third Party Application Security Issue (Mac Specific)
If you get a prompt saying Chrome is `“chromedriver” cannot be opened because the developer cannot be verified`,
then you must specifically give it permissions from your security settings.
`System Preferences > Security & Privacy > There must be a button for "Allow Anyway" on the bottom`

### PermissionError: [Errno 13] Permission denied: 'Analysis.pdf' (Windows Specific)
If you get an error with opening 'Analysis.pdf', you must close all other applications that might be using 
'Analysis.pdf' and then re-run the application.