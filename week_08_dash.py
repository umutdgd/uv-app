import dash
from dash import Dash, html, dcc, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Input, Output, State

df_new = pd.read_csv('df_new.csv', parse_dates=['daylight_time','date'])
df_monthly_new = pd.read_csv('df_monthly_new.csv', parse_dates=['avg_daylight_time'])

color_map = {'Berlin': '#C8A2C8', 'Izmir': '#FFA500', 'Lisbon': 'green'}


fig1 = px.bar(df_monthly_new, 
             x='month_of_year', 
             y='avg_temp_monthly',  
             color='city',
             barmode='group',
             height=300, title = "Avg Temperatur Berlin - Lisbon - Izmir",
             color_discrete_map=color_map)
fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
fig1.show()

graph1 = dcc.Graph(figure=fig1)

fig2 = px.scatter(data_frame=df_new,
                  x='date',
                  y='daylight_time', 
                  height=800,
                  title="Daylight time",
                  color='city',
                  color_discrete_map=color_map)

fig2 = fig2.update_layout(
    plot_bgcolor="#222222",
    paper_bgcolor="#222222",
    font_color="white",
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False)
)

fig2.show()
graph2 = dcc.Graph(figure=fig2)

fig3 = px.line(data_frame=df_monthly_new,
              x='month_of_year',
              y='avg_uv_monthly', 
              height=800,
              title="UV Level",
              color='city',
             range_y=[1,10],
              color_discrete_map=color_map)
fig3 = fig3.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="white",
        geo_bgcolor="#222222",
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False))
  
fig3.show()
graph3 = dcc.Graph(figure=fig3)

fig4 = px.scatter(df_monthly_new, 
           x="year", 
           y="avg_uv_monthly", 
           animation_frame="month_of_year", 
           size="avg_uv_monthly", color="city", 
           hover_name="city",
           #log_x=True, 
           size_max=20, 
           #range_x=['may','march'], 
           range_y=[0,10],
           category_orders={"month_of_year": df_monthly_new["month_of_year"].unique()[::5]})
fig4 = fig4.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="white",
        geo_bgcolor="#222222")
fig4.show()

graph4 = dcc.Graph(figure=fig4)

fig5 = px.choropleth(df_monthly_new,
                     locations='alpha-3',
                     projection='natural earth',
                     animation_frame="month_of_year",
                    scope='world',
                     hover_data='avg_uv_monthly',
                    color='avg_uv_monthly',
                    locationmode='ISO-3', 
                    color_continuous_scale='YlOrRd',
                    category_orders={"month_of_year": df_monthly_new["month_of_year"].unique()[::5]})
                    #mapbox_style='carto-positron')

fig5 = fig5.update_layout(
        plot_bgcolor="#222222",
        paper_bgcolor="#222222",
        font_color="white",
        geo_bgcolor="#222222")

fig5.show()
graph5 = dcc.Graph(figure=fig5)

import dash_bootstrap_components as dbc

graph = dcc.Graph()
cities =df_monthly_new['city'].unique().tolist() 

app =dash.Dash(external_stylesheets=[dbc.themes.LITERA])

# Do not forget to add server

server=app.server

dropdown = dcc.Dropdown(['Berlin', 'Lisbon', 'Izmir'],  value=['Berlin', 'Lisbon', 'Izmir'],
                        clearable=False, multi=True, style ={'paddingLeft': '30px', 
                                                             "backgroundColor": "#222222", "color": "#222222"})

app.layout = html.Div([html.H1('Day light Analysis of Berlin - Lisbon - Izmir', style={'textAlign': 'center', 'color': '#FFA500'}), 
                       html.Div(html.P("Using Weather.api data to analys UV and Daylight time of Berlin - Lisbon - Izmir"), 
                                style={'textAlign': 'center'}),
                       html.Div([html.Div('Berlin - Lisbon - Izmir',
                                          style={'textAlign': 'center','backgroundColor': '#FFA500', 'color': 'black', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}), 

                                 dropdown, graph1,  graph2, graph3,  graph4,  graph5])
                                 #dcc.Graph(figure=fig1),  
                                 #dcc.Graph(figure=fig2), 
                                 #dcc.Graph(figure=fig3),
                                 #dcc.Graph(figure=fig4),
                                 #dcc.Graph(figure=fig5)])

                    
])

@callback(                       
    Output(graph1, "figure"),  
    Input(dropdown, "value"))

def update_bar_chart(city): # it will be city instead country for my case
    mask = df_monthly_new["city"] == city # coming from the function parameter
    fig =px.bar(df_monthly_new[mask], 
             x='month_of_year', 
             y='avg_temp_monthly',  
             color='city',
             barmode='group',
             height=300, title = "Avg Temperatur Berlin - Lisbon - Izmir",
             color_discrete_map=color_map)
    fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    return fig

if __name__ == '__main__':
     app.run_server()