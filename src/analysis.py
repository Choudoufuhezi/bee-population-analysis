import mysql.connector
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import xgboost as xgb
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import shap
import os

def connect_to_db(port_num, host_name):
    """
    connect to mysql
    """
    connection = mysql.connector.connect(
        host = host_name,
        user = 'system',
        password = '123456',
        database = 'bee_population_analysis_db',
        port = port_num
    )

    return connection

def load_sql_to_db(connection, sql_file_path):
    """
    load the sql file into the server
    """
    cursor = connection.cursor()

    try:
        if os.path.exists(os.path.dirname(sql_file_path)):
            with open(sql_file_path, 'r') as f:
                doc = f.read()

            for i in doc.split(";"):
                i = i.strip()
                if i:
                    cursor.execute(i)
        
            connection.commit()
            return True
        
        else:
            raise FileNotFoundError(f"file {sql_file_path} not found")
    except Exception:
        return False
    
def year_percentage_lost(connection, year_lost_path):
    """
    year and average percentage loss of bee colonies as line chart
    """
    query = "SELECT Year, AVG(PercentLost) AS AveragePercentLost FROM Bee GROUP BY Year ORDER BY Year DESC"

    # Execute the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Extract data into separate lists for plotting
    years = []
    percent_lost = []

    for row in rows:
        years.append(row[0])
        percent_lost.append(row[1])

    # Make a dataframe for the plot
    data = {"years": years,
            "percent_lost": percent_lost}

    data = pd.DataFrame(data)
    data["percent_lost"] = pd.to_numeric(data["percent_lost"])

    # Create a line graph
    graph = alt.Chart(data).mark_line(color = "skyblue", point = True).encode(
        x = alt.X("years:O", title = 'Year', axis=alt.Axis(labelAngle= 0)),
        y = alt.Y("percent_lost:Q", title = 'Average Percentage Lost (%)', scale = alt.Scale(domain = [13, 15.6])),
        tooltip = [alt.Tooltip("years", title = "Year"),
                   alt.Tooltip("percent_lost", title = "Average Percentage Lost (%)", format='.2f')]
    ).properties(
        title = 'Average Percentage Lost of Bee Colonies in the USA Over Time',
        width = 600,
        height = 300
    ).configure_axis(
        grid = True
    )

    graph.save(year_lost_path)

    return graph
  

def year_temperature(connection, year_temperature_path):
    """
    year and average temperature as line chart
    """
    query_temperature = "SELECT Year, AVG(AverageTemperature) AS AverageTemperature FROM MonitorStation GROUP BY Year ORDER BY Year DESC"

    cursor = connection.cursor()
    cursor.execute(query_temperature)
    # Fetch all temperature rows
    temperature_rows = cursor.fetchall()

    # Extract data into separate lists for plotting
    years_temperature = []
    average_temperature = []
    for row in temperature_rows:
        years_temperature.append(row[0])
        average_temperature.append(row[1])

    # Make a dataframe for the plot
    data = {"years_temperature": years_temperature,
            "average_temperature": average_temperature}

    data = pd.DataFrame(data)
    data["average_temperature"] = pd.to_numeric(data["average_temperature"])

    # Create a line graph
    graph = alt.Chart(data).mark_line(color = "orange", point = {"color":"orange", "size": 60}).encode(
            x = alt.X("years_temperature:O", title = 'Year', axis=alt.Axis(labelAngle= 0)),
            y = alt.Y("average_temperature:Q", title = 'Average Temperature (°C)', scale = alt.Scale(domain = [53, 56.5])),
            tooltip = [alt.Tooltip("years_temperature", title = "Year"),
                       alt.Tooltip("average_temperature", title = "Average Temperature (°C)", format='.2f')]
        ).properties(
            title = 'Average Temperature in the USA Over Time',
            width = 600,
            height = 300
        ).configure_axis(
            grid = True
        )
    
    graph.save(year_temperature_path)

    return graph

def year_pesticide(connection, year_pesticide_path):
    """
    year and average pesticide as line chart
    """
    # Query to retrieve average pesticide usage data for each year for the whole USA
    query = """
        SELECT Year, AVG((LowEstimate + HighEstimate) / 2) AS AveragePesticideUsage
        FROM Pesticide
        GROUP BY Year
        ORDER BY Year
    """
    # Execute the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Extract data into separate lists for plotting
    years = []
    average_pesticide_usage = []

    for row in rows:
        years.append(row[0])
        average_pesticide_usage.append(row[1])

    # Make a dataframe for the plot
    data = {"years": years,
            "average_pesticide_usage": average_pesticide_usage}

    data = pd.DataFrame(data)
    data["average_pesticide_usage"] = pd.to_numeric(data["average_pesticide_usage"])

    # Create a line graph
    graph = alt.Chart(data).mark_line(color = "green", point = {"color":"green", "size": 60}).encode(
        x = alt.X("years:O", title = 'Year', axis=alt.Axis(labelAngle= 0)),
        y = alt.Y("average_pesticide_usage:Q", title = 'Average Pesticide Usage (kg)', scale = alt.Scale(domain = [5200, 5900])),
        tooltip = [alt.Tooltip("years", title = "Year"),
                alt.Tooltip("average_pesticide_usage", title = "Average Pesticide Usage (kg)", format='.2f')]
    ).properties(
        title = 'Average Pesticide Usage in the USA Over Time',
        width = 600,
        height = 300
    ).configure_axis(
        grid = True
    )

    graph.save(year_pesticide_path)

    return graph


def year_AQI(connection, year_aqi_path):
    """
    year and AQI as line chart
    """
    query = "SELECT Year, Name, AVG(AverageAQI) AS AverageAQI FROM GasConditions GROUP BY Year, Name ORDER BY Year, Name"

    # Execute the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Extract data into separate lists for plotting
    years = []
    gases = []
    average_aqi_values = []

    for row in rows:
        years.append(row[0])
        gases.append(row[1])
        average_aqi_values.append(row[2])

    # Get unique gases
    unique_gases = list(set(gases))

    # Make a dataframe for the plot
    data = {"years": years,
            "gases": gases, 
            "average_aqi_values": average_aqi_values}

    data = pd.DataFrame(data)
    data["average_aqi_values"] = pd.to_numeric(data["average_aqi_values"])


    # Create a line graph
    graph = alt.Chart(data).mark_line(point = True).encode(
        x = alt.X("years:O", title = 'Year', axis=alt.Axis(labelAngle= 0)),
        y = alt.Y("average_aqi_values:Q", title = 'Average AQI'),
        color = "gases",
        tooltip = [alt.Tooltip("years", title = "Year"),
                alt.Tooltip("gases", title = "Gase Type"),
                alt.Tooltip("average_aqi_values", title = "Average AQI", format='.2f')]
    ).properties(
        title = 'Average AQI of Gas Conditions in the USA Over Time',
        width = 600,
        height = 300
    ).configure_axis(
        grid = True
    )

    graph.save(year_aqi_path)

    return graph


def top_ten_states_bee_loss(connection, state_bee_loss_path):
    # Query to retrieve top 10 states with the most percentage lost of bees
    query = """
        SELECT State, AVG(PercentLost) AS AveragePercentLost
        FROM Bee
        GROUP BY State
        ORDER BY AveragePercentLost DESC
        LIMIT 10;
    """

    # Execute the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Extract data into separate lists for plotting
    states = []
    percent_lost = []

    for row in rows:
        states.append(row[0])
        percent_lost.append(row[1])

    # Make a dataframe for the plot
    data = {"states": states,
            "percent_lost": percent_lost}

    data = pd.DataFrame(data)
    data["percent_lost"] = pd.to_numeric(data["percent_lost"])

    # Plot data using a bar chart
    graph = alt.Chart(data).mark_bar(color = "skyblue").encode(
        x = alt.X("states:N", title = 'State', axis=alt.Axis(labelAngle= -45)),
        y = alt.Y("percent_lost:Q", title = 'Average Percentage Lost (%)'),
        tooltip = [alt.Tooltip("states", title = "State"),
                alt.Tooltip("percent_lost", title = "Average Percentage Lost (%)", format='.2f')]
    ).properties(
        title = 'Top 10 States with the Most Percentage Lost of Bees',
        width = 600,
        height = 300
    )

    graph.save(state_bee_loss_path)

    return graph


def top_ten_states(connection):
    """
    return the top 10 states with the highest avergae pencentage loss in bee colonies
    """
    query = """
        SELECT State, AVG(PercentLost) AS AveragePercentLost
        FROM Bee
        GROUP BY State
        ORDER BY AveragePercentLost DESC
        LIMIT 10;
    """

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    # Extract state names from the fetched rows
    top_10_states = [row[0] for row in rows]

    return top_10_states


def fetch_percentage_diseaselost(connection, query):
    """
    Fetch data for percentage lost by disease
    """
    cursor = connection.cursor()
    cursor.execute(query)
    percentage_diseaselost_data = cursor.fetchall()
    years_lost = [row[0] for row in percentage_diseaselost_data]
    percentage_lost_by_disease = [row[1] for row in percentage_diseaselost_data]

    return years_lost, percentage_lost_by_disease


def fetch_parasite(connection, query):
    """
    Fetch data for percentage affected by parasites
    """
    cursor = connection.cursor()
    cursor.execute(query)
    parasite_data = cursor.fetchall()
    years_parasite = [row[0] for row in parasite_data]
    percentage_parasite = [row[1] for row in parasite_data]

    return years_parasite, percentage_parasite

def fetch_colony_tracker(connection, query):
    """
    Fetch data for colony tracker
    """
    cursor = connection.cursor()
    cursor.execute(query)
    colony_tracker_data = cursor.fetchall()
    colony_years = [row[0] for row in colony_tracker_data]
    colony_values = [row[1] for row in colony_tracker_data]
    lost_colonies = [row[2] for row in colony_tracker_data]
    added_colonies = [row[3] for row in colony_tracker_data]

    return colony_years, colony_values, lost_colonies, added_colonies

def fetch_pesticide_usage(connection, query):
    """
    Fetch pesticide usage data
    """
    cursor = connection.cursor()
    cursor.execute(query)
    pesticide_data = cursor.fetchall()
    years = [row[0] for row in pesticide_data]
    low_estimate = [row[1] for row in pesticide_data]
    high_estimate = [row[2] for row in pesticide_data]

    return years, low_estimate, high_estimate

def fetch_aqi(connection, query):
    """
    Fetch AQI data for each gas
    """
    cursor = connection.cursor()
    cursor.execute(query)
    aqi_data = cursor.fetchall()
    gas_names = set(row[1] for row in aqi_data)
    gas_data = {gas_name: ([], []) for gas_name in gas_names}

    for row in aqi_data:
        year, gas_name, aqi_value = row
        gas_data[gas_name][0].append(year)
        gas_data[gas_name][1].append(aqi_value)
    
    return gas_data, aqi_data

def fetch_temperature(connection, query):
    """
    Fetch temperature data for the state
    """
    cursor = connection.cursor()
    cursor.execute(query)
    temperature_data = cursor.fetchall()
    years = [row[0] for row in temperature_data]
    temperatures = [row[1] for row in temperature_data]

    return years, temperatures

def plot_1_render(state, years_parasite, years_lost, percentage_parasite, percentage_lost_by_disease):
    """
    Plot 1: Percentage lost by disease and parasite
    """
    plot_1_data = pd.DataFrame({"year": years_parasite + years_lost,
                                "percentage" : percentage_parasite + percentage_lost_by_disease,
                                "type": ["Percentage Affected by Parasites"] * len(years_parasite) + ["Percentage Lost by Disease"] * len(years_lost)})
    
    plot_1_data["percentage"] = pd.to_numeric(plot_1_data["percentage"])

    graph = alt.Chart(plot_1_data).mark_line(point = True).encode(
            x = alt.X("year:O", title = "Year", axis=alt.Axis(labelAngle=0)), 
            y = alt.Y("percentage:Q", title = "Percentage Lost"),
            color = alt.Color("type:N", scale = alt.Scale(range = ["red", "blue"]), legend=alt.Legend(title='Legend')),
            tooltip = [alt.Tooltip("year", title = "Year"),
                    alt.Tooltip("percentage", title = "Percentage Lost", format='.2f')]
        ).properties(
            title = (f'Percentage Lost by Disease and Parasite in {state}'),
            width = 350
        )
    
    return graph


def plot_2_render(state, colony_years, colony_values, lost_colonies, added_colonies):
    """
    Plot 2: Colony tracker
    """
    plot_2_data = pd.DataFrame({"year": colony_years + colony_years + colony_years,
                                "number": colony_values + lost_colonies + added_colonies,
                                "type": ["Total Colonies"] * len(colony_years) +  ["Lost Colonies"] * len(colony_years) + ["Added Colonies"] * len(colony_years)})
    
    plot_2_data["number"] = pd.to_numeric(plot_2_data["number"])

    graph = alt.Chart(plot_2_data).mark_line(point = True).encode(
            x = alt.X("year:O", title = "Year", axis=alt.Axis(labelAngle=0)), 
            y = alt.Y("number:Q", title = 'Number of Colonies'),
            color = alt.Color("type:N", scale = alt.Scale(domain = ["Total Colonies", "Lost Colonies", "Added Colonies"],
                                                        range = ["black", "red", "green"])),
            tooltip = [alt.Tooltip("year", title = "Year"),
                    alt.Tooltip("number", title = "Number of Colonies")]
        ).properties(
            title = (f'Colony Tracker in {state}'),
            width = 350
        )
    
    return graph


def plot_3_render(state, years, low_estimate, high_estimate):
    """
    Plot 3: Pesticide usage 
    """
    plot_3_data = pd.DataFrame({"year": years + years,
                                "number": low_estimate + high_estimate,
                                "type": ["Low Estimate"] * len(years) +  ["High Estimate"] * len(years)})
    
    plot_3_data["number"] = pd.to_numeric(plot_3_data["number"])

    graph = alt.Chart(plot_3_data).mark_line(point = True).encode(
            x = alt.X("year:O", title = "Year", axis=alt.Axis(labelAngle=0)), 
            y = alt.Y("number:Q", title = 'Pesticide Usage (kg)'),
            color = alt.Color("type:N", scale = alt.Scale(domain = ["Low Estimate","High Estimate"],
                                                        range = ["blue", "green"])),
            tooltip = [alt.Tooltip("year", title = "Year"),
                    alt.Tooltip("number", title = "Pesticide Usage (kg)")]
        ).properties(
            title = (f'Pesticide Usage in {state} Over the Years'),
            width = 350
        )
    
    return graph


def plot_4_render(state, aqi_data):
    """
    Plot 4: Average AQI for each gas
    """
    plot_4_data = pd.DataFrame(aqi_data, columns = ["year", "type", "value"])

    plot_4_data["value"] = pd.to_numeric(plot_4_data["value"])

    graph = alt.Chart(plot_4_data).mark_line(point = True).encode(
            x = alt.X("year:O", title = "Year", axis=alt.Axis(labelAngle=0)), 
            y = alt.Y("value:Q", title = 'Average AQI'),
            color = alt.Color("type:N", scale = alt.Scale(domain = ["CO", "O3", "NO2", "SO2"],
                                                        range = ["blue", "orange", "green", "red"])),
            tooltip = [alt.Tooltip("year", title = "Year"),
                    alt.Tooltip("value", title = "Average AQI", format='.2f')]
        ).properties(
            title = (f'AQI for Each Gas in {state} Over the Years'),
            width = 350
        )
    
    return graph

def plot_5_render(state, years, temperatures):
    """
    Plot 5: Average temperature change 
    """
    plot_5_data = pd.DataFrame({"year": years,
                                "temperatures": temperatures})
    
    plot_5_data["temperatures"] = pd.to_numeric(plot_5_data["temperatures"])
    graph = alt.Chart(plot_5_data).mark_line(point = True).encode(
            x = alt.X("year:O", title = "Year", axis=alt.Axis(labelAngle=0)), 
            y = alt.Y("temperatures:Q", title = 'Average Temperature (°C)', scale = alt.Scale(zero=False)),
            tooltip = [alt.Tooltip("year", title = "Year"),
                    alt.Tooltip("temperatures", title = "Average Temperature (°C)", format='.2f')]
        ).properties(
            title = (f'Temperature Change in {state} Over the Years'),
            width = 350
        )

    return graph



def concat_plots(plot1, plot2, plot3, plot4, path):
    v1_1 = alt.hconcat(plot1, plot2)
    v1_2 = alt.hconcat(plot3, plot4)
    plot = alt.vconcat(v1_1, v1_2)

    plot.save(path)

    return plot

def query_transform_dataframe(connection, query, columns_selected):
    """
    query and transform data into dataframe
    """
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    dataframe = pd.DataFrame(rows, columns=columns_selected)

    return dataframe


def combined_dataframe(monitor_station_df, monitor_df):
    """
    Merge the DataFrames on 'CentroidLongitude', 'CentroidLatitude', and 'Year'
    """
    combined_df = pd.merge(
        monitor_station_df, 
        monitor_df, 
        how='inner', 
        left_on=['CentroidLongitude', 'CentroidLatitude', 'Year'],
        right_on=['CentroidLongitude', 'CentroidLatitude', 'StationYear']
        )
    
    return combined_df


def temp_dataframe(combined_df):
    """
    Selecting specific columns and creating a new DataFrame
    """
    temp_df = combined_df[['RiskFactorsReportedState', 'Year', 'AverageTemperature']].copy()

    # Renaming the column 'RiskFactorsReportedState' to 'State'
    temp_df.rename(columns={'RiskFactorsReportedState': 'State'}, inplace=True)

    return temp_df


def final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df):
    """
    Merge everything as a final dataframe 
    """
    merged1 = pd.merge(temp_df, gas_conditions_df, how='inner', 
                left_on=['State', 'Year'], right_on=['State', 'Year'])

    # select response variable %loss from bee_df, and merge by 'State' and 'Year'
    bee1 = bee_df[['PercentLost', 'State', 'Year', 'PercentLostByDisease']].copy()
    data1 = pd.merge(merged1, bee1, how='inner', 
                    left_on=['State', 'Year'], right_on=['State', 'Year'])

    # Pivot the table to transform GasName values into separate columns, with MeanValue as values
    data_pivot = data1.pivot_table(index=['State', 'Year', 'AverageTemperature', 
                                        'PercentLost', 'PercentLostByDisease'],
                                columns='GasName', 
                                values='MeanValue').reset_index()

    # Rename columns to add '_conc' suffix to gas concentration columns
    data_pivot.columns = [str(col) + '_conc' if col not in ['State', 'Year',
                                                            'AverageTemperature', 'PercentLost', 
                                                            'PercentLostByDisease'] else col for col in data_pivot.columns]

    # Now merge the pivoted data back with AverageAQI and PercentLost, and also add pesticide data
    data2 = pd.merge(data_pivot, data1[['State', 'Year', 'PercentLost', 'PercentLostByDisease']].drop_duplicates(), 
                        on=['State', 'Year', 'PercentLost', 'PercentLostByDisease'], 
                        how='left')
    pesticide_df['PesticideEstimate'] = pesticide_df[['LowEstimate', 'HighEstimate']].mean(axis=1)

    # Drop the LowEstimate and HighEstimate columns
    pesticide_df.drop(['LowEstimate', 'HighEstimate'], axis=1, inplace=True)

    data = pd.merge(data2, pesticide_df, on=['State', 'Year'])

    # Drop the O3_conc column
    data.drop('O3_conc', axis=1, inplace=True)

    # Display the final merged DataFrame for analysis
    return data

def check_linearity(data, variable, path):
    """
    Plot to check linearity
    """
    plt.figure(figsize=(10, 6))
    sns.lmplot(x=variable, y='PercentLost', data=data, aspect=1.5)
    plt.suptitle(f'Relationship between {variable} and PercentLost')
    plt.savefig(path)
    plt.close()
    graph = plt.gca()
    return graph

def check_vif(data):
    """
    checking multicollinearity measured by VIF score
    """
    features = data[['AverageTemperature', 'CO_conc', 'NO2_conc', 'SO2_conc', 'PercentLostByDisease', 'PesticideEstimate']]

    # Calculating VIF for each feature
    vif_data = pd.DataFrame()
    vif_data['Variable'] = features.columns
    vif_data['VIF'] = [variance_inflation_factor(features.values, i) for i in range(len(features.columns))]
    return vif_data

def correlation(data, path):
    """
    generate correlation matrix
    """
    correlation_matrix = data[['AverageTemperature', 'CO_conc', 'NO2_conc', 'SO2_conc', 'PercentLostByDisease', 'PesticideEstimate']].corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(13, 12))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='Blues', 
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    plt.savefig(path)
    plt.close()
    graph = plt.gca()
    return graph


def linear_model(data, path):
    """
    fit a ordinary least squares(OLS) model 
    """
    encoder = OrdinalEncoder()

    data['State_encoded'] = encoder.fit_transform(data[['State']])
    # Drop the non-numeric 'State' column if it's still in the DataFrame
    X = data.drop(['PercentLost', 'State'], axis=1)

    # Ensure that 'State_encoded' is used as a predictor
    X['State_encoded'] = data['State_encoded']

    # Add a constant to the model (intercept)
    X = sm.add_constant(X)

    y = data['PercentLost']  # Response variable

    # Fit the regression model
    model = sm.OLS(y, X).fit()

    with open(path, "wb") as p:
        pickle.dump(model, p)

    return X, y, model


def non_linear_model(X, y, shap_train_path, shap_overall_path):
    """
    fit a XGBoost model
    """
    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # Initialize XGBoost regressor
    xgb_model = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                                max_depth = 5, alpha = 10, n_estimators = 100)

    # Fit the model
    xgb_model.fit(X_train, y_train)

    # Predict the model
    y_pred = xgb_model.predict(X_test)

    # Compute and print the performance metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Compute SHAP values
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_train)

    # Plot the SHAP values - summary plot
    shap.summary_plot(shap_values, X_train)
    plt.savefig(shap_train_path)
    plt.close()

    shap.summary_plot(shap_values, X, plot_type="bar")
    plt.savefig(shap_overall_path)
    plt.close()

    return xgb_model