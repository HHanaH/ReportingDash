from re import S
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import pyodbc

#To do :
#1. Remplacer la partie conditions, choices par un merge avec BI_Dates
app = dash.Dash(__name__)
#server = app.server

#Import data

cnxn = pyodbc.connect(
    Trusted_Connection='Yes',
    Driver='{SQL Server Native Client 11.0}',
    Server='EMFRPARAPP01',
    Database='FNO_Datawarehouse'
)

df_debut = pd.read_sql_query("SELECT debut, Type FROM BI_RecurringGift WHERE debut>='20180701' AND Type IN('Parrainage enfant','Recurring gift') ORDER BY debut ASC",cnxn)
conditions = [
    (df_debut['debut'] >= pd.to_datetime('2018-07-01')) & (df_debut['debut'] <= pd.to_datetime('2019-06-30')),
    (df_debut['debut'] >= pd.to_datetime('2019-07-01')) & (df_debut['debut'] <= pd.to_datetime('2020-06-30')),
    (df_debut['debut'] >= pd.to_datetime('2020-07-01')) & (df_debut['debut'] <= pd.to_datetime('2021-06-30')),
    (df_debut['debut'] >= pd.to_datetime('2021-07-01')) & (df_debut['debut'] <= pd.to_datetime('2022-06-30')),
    (df_debut['debut'] >= pd.to_datetime('2022-07-01')) & (df_debut['debut'] <= pd.to_datetime('2023-06-30'))    ]
choices = ['FY19', 'FY20', 'FY21','FY22','FY23']
df_debut['FY'] = np.select(conditions, choices)
df_debut['month'] = pd.to_datetime(df_debut.debut, format='%Y-%m-%d %H:%M:%S').dt.strftime('%b')
df_debut = df_debut.groupby(['Type','FY','month']).agg({'debut':'count'}).reset_index()

fig_debutSP = px.histogram(df_debut.loc[df_debut.Type=='Parrainage enfant'], x='month', y='debut',
                barmode='group', color='FY',height=400, text_auto=True,
                category_orders={"month": ["Jul", "Aug", "Sep", "Oct", "Nov","Dec","Jan","Feb","Mar","Apr","May", "Jun"]},
                color_discrete_sequence = ['#A8E1FF', '#88C4FF', '#66A8FF', '#418CEC', '#0072ce'],
                template="simple_white",
                nbins=20)
fig_debutSP.update_traces(textposition='inside')



fig_debutSR = px.histogram(df_debut.loc[df_debut.Type=='Recurring gift'], x='month', y='debut',
                barmode='group', color='FY',height=400, text_auto=True,
                category_orders={"month": ["Jul", "Aug", "Sep", "Oct", "Nov","Dec","Jan","Feb","Mar","Apr","May", "Jun"]},
                color_discrete_sequence = ['#FFA89A', '#FF897E', '#FF6A63', '#F54A49', '#D22630'],
                template="simple_white")
fig_debutSR.update_traces(textposition='inside')



df_fin = pd.read_sql_query("SELECT datefin, Type FROM BI_RecurringGift WHERE datefin>='20180701' AND Type IN('Parrainage enfant','Recurring gift') ORDER BY datefin ASC",cnxn)
conditions = [
    (df_fin['datefin'] >= pd.to_datetime('2018-07-01')) & (df_fin['datefin'] <= pd.to_datetime('2019-06-30')),
    (df_fin['datefin'] >= pd.to_datetime('2019-07-01')) & (df_fin['datefin'] <= pd.to_datetime('2020-06-30')),
    (df_fin['datefin'] >= pd.to_datetime('2020-07-01')) & (df_fin['datefin'] <= pd.to_datetime('2021-06-30')),
    (df_fin['datefin'] >= pd.to_datetime('2021-07-01')) & (df_fin['datefin'] <= pd.to_datetime('2022-06-30')),
    (df_fin['datefin'] >= pd.to_datetime('2022-07-01')) & (df_fin['datefin'] <= pd.to_datetime('2023-06-30'))    ]
choices = ['FY19', 'FY20', 'FY21','FY22','FY23']
df_fin['FY'] = np.select(conditions, choices)
df_fin['month'] = pd.to_datetime(df_fin.datefin, format='%Y-%m-%d %H:%M:%S').dt.strftime('%b')
df_fin = df_fin.groupby(['Type','FY','month']).agg({'datefin':'count'}).reset_index()

fig_finSP = px.histogram(df_fin.loc[df_fin.Type=='Parrainage enfant'], x='month', y='datefin',
                barmode='group', color='FY',height=400, text_auto=True,
                category_orders={"month": ["Jul", "Aug", "Sep", "Oct", "Nov","Dec","Jan","Feb","Mar","Apr","May", "Jun"]},
                color_discrete_sequence = ['#A8E1FF', '#88C4FF', '#66A8FF', '#418CEC', '#0072ce'],
                template="simple_white"
                )
fig_finSP.update_traces(textposition='inside')

fig_finSR = px.histogram(df_fin.loc[df_fin.Type=='Recurring gift'], x='month', y='datefin',
                barmode='group', color='FY',height=400, text_auto=True,
                category_orders={"month": ["Jul", "Aug", "Sep", "Oct", "Nov","Dec","Jan","Feb","Mar","Apr","May", "Jun"]},
                color_discrete_sequence = ['#FFA89A', '#FF897E', '#FF6A63', '#F54A49', '#D22630'],
                template="simple_white")
fig_finSR.update_traces(textposition='inside')


months = ["Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin"]
df_Proj = pd.DataFrame(data={'MonthName': months,
                             'Recette_SP': [872234, 870577, 868921, 867265, 865608, 863952, 882715, 881058, 879402, 877746, 876090, 874432]})

df_Payment = pd.read_sql_query("SELECT PA.Date, AmountSplit, PurposeType, FiscalYear, MonthName FROM BI_Payment PA \
                              LEFT JOIN BI_Designation DE ON PA.DesignationLookupID = DE.DesignationLookupID \
                                LEFT JOIN BI_Dates DA ON PA.Date = DA.Date \
                                 WHERE PA.Date>='20220701' AND PurposeType='Child sponsorship' AND RecordStatus='A' \
                                    ORDER BY Date ASC",cnxn)
df_Payment['MonthName']=df_Payment['MonthName'].str.strip()

fig_RecettesSP = px.histogram(df_Payment, x='MonthName', y='AmountSplit',
                                barmode='group', text_auto=True)

fig_RecettesSP.add_trace(go.Scatter(x=months, y=df_Proj['Recette_SP']))


# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Recrutements", style={'textAlign': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='deb_SP', figure=fig_debutSP)
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='deb_SR', figure=fig_debutSR)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("Arrêts", style={'textAlign': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fin_SP', figure=fig_finSP)
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fin_SR', figure=fig_finSR)
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H1("Recette SP", style={'textAlign': 'center'})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='Recettes_SP', figure=fig_RecettesSP)
        ], width=12)
    ])


])
#-------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)