from flask import Flask
import xmltodict as xm
import json
import logging

#new line
app = Flask(__name__)
iss_epoch_data = {}
iss_sighting_data = {}
@app.route('/load_data', methods=['POST'])
def load_from_file():
    """
    Reads two XML data files and states that both files have been read
    """
    logging.info("Reading Data.")
    global iss_epoch_data
    global iss_sighting_data
    with open('ISS.OEM_J2K_EPH.xml' , 'r') as f:
        iss_epoch_data =  xm.parse(f.read())
    with open('XMLsightingData_citiesUSA04.xml' , 'r') as f:
        iss_sighting_data = xm.parse(f.read())
    return f'Data was read\n'

@app.route('/epoch', methods=['GET'])
def find_epochs():
    """
    Runs through epoch dictionaries and returns epochs for position data

    Returns:
    epochs found in position data
    """
    logging.info("Code to find epochs...")
    epoch = " "
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        epoch = epoch + iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return epoch

@app.route('/<epoch>', methods=['GET'])
def find_epoch_data(epoch: str):
    """
    Runs through vectors for each state in epoch dictionary. Once the epoch value is found, position and velocity values are found.

    Args:
    epoch (str): A string with the epoch value
    Returns:
    e_dict (dictionary): Position and velocity data for each epoch.
    """
    logging.info("Code to find epoch information/"+epoch)
    e_num=0
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if epoch == iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            e_num = i
            break
    pv = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
    e_dict = {}
    for num in pv:
        e_dict[num] = iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][e_num][num]
    return e_dict
@app.route('/count',methods=['GET'])
def get_countries():
    """
    Iterates through ISS data and finds "country" key.
    Returns:
    count_dict (dictionary): All countries featured in the dataset
    """
    logging.info("Code to find all countries")
    count_dict = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count_name in count_dict:
            count_dict[count_name] += 1
        else:
            count_dict[count_name]=1
    return count_dict
@app.route('/count/<count>',methods=['GET'])
def country_data(count):
    """
    Iterates through ISS sighting data and returns values for each specific country noted by the 'country' key

    Args:
    count(str): String that denotes each specific country from which to pull data
    Returns:
    count_list_of_dicts(list): list of information on each country
    """
    logging.info("code to obtain data on /"+count)
    count_list_of_dicts = []
    count_data = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count == count_name:
            new_dict_c = {}
            for j in count_data:
                new_dict_c[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
            count_list_of_dicts.append(new_dict_c)
    return json.dumps(count_list_of_dicts, indent=2)
@app.route('/count/<count>/region',methods=['GET'])
def get_regions(count):
    """
    Iterates through ISS sighting data for specific countries and returns values for the 'region' key.A key is created for each region and housed in a new dictionary

    Args:
    count (str): String that denotes each specific country from which to pull data

    Returns:
    region_dict (dictionary): dictionary with regions for each country
    """
    logging.info("code to find all regions in /"+count)
    region_dict = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count == count_name:
            region_name = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if region_name in region_dict:
                region_dict[region_name] += 1
            else:
                region_dict[region_name] = 1
    return region_dict
@app.route('/count/<count>/region/<region>', methods=['GET'])
def region_data(count, region):
    """
    Iterates through ISS sighting data for specific regions within each country. Gets information from each region in the region_dict.

    Args:
    count (str): String that denotes each specific country from which to pull data
    region (str): String that denotes each specific region from which to pull data

    Returns: 
    region_list_of_dicts (list): contains all the information about a specific region
    """
    logging.info("Code to find all info on /"+region)
    region_list_of_dicts = []
    region_data = ['city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count == count_name:
            region_name = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == region_name:
                new_dict_r = {}
                for j in region_data:
                    new_dict_r[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
                region_list_of_dicts.append(new_dict_r)
    return json.dumps(region_list_of_dicts, indent=2)

@app.route('/count/<count>/region/<region>/city',methods=['GET'])
def get_cities(count, region):
    """
    Iterates through ISS sighting data within specific regions and countries and returns values for the 'city' key. Key for each city is stored in a dictionary

    Args:
    count(str):String that denotes each specific country from which to pull data
    region (str): String that denotes each specific region from which to pull data

    Returns:
    city_dict(dictionary): Dictionary that contains all cities.
    """
    logging.info("code to find cities in /"+region)
    city_dict={}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count == count_name:
            region_name = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == region_name:
                city_name = iss_sighting_data['visible_passes']['visible_pass'][i]['city']
                if city_name in city_dict:
                    city_dict[city_name] +=1
                else:
                    city_dict[city_name]=1
    return city_dict
@app.route('/count/<count>/region/<region>/city/<city>',methods=['GET'])
def get_city_data(count, region, city):
    """
    Iterates through ISS sighting data for each specific city. Gets data for each specific city and creates a list.

    Args:
    count(str):String that denotes each specific country from which to pull data
    region (str): String that denotes each specific region from which to pull data
    city (str): String that denotes each specific city from which to pull data

    Returns:
    city_list_of_dicts (list): Contains information based on a specific city.
    """
    logging.info("Code to find info on /"+city)
    city_list_of_dicts = []
    city_data = ['spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        count_name = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if count == count_name:
            region_name = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == region_name:
                city_name = iss_sighting_data['visible_passes']['visible_pass'][i]['city']
                if city == city_name:
                    new_dict_ci = {}
                    for j in city_data:
                        new_dict_ci[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
                    city_list_of_dicts.append(new_dict_ci)
    return json.dumps(city_list_of_dicts, indent=2)

@app.route('/help', methods=['GET'])
def help():
    """
    Gives output and results for each app route
    """
    logging.info("The information on each route and what they do.")
    describe = "ISS Sighting Location\n"
    describe += "/ (GET) Information is outputted\n"
    describe += "/load_data ((POST) Resets and loads data from a file)\n"
    describe += "Routes to find position and velocity data:\n\n"
    describe += "/epoch ((GET) lists epochs for postion and velocity data)\n"
    describe += "/epoch/<epoch> ((GET) lists data for each specific epoch)\n"
    describe += "Routes to find ISS sighting data\n\n"
    describe += "/count ((GET) lists each country found in the sighting data)\n"
    describe += "/count/<count> ((GET) lists data for each specific country)\n"
    describe += "/count/<count>/region ((GET) lists each region found in a specific country)\n"
    describe += "/count/<count>/region/<region> ((GET) lists data for each specific region)\n"
    describe += "/count/<count>/region/<region>/city ((GET) lists each city in a specific region)\n"
    describe += "/count/<count>/region/<region>/city/<city> ((GET) lists data for each specific city) \n"
    return describe

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')






















