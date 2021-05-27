# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
import datetime

# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role, rac, wac):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1
        
        user_data = {'username': username, 'email': email, 'role': role, 'rac': rac, 'wac': wac}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id, user_rac):
        key = {'device_id': device_id}
        if(key['device_id'] in user_rac or user_rac == 'admin'):
            return self.__find(key)
        else:
            return -1
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer, user_wac):
        self._latest_error = ''
        if(device_id in user_wac or user_wac == 'admin'):
            device_document = self.find_by_device_id(device_id, device_id)
            if (device_document):
                self._latest_error = f'Device id {device_id} already exists'
                return -1
        
            device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
            device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
            return self.find_by_object_id(device_obj_id)
        else:
            self._latest_error = f'Device id {device_id} cant be modified by this user'
            return -1

# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp, user_rac):
        key = {'device_id': device_id, 'timestamp': timestamp}
        if(key['device_id'] in user_rac or user_rac == 'admin'):
            return self.__find(key)
        else:
            return -1;
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp, user_wac):
        self._latest_error = ''
        if(device_id in user_wac or user_wac == 'admin'):
            wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp, device_id)
            if (wdata_document):
                self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
                return -1
        
            weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
            wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
            return self.find_by_object_id(wdata_obj_id)

        else:
            self._latest_error = f'Device id {device_id} for Weather cant be modified by this user'
            return -1
        
        
        
        
class DailyReportModel:
    
    DAILY_REPORT_MODEL = 'daily_report_model'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Private function (starting with __) to be used as the base for all find functions from weather data model
    # get_all_data() method created to pull more than one record
    def __find(self, key):
        wdata_document = self._db.get_all_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # Private function (starting with __) to be used as the base for all find functions from daily report model
    # get_all_data() method created to pull more than one record
    def __findindaily(self, key):
        dailydata_document = self._db.get_all_data(DailyReportModel.DAILY_REPORT_MODEL, key)
        return dailydata_document
    
    # Method to find the average, minimum and maximum from the data passed
    def daily_report_avg_min_max(self, wdata_document):
        if(wdata_document):
            minimum = 9999
            maximum = 0
            total = 0
            average = 0
            for num in wdata_document:
                if(num['value']<minimum):
                    minimum=num['value']
                elif(num['value']>maximum):
                    maximum=num['value']
                total+=num['value']    
                average = total / len(wdata_document)  
  
            result = { 'average':average, 'minimum':minimum, 'maximum':maximum, 'count':len(wdata_document)}
            return result
        else:
            return -1;
    
          
        
    # Method to insert daily report data from weather_data collection database to daily_report_model database  
    # This method is used from setup.py for inserting all the data from to model database while populating in bulk
    # This method is also used from main.py for manually inserting one record at a time as well for future use
    def insert_daily_report_to_daily_report_model(self, device_id, timestamp, user_rac):
        if(device_id in user_rac or user_rac == 'admin'):
            self._latest_error = ''
            key = {'device_id': device_id, 'timestamp': { "$gte": timestamp, "$lt": timestamp+ datetime.timedelta(days=+1)}}
            data_doc = self.__find(key)
            if(data_doc):
                avg_min_max_result = self.daily_report_avg_min_max(data_doc)
                calculated_result = {'device_id': device_id, 'timestamp': timestamp}
                calculated_result.update(avg_min_max_result)
            
                wdata_document = self.find_by_device_id_and_timestamp_indaily(device_id, timestamp)
                if (wdata_document):
                    self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
                    return -1
                else:
                    self.insert(calculated_result)
                return calculated_result
            else:
                return -1
        else:
            return -1    
        
        
    # This method checks if the user has read access, then creates the key and pass it to 'find' method to retrive data from daily_report_model 
    def daily_report_from_datestamp(self, device_id, timestamp, user_rac):
        if(device_id in user_rac or user_rac == 'admin'):
            key = {'device_id': device_id, 'timestamp': { "$gte": timestamp, "$lt": timestamp+ datetime.timedelta(days=+1)}}
            data_doc = self.__findindaily(key)
            return data_doc
        else:
            return -1
        
    # This method checks if the user has read access, then creates the key with both timestamp for range and pass it to 'find' method to retrive data from daily_report_model     
    def daily_report_by_datestamp_range(self, device_id, timestamp1, timestamp2, user_rac):
        if(device_id in user_rac  or user_rac == 'admin'):
            key = {'device_id': device_id, 'timestamp': { "$gte": timestamp1, "$lte": timestamp2 }}
            data_doc2 = self.__findindaily(key)
            return data_doc2
        else:
            return -1
        

    # Retrives all the record from device id and timestamp
    def find_by_device_id_and_timestamp_indaily(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__findindaily(key)

    
    # Retrives all the record with object id from daily_report_model database
    def find_by_object_id_indaily(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__findindaily(key)

    # Inserts the record to daily_report_model database
    def insert(self, cal_res):
        wdata_obj_id = self._db.insert_single_data(DailyReportModel.DAILY_REPORT_MODEL, cal_res)
        return self.find_by_object_id_indaily(wdata_obj_id)

        