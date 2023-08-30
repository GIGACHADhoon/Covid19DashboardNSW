from sql_tools import azSqlDB
import plotly.express as px
from datetime import date
import pandas as pd
class cpthOne:

    def __init__(self):
        self.dbcon = azSqlDB()
        self.df = self.dbcon.getCc()
        self.gdf = self.dbcon.getGeo()
        self.selections = set([])
        self.geoJSON = self.gdf.__geo_interface__
        self.lgaLookup = {feature['properties']['lgaCode']: feature for feature in self.geoJSON['features']}
        self.getName = self.dbcon.getDetails()

    def update_sel(self,location):
        if location not in self.selections:
            self.selections.add(location)
        else:
            self.selections.remove(location)


    def get_highlights(self):
        geojson_highlights = {}
        for k in self.geoJSON.keys():
            if k != 'features':
                geojson_highlights[k] = self.geoJSON[k]
            else:
                geojson_highlights[k] = [self.lgaLookup[selection] for selection in self.selections]        
        return geojson_highlights
    

    def get_figure(self,st,ed):
        if not st:
            st = date(2020,1,5)
        if not ed:
            ed = date(2023,8,24)
        df = self.df[(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))].groupby(['lgaCode','lgaName'])['Confirmed Cases'].sum().reset_index()
        # Base choropleth layer --------------#
        fig = px.choropleth_mapbox(df,geojson=self.geoJSON,locations='lgaCode',labels={'css':'Confirmed Cases'},featureidkey="properties.lgaCode", \
                                   hover_name='lgaName',color='Confirmed Cases',opacity =0.25,)

        # Second layer - Highlights ----------#
        if len(self.selections) > 0:
            # highlights contain the geojson information for only 
            # the selected districts

            fig.add_trace(
                px.choropleth_mapbox(df,geojson=self.get_highlights(),locations='lgaCode',featureidkey="properties.lgaCode", \
                                     hover_name='lgaName',color='Confirmed Cases',opacity =1).data[0])

        fig.update_layout(mapbox_style="open-street-map",
                        title_text = 'Select the LGAs and please Wait a few Seconds',
                        mapbox_zoom=6,
                        mapbox_center={"lat": -33.868820, "lon": 151.209296},
                        height = 600)
        return fig

    def get_sum(self,st,ed):
        df = self.df[(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))]
        ans = 0
        for sel in self.selections:
            ans += df[df['lgaCode'] == sel]['Confirmed Cases'].sum()
        return ans
    
    def get_lga(self):
        ans = ''
        for sel in self.selections:
            ans = ans + self.getName[self.getName['lgaCode'] == sel]['lgaName'].values[0] +', '
        return ans[:-2]