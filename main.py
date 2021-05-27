from model import UserModel, DeviceModel, WeatherDataModel, DailyReportModel
from datetime import datetime

# Shows how to initiate and search in the users collection based on a username
# Uncomment admin to see the admin rights
user_coll = UserModel()
user_document = user_coll.find_by_username('admin')
# user_document = user_coll.find_by_username('test_4')
user_role = user_document['role']

# Added 2 variables user_rac and user_wac which stores the read and write privileges for each user for each device
# Comment the user_rac and user_wac while running for the first time and
# uncomment only after inserting the user with read and write permissions
if user_role == 'admin':
    user_rac = 'admin'
    user_wac = 'admin'
else:
    user_rac = user_document['rac'].upper()
    user_wac = user_document['wac'].upper()

if user_document:
    print("Current User is :", user_document)



# USER CONTROL SECTION
# Added access control to allow only admin to have access to User Management
if user_role != 'admin':
    print("Sorry the user doesn't have admin privileges to add user")
else:
    # Shows a successful attempt on how to insert a user by admin only
    # Uncomment the below one by one to insert the user with read and write permissions after changing to admin user
    user_document = user_coll.insert('test_3', 'test_3@example.com', 'default', 'dt001,dt002,dt003', 'dt005,dt002')
    # user_document = user_coll.insert('test_4', 'test_4@example.com', 'default', 'dt004,dt005,dt006', 'dt005,dt002')
    # user_document = user_coll.insert('test_5', 'test_5@example.com', 'default', 'dt001,dt003', 'dt002')
    # user_document = user_coll.insert('test_6', 'test_6@example.com', 'default', 'dt001,dt002,dt003', 'dt005,dt002')
    if user_document == -1:
        print("Sorry, can't create the user!",user_coll.latest_error)
    else:
        print("New User Created :",user_document)



#DEVICE READ AND WRITE SECTION
# Shows how to initiate and search in the devices collection based on a device id
device_coll = DeviceModel()
# Passing user_rac along with device_id to the method to validate if the user has read access for the given device
dev_id = 'DT001'
device_document = device_coll.find_by_device_id(dev_id, user_rac)
if device_document == -1 or device_document == None:
    print("Sorry",dev_id,"doesn't exist or the current user has no read access to this device")
else:
    print("Details for",dev_id,"is :",device_document)

# Shows a successful attempt on how to insert a new device
# Passing user_wac to the method to validate if the current user has write access to this device
device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme', user_wac)
if (device_document == -1):
    print("Sorry, can't insert this device into database!",device_coll.latest_error)
else:
    print(device_document)




#WEATHER DATA READ AND WRITE SECTION
# Shows how to initiate and search in the weather_data collection based on a device_id and timestamp
# User read access is managed by passsing user_wac list to the method and handled in model
wdata_coll = WeatherDataModel()
device_id = 'DT009'
wdata_document = wdata_coll.find_by_device_id_and_timestamp(device_id, datetime(2020, 12, 2, 13, 30, 0), user_rac)
if (wdata_document):
    print("Details for", device_id, "is :", wdata_document)
else:
    print("Sorry,",device_id,"doesn't exist or the current user has no read access to this weather device")

# Shows how to insert in the weather_data collection based on a device_id and timestamp
# User write access is managed by passsing user_wac list to the method and handled in model
wdata_document = wdata_coll.insert('DT009', 12, datetime(2020, 12, 2, 13, 30, 0), user_wac)
if (wdata_document == -1):
    print(wdata_coll.latest_error)
else:
    print(wdata_document)




#DAILY REPORT SECTION
# Shows how to initiate and search in the daily_report_model collection based on a device_id and timestamp
# Passing user_rac to the method to validate if the user has read access for the given device
dailyreport_coll = DailyReportModel()
dev_id2 = 'DT002'
dailyreport_document = dailyreport_coll.daily_report_from_datestamp(dev_id2, datetime(2020, 12, 1), user_rac)
if(dailyreport_document):
    print("Daily report of",dev_id2,"for the given date is : ")
    print(dailyreport_document)
else:
    print("No Data for",dev_id2,"found on the given date or the user doesn't have read access for this device")


# Shows how to initiate and search in the daily_report_model collection based on a device_id and range of timestamp
# Passing user_rac to the method to validate if the user has read access for the given device
dev_id3 = 'DT001'
rangedailyreport_document = dailyreport_coll.daily_report_by_datestamp_range(dev_id3, datetime(2020, 12, 2), datetime(2020, 12, 3), user_rac)
if(rangedailyreport_document==-1):
    print("No Data Found for",dev_id3,"in the given range")
else:
    print("Daily report for",dev_id3,"in the given range is : ")
    print(rangedailyreport_document)

# Shows how to insert the report from weather_db to daily_report_model collection based on device_id and timestamp
# Passing user_rac to the method to validate if the user has read access for the given device
# Bulk aggregator for the same functionality has been implemented in the setup.py
dev_id4 = 'DT005'
writedatafromweathertodaily_document = dailyreport_coll.insert_daily_report_to_daily_report_model(dev_id4, datetime(2020, 12, 2), user_wac)
if(writedatafromweathertodaily_document==-1):
    print("Summary data for",dev_id4,"already exist in daily report database for the given date or the user doesn't have write access for this device")
else:
    print("Report as shown below is inserted into Daily Report Model for the given datestamp : ")
    print(writedatafromweathertodaily_document)
