import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

class azSqlDB:
    def __init__(self):
        server = os.getenv("server")
        database = os.getenv("database")
        username = os.getenv("username")
        password = os.getenv("password")
        self.conString = 'Driver={ODBC Driver 18 for SQL Server};SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+ \
            ';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
            
    #input tp specifies the time period of the confirmed cases
    def getCc(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT c.date,c.lgaCode,l.lgaName,c.cc  \
                        FROM [dbo].[confirmedCases] c \
                        LEFT JOIN  \
                        [dbo].[lgaDetails] l \
                        ON c.lgaCode = l.lgaCode"
                cursor.execute(query)
                rows = cursor.fetchall()
                df_dict = {'date':[],'lgaCode':[],'lgaName':[],'ccs':[]}
                for row in rows:
                    df_dict['date'].append(row[0])
                    df_dict['lgaCode'].append(row[1])
                    df_dict['lgaName'].append(row[2])
                    df_dict['ccs'].append(row[3])
                df = pd.DataFrame(df_dict)
                df['date'] = pd.to_datetime(df['date'])
                return df

    #input tp specifies the time period of the confirmed cases
    def getGeo(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT lgaCode,Geom.STAsBinary() FROM dbo.nswGeo"
                cursor.execute(query)
                rows = cursor.fetchall()
                df_dict = {'lgaCode':[],'geometry':[]}
                for row in rows:
                    df_dict['lgaCode'].append(row[0])
                    df_dict['geometry'].append(row[1])

                df = pd.DataFrame(df_dict)
                gdf_wkb= gpd.GeoSeries.from_wkb(df['geometry'])
                gdf = gpd.GeoDataFrame(df, geometry=gdf_wkb)
                gdf.set_index('lgaCode')
                return gdf
            
    def getDetails(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM [dbo].[lgaDetails]"
                cursor.execute(query)
                rows = cursor.fetchall()
                df_dict = {'lgaCode':[],'lgaName':[]}
                for row in rows:
                    df_dict['lgaCode'].append(row[0])
                    df_dict['lgaName'].append(row[1])

                df = pd.DataFrame(df_dict)
                return df
            