#creating tables
from connect2DB import *

class TABLES:
    # def USER_TABLE(self, dbase):
    #     # creating user_table
    #     mycursor = dbase.cursor()
    #     mycursor.execute("DROP TABLE IF EXISTS USER_table")
    #     mycursor.execute("CREATE TABLE User_table(ID varchar NOT NULL PRIMARY KEY ,"
    #                      "Email_ID varchar(30) Not NULL,Password varchar(300),"
    #                      "First_Name varchar(250) Not NULL,Last_Name varchar(250),"
    #                      " Username varchar NOT NULL,Created_on DATE, Updated_on DATE,Role varchar(20)NOT NULL);")
    #     dbase.commit()

    def USERS(self, dbase):
        # creating user_table
        mycursor = dbase.cursor()
        mycursor.execute("DROP TABLE IF EXISTS USERS")
        mycursor.execute("CREATE TABLE Users(User_ID INT  PRIMARY KEY ,"
                         "Email_ID varchar(50) Not NULL,Password varchar(1000) NOT NULL,"
                         "First_Name varchar(250) Not NULL,Last_Name varchar(250) NOT NULL,"
                         "Created_on DATE NOT NULL,Created_by varchar not null,"
                         " Updated_on DATE NOT NULL,Updated_by varchar not null,"
                         "Role varchar(20)NOT NULL,Teams Varchar Not NULL,Delete BIT null);")
        dbase.commit()

    # def ASSET_TABLE(self, dbase):
    #     # creating server_table
    #     mycursor = dbase.cursor()
    #     mycursor.execute("DROP TABLE IF EXISTS ASSET_table")
    #     mycursor.execute("CREATE TABLE Asset_TABLE(Asset_ID varchar NOT NULL PRIMARY KEY,"
    #                      "ID VARCHAR NOT NULL ,FOREIGN KEY(ID) REFERENCES User_TABLE(ID),"
    #                      "Manufacturer varchar NOT NULL, BMC_IP INET NOT NULL,"
    #                      " BMC_User varchar NOT NULL, BMC_Password varchar NOT NULL,"
    #                      " Asset_Location varchar NOT NULL, Reserved BOOL Not NULL,Assigned_on DATE,"
    #                      " Purpose varchar(300),Cluster_Id  Varchar Not NULL, Team_Id Varchar Not NULL,"
    #                      "DELETE BOOL,Status varchar );")
    #     dbase.commit()
    #
    # def HISTORIC_DETAILS(self, dbase):
    #     # creating historic_table
    #     mycursor = dbase.cursor()
    #     mycursor.execute("DROP TABLE IF EXISTS historic_DETAILS")
    #     mycursor.execute("CREATE TABLE Historic_details(H_Id varchar NOT NULL PRIMARY KEY,Asset_ID varchar NOT NULL,"
    #                      "FOREIGN KEY(Asset_ID) REFERENCES Asset_TABLE(Asset_ID),Updated_on DATE,Remarks varchar(300));")
    #     dbase.commit()
    # def CPU_SKU(self, dbase):
    #     # creating historic_table
    #     mycursor = dbase.cursor()
    #     mycursor.execute("DROP TABLE IF EXISTS CPU_SKU")
    #     mycursor.execute("CREATE TABLE cpu_sku(PL_ID VARCHAR(50) NOT NULL PRIMARY KEY ,"
    #                      "RAM_gb INT NOT NULL,STORAGE_gb INT NOT NULL,OS_IP INET NOT NULL,"
    #                      "OS_USER VARCHAR(50) NOT NULL,OS_PASSWORD VARCHAR(300) NOT NULL,"
    #                      "Asset_ID varchar NOT NULL,FOREIGN KEY(Asset_ID) REFERENCES Asset_TABLE(Asset_ID));")
    #     dbase.commit()
T=TABLES()
dbase=connectDB()
# T.USER_TABLE(dbase)
T.USERS(dbase)
# T.ASSET_TABLE(dbase)
# T.HISTORIC_DETAILS(dbase)
# T.CPU_SKU(dbase)
