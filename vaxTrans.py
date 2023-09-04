from sql_tools import azSqlDB
import plotly.graph_objects as go

def transform_string(x):
        x = float(x.replace('%','').replace('>',''))
        if x < 1:
            x = x*100
        return x


class vaxTrans:

    def __init__(self):
        self.dbcon = azSqlDB()
        self.df = self.dbcon.getVax()
        self.df['dose1'] = self.df['dose1'].apply(lambda x : transform_string(x))
        self.df['dose2'] = self.df['dose2'].apply(lambda x : transform_string(x))
        self.df['dose3'] = self.df['dose3'].apply(lambda x : transform_string(x))
        self.df['dose4'] = self.df['dose4'].apply(lambda x : transform_string(x))


    def getLgas(self):
        return self.df.lgaName.unique()
    
    def updateFigure(self, dosage, lgas):
        fig = go.Figure()
        for gas in lgas:
            # Filter the DataFrame for the specific gas (lgaName) and add it to the figure
            filtered_df = self.df[self.df['lgaName'] == gas]
            fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df[dosage], mode='lines', name=gas))
        
        if dosage == 'dose1':
            tit = '1st Vaccine'
        elif dosage == 'dose2':
            tit = '2nd Vaccine'
        elif dosage == 'dose3':
            tit = '3rd Vaccine'
        else:
            tit= '4th Vaccine'

        fig.update_layout(
            paper_bgcolor="rgba(240,240,240,1)",
            plot_bgcolor="rgba(240,240,240,1)",
            title = tit,
            xaxis_title="Date",
            yaxis_title="Population Coverage (%)",

        )
        return fig
