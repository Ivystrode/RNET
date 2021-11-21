from bs4 import BeautifulSoup
import pandas as pd
import requests, sqlalchemy, time

import data_dbcontrol as dbcon


class DataSorter():
    
    def __init__(self, file_to_read, db_table):
        self.file_to_read = file_to_read
        self.db_table = db_table
        self.devices = []
        dbcon.connect()
        
        #need this??
        # self.engine = sqlalchemy.create_engine('sqlite:///data_db.db')
        
    def mac_lookup(self, macaddr):
        # headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        # r = requests.get(f'https://maclookup.app/search/result?mac={macaddr}', headers = headers)
        # c = r.content
        # soup = BeautifulSoup(c, "html.parser")
        # try:
        #     org = soup.select_one("h2").get_text()
        # except:
        #     org="Unknown"
        # return org
        print("simulating makers (maclookup requests exceeded")
        return "simulated"
        
    def mac_gather(self, data):
        macs = [mac for mac in data['BSSID'] if mac != "Station MAC"]
        mac_prefixes = [mac[:8].replace(":", "") for mac in macs] 
        mac_suffixes = [mac[9:].replace(":", "") for mac in macs]
        
        return mac_prefixes
    
    def serialize(self, detail):
        detail = str(detail)
        return detail
    
    def deserialize(self, table, device, detail):
        res = dbcon.check_device(device)
        for row in res[0]:
            original_db_string = row[detail]
            original_db_string = original_db_string.replace("[", "")
            original_db_string = original_db_string.replace("]", "")
            original_db_string = original_db_string.replace("'", "")
            original_db_string = original_db_string.split(",")
            return original_db_string
        

    def store_new_report(self):
        data = pd.read_csv(self.file_to_read, sep=r'\s*,\s*', encoding='ascii', engine='python')
        mac_prefixes = self.mac_gather(data)
        manufacturers = [self.mac_lookup(prefix) for prefix in mac_prefixes]
        
        # delete second header row
        data.drop(data.index[data['BSSID'] == "Station MAC"], inplace=True)
        
        # put first seen and last seen into a list of 'sightings' of that device
        sightings_dict = {}
        for device, fts, lts in zip(data['BSSID'], data['First time seen'], data['Last time seen']):
            sightings = []
            sightings.append(fts)
            sightings.append(lts)
            sightings_dict[device] = sightings
            
        # we can do this with power as well so we can see whether device is moving closer/further from detector
        power_dict = {}
        for device, power_reading in zip(data['BSSID'], data['Power']):
            power_readings = []
            power_readings.append(power_reading)
            power_dict[device] = power_readings

        # sort out devices that appeared below second heaader row (non-dynamically...)
        for index, row in data.iterrows():
            if int(row.channel) < 0:
                data.at[index, 'Power'] = row.channel
                data.at[index, 'channel'] = 99

            
        data = data.assign(sightings=[str(value) for value in sightings_dict.values()])
        data = data.assign(power_readings=[str(value) for value in power_dict.values()])
        data = data.assign(maker=[m for m in manufacturers])
        data = data[['BSSID','channel','power_readings','ESSID', 'maker', 'sightings']]
        
        for row in data.iterrows():
            time.sleep(1)
            try:
                dbcon.insert(row[1][0], row[1][1], self.serialize(row[1][2]), row[1][3], row[1][4], self.serialize(row[1][5]))
            except:
                power_readings_list = self.deserialize(self.db_table, row[1][0], 2)
                sightings_list = self.deserialize(self.db_table, row[1][0], 5)
                
                power_readings_list.append(str(row[1][2]))
                sightings_list.append(str(row[1][5]))
                
                power_readings_list = self.serialize(power_readings_list)
                sightings_list = self.serialize(sightings_list)
                
                dbcon.update_device(row[1][0], row[1][1], power_readings_list, row[1][3], row[1][4], sightings_list)
                
        
        
        
        
        
        
        
if __name__ == '__main__':
    # just for testing
    d = DataSorter("../media/20210601-1752_prototype1_wifi_scan-01.csv", "test")
    d.store_new_report()