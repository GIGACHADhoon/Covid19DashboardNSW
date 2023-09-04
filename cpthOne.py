from sql_tools import azSqlDB
import plotly.express as px
from datetime import date
import pandas as pd
import plotly.graph_objects as go

class cpthOne:

    def __init__(self):
        self.dbcon = azSqlDB()
        self.df = self.dbcon.getCc()
        self.gdf = self.dbcon.getGeo()
        self.geoJSON = self.gdf.__geo_interface__
        self.lgaLookup = {feature['properties']['lgaCode']: feature for feature in self.geoJSON['features']}
        self.getName = self.dbcon.getDetails()
    
    

    def get_figure(self,location,st,ed):
        if not st:
            st = date(2020,1,5)
        if not ed:
            ed = date(2023,8,24)
        df = self.df[(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))].groupby(['lgaCode','lgaName'])['Confirmed Cases'].sum().reset_index()
        # Base choropleth layer --------------#
        fig = px.choropleth_mapbox(df,geojson=self.geoJSON,locations='lgaCode',labels={'css':'Confirmed Cases'},featureidkey="properties.lgaCode", \
                                   hover_name='lgaName',color='Confirmed Cases',opacity =0.25)

        # Second layer - Highlights ----------#
        if location:
            # highlights contain the geojson information for only 
            # the selected districts
            fig.add_trace(
                px.choropleth_mapbox(df,geojson=self.get_highlights(location),locations='lgaCode',featureidkey="properties.lgaCode", \
                                     hover_name='lgaName',color='Confirmed Cases',opacity =1).data[0])

        fig.update_layout(mapbox_style="open-street-map",
                        mapbox_zoom=8,
                        mapbox_center={"lat": -33.868820, "lon": 151.209296},
                        height = 600,
                        paper_bgcolor="rgba(240,240,240,1)",
                        plot_bgcolor="rgba(240,240,240,1)")
        return fig

    def get_highlights(self,location):
        geojson_highlights = {}
        for k in self.geoJSON.keys():
            if k != 'features':     
                geojson_highlights[k] = self.geoJSON[k]
            else:
                geojson_highlights[k] = [self.lgaLookup[location]]
        return geojson_highlights
    
    def get_sum(self,location,st,ed):
        df = self.df[(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))]
        if location:
            return df[df['lgaCode'] == location]['Confirmed Cases'].sum()
        else:
            return df['Confirmed Cases'].sum()
    
    def get_lga(self,location):
        ans = ''
        if location:
            ans = ans + self.getName[self.getName['lgaCode'] == location]['lgaName'].values[0] +', '
        return ans[:-2]
    
    def get_history(self,location,st,ed):
        fig = go.Figure()

        if not location:
            tits = ''
            if st and ed:
                df = self.df[(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))].groupby(['date'])['Confirmed Cases'].sum().reset_index()
                fig.add_trace(go.Scatter(x=df['date'],y=df['Confirmed Cases'],mode = 'lines'))
            else:
                df = self.df.groupby(['date'])['Confirmed Cases'].sum().reset_index()
                fig.add_trace(go.Scatter(x=df['date'],y=df['Confirmed Cases'],mode = 'lines'))
        else:
            tits = f'NSW Confirmed Cases for \n{self.getName[self.getName["lgaCode"] == location]["lgaName"].values[0]} LGA'    
            if st and ed:
                df = self.df[(self.df.lgaCode == location)&(self.df.date>=pd.to_datetime(st)) & (self.df.date<=pd.to_datetime(ed))]
                fig.add_trace(go.Scatter(x=df['date'],y=df['Confirmed Cases'],mode = 'lines',name=self.getName[self.getName["lgaCode"] == location]["lgaName"].values[0]))
            else:
                df = self.df[(self.df.lgaCode == location)]
                fig.add_trace(go.Scatter(x=df['date'],y=df['Confirmed Cases'],mode = 'lines',name=self.getName[self.getName["lgaCode"] == location]["lgaName"].values[0]))
                    

        current_height = fig.layout.height
        if current_height is None:
            current_height = 400  # Set a default height (adjust as needed)

        # Calculate the new height (25% of the current height)
        new_height = current_height * 0.75
        fig.update_layout(
            paper_bgcolor="rgba(240,240,240,1)",
            plot_bgcolor="rgba(240,240,240,1)",
            title=tits,
            xaxis_title="Date",
            yaxis_title="Confirmed Cases",
            height=new_height  # Set the new height
        )

        return fig
    
    def get_neighbors(self,location):
        region_of_interest = self.gdf[self.gdf['lgaCode'] == location]
        neighbors = self.gdf[self.gdf.touches(region_of_interest.unary_union)]
        return neighbors