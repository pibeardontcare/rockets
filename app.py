# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Extract min and max payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Extract unique launch sites for the dropdown options
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in spacex_df["Launch Site"].unique()
]

# Create a Dash application
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'padding': '40px',
        'margin': '20px auto',
        'maxWidth': '900px',
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'fontFamily': 'Arial'
    },
    children=[
        html.H1("SpaceX Launch Records Dashboard",
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

        # Dropdown for launch site selection
        dcc.Dropdown(
            id='site-dropdown',
            options=launch_sites,
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True,
            style={'marginBottom': '30px'}
        ),

        html.Div(dcc.Graph(id='success-pie-chart')),

        html.Br(),

        html.P("Payload range (Kg):", style={'marginTop': '20px'}),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={i: str(i) for i in range(0, 10001, 2500)},
            value=[min_payload, max_payload]
        ),

        html.Br(),

        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)


# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df_all = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df_all, names='Launch Site', title='Total Success Launches by Site')
    else:
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(df_site, names='class', title=f'Total Launch Outcomes for site: {selected_site}')
    return fig

# Callback for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if selected_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]

    fig = px.scatter(df_filtered,
                     x='Payload Mass (kg)',
                     y='class',
                     color='Booster Version Category',
                     title=f'Payload vs. Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

