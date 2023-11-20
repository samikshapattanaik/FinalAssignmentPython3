# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


import pandas as pd


URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"


automobile_data = pd.read_csv(URL, encoding="ISO-8859-1", dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str})


# Create a dash application
app = dash.Dash(_name_)


app.layout = html.Div(children=[
    html.H1('Automobile Sales Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in range(1980, 2024, 1)],
        placeholder='Select a year',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),
    
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Select Statistics',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),
    
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_stat):
    if selected_stat == 'Yearly Statistics':
        return False
    else:
        return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'),
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_statistics, input_year):


    if selected_statistics == 'Recession Period':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        # Create plots or perform calculations based on recession_data


    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter the data for the selected year
        yearly_rec = data[data['Year'] == int(input_year)]
        # Create plots or perform calculations based on yearly_rec


        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using line chart
        # Grouping data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()


        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',  # Replace with your actual column name for the x-axis
                y='Automobile_Sales',  # Replace with your actual column name for the y-axis
                title="Automobile Sales Fluctuation over Recession Period (Year-wise)"
            )
        )


        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        # Grouping data for plotting
        avg_sales_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()


        # Plotting the bar chart
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales_by_vehicle_type,
                x='Vehicle_Type',  
                y='Automobile_Sales',  
                title="Average Number of Vehicles Sold by Vehicle Type"
            )
        )


        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        # Grouping data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()


        # Plotting the pie chart
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',  
                names='Vehicle_Type',  
                title="Total Expenditure Share by Vehicle Type during Recessions"
            )
        )


        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        # Grouping data for plotting
        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()


        # Creating Bar chart
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='Vehicle_Type',  
                y='Automobile_Sales',  
                color='unemployment_rate',  
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )


        # Returning the chart items
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart4),
                html.Div(children="Effect of Unemployment Rate on Vehicle Type and Sales")
            ]),
        ]
    else:
        return []  # Return an empty list if no valid statistics are selected




# Run the application                   
if _name_ == '_main_':
    app.run_server()
