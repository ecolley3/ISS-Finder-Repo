# Needle in a Haystack
## ISS Data Finder: By Ethan Colley

### Description
This project takes data from the International Space Station and creates a containerized Flask application that takes the inputed data and returns a more organized version of the data given bythe file. The application can take the country, region, and city, then output relevant information like the times that the ISS can be seen as as position and velocity values of the ISS. All information is displayed in a way that makes it easy for the user to understand.

### ISS Data Download
1) Paste the link `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq` into your web browser and login to isp in your shell.
2) Under the public distribution file, right click the XML option and copy the link address.
3) Use the wget command and paste the link address afterward: `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml`
4) Now go back to the ISS website and find and copy the XML link for `XMLsightingData_citiesUSA04`.
5) Use wget with the link again to download the sighting data: `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA04.xml`

### Building the Docker File
1) First, pull the files from Docker by using `docker pull ecolley3/iss-finder:Midterm`
2) Now, utilizing the Makefile, use `make build` to build your Dockerfile. The output should look like:
```bash
Sending build context to Docker daemon  740.9kB
Step 1/8 : FROM python:3.9
 ---> 745b54045d61
Step 2/8 : RUN mkdir /app
 ---> Using cache
 ---> ae082c8f115a
Step 3/8 : WORKDIR /app
 ---> Using cache
 ---> c90a4ff43ea7
Step 4/8 : COPY fsk.txt /app/fsk.txt
 ---> Using cache
 ---> 8639d8a7a0d4
Step 5/8 : RUN pip3 install -r /app/fsk.txt
 ---> Using cache
 ---> 7814b062cf57
Step 6/8 : COPY . /app
 ---> b69240443771
Step 7/8 : ENTRYPOINT ["python"]
 ---> Running in 25f182836784
Removing intermediate container 25f182836784
 ---> 7e04874d0a15
Step 8/8 : CMD ["app.py"]
 ---> Running in b82db29aa417
Removing intermediate container b82db29aa417
 ---> bb38de88c018
Successfully built bb38de88c018
Successfully tagged ecolley3/iss-finder:Midterm
```
### Running the Application Using Curl
1) Open two shell terminals for ease of use in this process
2) In the first window, run these three commands:
```bah
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5009
```
3) In the second window, run this command `curl localhost:5009/load_data -X POST` to read the data from the files.
4) You can then run the `curl localhost:5009/help` command to see each app route and what they will output.
5) Use a route to find the specific data you are looking for. 
Example: `curl localhost:5009/count/United_States/region/Illinois/city`
Output:

```bash
"McHenry": 13,
  "McLeansboro": 11,
  "Metropolis": 9,
  "Milledgeville": 14,
  "Minooka": 13,
  "Moline": 14,
  "Monmouth": 13,
  "Monticello": 13,
  "Morris": 13,
  "Morrison": 14,
  "Mound_City": 9,
  "Mount_Carmel": 12,
  "Mount_Carroll": 14,
  "Mount_Sterling": 12,
  "Mount_Vernon": 10,
  "Murphysboro": 9,
  "Naperville": 13,
  "Nashville": 10,
  "Newton": 11,
  "Oak_Forest": 12,
  "Olney": 12,
  "Oquawka": 13,
  "Oregon": 14,
  "Ottawa": 13,
  "Ozark": 9,
  "Palatine": 13,...
  ```
The data lists all cities found in Illinois inside the United States.

### Works Cited
1) Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. ISS.OEM_J2K_EPH. NASA. Retrieved March 20, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

2) Goodwin, S. (n.d.). XMLsightingData_citiesUSA04. NASA. Retrieved March 20, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA04.xml
