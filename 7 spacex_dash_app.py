# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} Kg' for i in range(0, 11000, 1000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function to update the pie chart based on selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Pie chart showing total successful launches by site
        fig = px.pie(spacex_df,
                     names='Launch Site',
                     values='class',
                     title='Total Successful Launches by Site')
    else:
        # Filter the DataFrame for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

        # Pie chart showing success vs failure for the selected site
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Success vs Failed Launches for {selected_site}',
                     color_discrete_map={0: 'red', 1: 'green'},
                     labels={'class': 'Launch Outcome'})
    return fig

# TASK 4: Callback function to update the scatter chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site != 'ALL':
        # Further filter the DataFrame for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Scatter plot showing the correlation between payload mass and launch outcome
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites' if selected_site == 'ALL'
              else f'Correlation between Payload and Success for {selected_site}',
        labels={'class': 'Launch Outcome'},
        hover_data=['Payload Mass (kg)', 'Booster Version Category']
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server()
