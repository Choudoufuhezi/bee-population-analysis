import sys
import os
import mysql.connector
import decimal
import re
import numpy as np
import pandas as pd
import altair as alt
from statsmodels.regression.linear_model import RegressionResultsWrapper
import xgboost as xgb
import matplotlib
matplotlib.use("Agg")
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.analysis import *


def test_connect_db():
    """
    test connect_to_db()
    """
    connection_output = connect_to_db(3307, 'localhost')
    connection_test = mysql.connector.connect(
        host = 'localhost',
        user = 'system',
        password = '123456',
        database = 'bee_population_analysis_db',
        port = 3307
    )

    assert(connection_output, connection_test)


def test_load_sql_db():
    """
    test load load_sql_to_db()
    """
    connection = connect_to_db(3307, 'localhost')
    assert(load_sql_to_db(connection, "scripts/output.sql"), True)
    assert(load_sql_to_db(connection, "scripts/output1.sql"), False)


def test_year_percent_lost():
    """
    test load year_percentage_lost()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    graph = year_percentage_lost(connection, "images/year_lost.png")
    assert(graph.encoding.x.shorthand == "years:O")
    assert(graph.encoding.y.shorthand == "percent_lost:Q")
    assert(graph.encoding.tooltip[0].shorthand == "years")
    assert(graph.encoding.tooltip[1].shorthand == "percent_lost")
    os.remove("images/year_lost.png")

def test_year_temperature():
    """
    test year_temperature()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    graph = year_temperature(connection, "images/year_temperature.png")
    assert(graph.encoding.x.shorthand == "years_temperature:O")
    assert(graph.encoding.y.shorthand == "average_temperature:Q")
    assert(graph.encoding.tooltip[0].shorthand == "years_temperature")
    assert(graph.encoding.tooltip[1].shorthand == "average_temperature")
    os.remove("images/year_temperature.png")


def test_year_pesticide():
    """
    test year_pesticide()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    graph = year_pesticide(connection, "images/year_pesticide.png")
    assert(graph.encoding.x.shorthand == "years:O")
    assert(graph.encoding.y.shorthand == "average_pesticide_usage:Q")
    assert(graph.encoding.tooltip[0].shorthand == "years")
    assert(graph.encoding.tooltip[1].shorthand == "average_pesticide_usage")
    os.remove("images/year_pesticide.png")


def test_year_AQI():
    """
    test year_AQI()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    graph = year_AQI(connection, "images/year_aqi.png")
    assert(graph.encoding.x.shorthand == "years:O")
    assert(graph.encoding.y.shorthand == "average_aqi_values:Q")
    assert(graph.encoding.color.shorthand == "gases")
    assert(graph.encoding.tooltip[0].shorthand == "years")
    assert(graph.encoding.tooltip[1].shorthand == "gases")
    assert(graph.encoding.tooltip[2].shorthand == "average_aqi_values")
    os.remove("images/year_aqi.png")
    

def test_top_ten_states_bee_loss():
    """
    test top_ten_states_bee_loss()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    graph = top_ten_states_bee_loss(connection, 'images/state_bee_loss.png')
    assert(graph.encoding.x.shorthand == "states:N")
    assert(graph.encoding.y.shorthand == "percent_lost:Q")
    assert(graph.encoding.tooltip[0].shorthand == "states")
    assert(graph.encoding.tooltip[1].shorthand == "percent_lost")
    os.remove("images/state_bee_loss.png")


def test_top_ten_states():
    """
    test top_ten_states()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    assert(len(states) == 10)
    for i in states:
        assert(type(i) == str)


def test_fetch_percentage_diseaselost():
    """
    test fetch_percentage_diseaselost()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT Year, PercentLostByDisease
        FROM Bee
        WHERE State = '{state}'
        ORDER BY Year
    """
    years_lost, percentage_lost_by_disease = fetch_percentage_diseaselost(connection, sample_query)
    assert(type(years_lost[0]) == int)
    assert(isinstance(percentage_lost_by_disease[0], decimal.Decimal))

    
def test_fetch_parasite():
    """
    test fetch_parasite()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT Year, PercentAffected
        FROM Parasite
        WHERE State = '{state}'
        ORDER BY Year
    """
    years_parasite, percentage_parasite = fetch_parasite(connection, sample_query)
    assert(type(years_parasite[0]) == int)
    assert(isinstance(percentage_parasite[0], decimal.Decimal))

def test_fetch_colony_tracker():
    """
    test fetch_colony_tracker
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT Year, Colony, LostColony, AddColony
        FROM Bee
        WHERE State = '{state}'
        ORDER BY Year
    """
    colony_years, colony_values, lost_colonies, added_colonies = fetch_colony_tracker(connection, sample_query)
    assert(type(colony_years[0]) == int)
    assert(type(colony_values[0]) == int)
    assert(type(lost_colonies[0]) == int)
    assert(type(added_colonies[0]) == int)


def test_fetch_pesticide_usage():
    """
    test fetch_pesticide_usage()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT Year, LowEstimate, HighEstimate
        FROM Pesticide
        WHERE State = '{state}'
        ORDER BY Year
    """
    years, low_estimate, high_estimate = fetch_pesticide_usage(connection, sample_query)
    assert(type(years[0]) == int)
    assert(isinstance(low_estimate[0], decimal.Decimal))
    assert(isinstance(high_estimate[0], decimal.Decimal))


def test_fetch_aqi():
    """
    test fetch_aqi()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT Year, Name, AverageAQI
        FROM GasConditions
        WHERE State = '{state}'
        ORDER BY Year
    """
    gas_data, aqi_data = fetch_aqi(connection, sample_query)

    first_gas = list(gas_data.keys())[0]
    assert(type(gas_data[first_gas][0][0]) == int)
    assert(isinstance(gas_data[first_gas][1][0], decimal.Decimal))

    assert(type(aqi_data[0][0]) == int)
    assert(type(aqi_data[0][1]) == str)
    assert(isinstance(aqi_data[0][2], decimal.Decimal))


def test_fetch_temperature():
    """
    test fetch_temperature()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    sample_query = f"""
        SELECT m.Year, m.AverageTemperature
        FROM MonitorStation m
        JOIN Detect d ON m.CentroidLongitude = d.CentroidLongitude 
                        AND m.CentroidLatitude = d.CentroidLatitude
                        AND m.Year = d.StationYear
        WHERE d.BeeState = '{state}'
        ORDER BY m.Year
    """
    years, temperatures = fetch_temperature(connection, sample_query)
    assert(type(years[0]) == int)
    assert(isinstance(temperatures[0], decimal.Decimal))


def test_plot_1_render():
    """
    test plot_1_render()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    query_parasite = f"""
        SELECT Year, PercentAffected
        FROM Parasite
        WHERE State = '{state}'
        ORDER BY Year
    """
    years_parasite, percentage_parasite = fetch_parasite(connection, query_parasite)
    query_percentage_diseaselost = f"""
        SELECT Year, PercentLostByDisease
        FROM Bee
        WHERE State = '{state}'
        ORDER BY Year
    """
    years_lost, percentage_lost_by_disease = fetch_percentage_diseaselost(connection, query_percentage_diseaselost)

    graph = plot_1_render(state, years_parasite, years_lost, percentage_parasite, percentage_lost_by_disease)

    assert(graph.encoding.x.shorthand == "year:O")
    assert(graph.encoding.y.shorthand == "percentage:Q")
    assert(graph.encoding.color.shorthand == "type:N")
    assert(graph.encoding.tooltip[0].shorthand == "year")
    assert(graph.encoding.tooltip[1].shorthand == "percentage")


def test_plot_2_render():
    """
    test plot_2_render()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    query_colony_tracker = f"""
        SELECT Year, Colony, LostColony, AddColony
        FROM Bee
        WHERE State = '{state}'
        ORDER BY Year
    """
    colony_years, colony_values, lost_colonies, added_colonies = fetch_colony_tracker(connection, query_colony_tracker)

    graph = plot_2_render(state, colony_years, colony_values, lost_colonies, added_colonies)

    assert(graph.encoding.x.shorthand == "year:O")
    assert(graph.encoding.y.shorthand == "number:Q")
    assert(graph.encoding.color.shorthand == "type:N")
    assert(graph.encoding.tooltip[0].shorthand == "year")
    assert(graph.encoding.tooltip[1].shorthand == "number")


def test_plot_3_render():
    """
    test plot_3_render()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    query_pesticide_usage = f"""
        SELECT Year, LowEstimate, HighEstimate
        FROM Pesticide
        WHERE State = '{state}'
        ORDER BY Year
    """
    years, low_estimate, high_estimate = fetch_pesticide_usage(connection, query_pesticide_usage)

    graph = plot_3_render(state, years, low_estimate, high_estimate)

    assert(graph.encoding.x.shorthand == "year:O")
    assert(graph.encoding.y.shorthand == "number:Q")
    assert(graph.encoding.color.shorthand == "type:N")
    assert(graph.encoding.tooltip[0].shorthand == "year")
    assert(graph.encoding.tooltip[1].shorthand == "number")


def test_plot_4_render():
    """
    test plot_4_render()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    query_aqi = f"""
        SELECT Year, Name, AverageAQI
        FROM GasConditions
        WHERE State = '{state}'
        ORDER BY Year
    """
    gas_data, aqi_data = fetch_aqi(connection, query_aqi)

    graph = plot_4_render(state, aqi_data)

    assert(graph.encoding.x.shorthand == "year:O")
    assert(graph.encoding.y.shorthand == "value:Q")
    assert(graph.encoding.color.shorthand == "type:N")
    assert(graph.encoding.tooltip[0].shorthand == "year")
    assert(graph.encoding.tooltip[1].shorthand == "value")


def test_plot_5_render():
    """
    test plot_5_render()
    """
    connection = connect_to_db(3307, 'localhost')
    load_sql_to_db(connection, "scripts/output.sql")
    states = top_ten_states(connection)
    state = states[0]
    query_temperature = f"""
        SELECT m.Year, m.AverageTemperature
        FROM MonitorStation m
        JOIN Detect d ON m.CentroidLongitude = d.CentroidLongitude 
                        AND m.CentroidLatitude = d.CentroidLatitude
                        AND m.Year = d.StationYear
        WHERE d.BeeState = '{state}'
        ORDER BY m.Year
    """
    years, temperatures = fetch_temperature(connection, query_temperature)
    graph = plot_5_render(state, years, temperatures)

    assert(graph.encoding.x.shorthand == "year:O")
    assert(graph.encoding.y.shorthand == "temperatures:Q")
    assert(graph.encoding.tooltip[0].shorthand == "year")
    assert(graph.encoding.tooltip[1].shorthand == "temperatures")


def test_concat_plots():
    """
    test concat_plots()
    """
    for i in range(1,11):
        x_values = np.random.randint(0, 100, 10)
        y_values = np.random.randint(0, 100, 10)
        dict = {"X" + str(i):x_values,
                "Y" + str(i):y_values}
        data = pd.DataFrame(dict)
        globals()["plot_" + str(i) ] = alt.Chart(data).mark_point().encode(
            x = "X" + str(i) + ":Q",
            y = "Y" + str(i) + ":Q"
        )
    
    graph = concat_plots(plot_1, plot_2, plot_3, plot_4, plot_5, plot_6, plot_7, plot_8, plot_9, plot_10, "images/test_concat.png")

    assert(graph.to_dict()["vconcat"][0]["hconcat"][0]["encoding"]["x"]["field"] == "X1")
    assert(graph.to_dict()["vconcat"][0]["hconcat"][-1]["encoding"]["x"]["field"] == "X5")
    assert(graph.to_dict()["vconcat"][1]["hconcat"][0]["encoding"]["x"]["field"] == "X6")
    assert(graph.to_dict()["vconcat"][1]["hconcat"][-1]["encoding"]["x"]["field"] == "X10")

    os.remove("images/test_concat.png")

def test_query_transform_dataframe():
    """
    test query_transform_dataframe()
    """
    connection = connect_to_db(3307, 'localhost')
    sample_query = """
        SELECT *
        FROM GasConditions 
    """
    sample_columns = ['GasName', 'State', 'Year', 'MeanValue', 'AverageAQI']
    df = query_transform_dataframe(connection, sample_query, sample_columns)
    assert(len(list(df.columns)) == 5)


def test_combined_dataframe():
    """
    test combined_dataframe()
    """
    connection = connect_to_db(3307, 'localhost')

    query_monitor = """
        SELECT *
        FROM Monitor
    """
    columns_monitor = ['CentroidLongitude', 'CentroidLatitude', 'StationYear', 'RiskFactorsReportedYear', 'RiskFactorsReportedState']
    monitor_df = query_transform_dataframe(connection, query_monitor, columns_monitor)

    query_monitor_station = """
        SELECT *
        FROM MonitorStation
    """
    columns_monitor_station = ['CentroidLongitude', 'CentroidLatitude', 'Year', 'AverageTemperature']
    monitor_station_df = query_transform_dataframe(connection, query_monitor_station, columns_monitor_station)

    df = combined_dataframe(monitor_station_df, monitor_df)

    #the number of columns of the combined dataframe should be the sum of the two given dataframes(monitor_df, monitor_station_df) subtract 2 (the duplicated columns ('CentroidLongitude', 'CentroidLatitude'))
    assert(len(list(df.columns)) == len(monitor_df.columns) + len(monitor_station_df.columns)) - 2

    columns = ['CentroidLongitude', 'CentroidLatitude', 'Year', 'AverageTemperature', 'StationYear', 'RiskFactorsReportedYear', 'RiskFactorsReportedState']
    assert(list(df.columns) == columns)


def test_temp_dataframe():
    """
    test temp_dataframe()
    """
    connection = connect_to_db(3307, 'localhost')
    query_monitor = """
        SELECT *
        FROM Monitor
    """
    columns_monitor = ['CentroidLongitude', 'CentroidLatitude', 'StationYear', 'RiskFactorsReportedYear', 'RiskFactorsReportedState']
    monitor_df = query_transform_dataframe(connection, query_monitor, columns_monitor)

    query_monitor_station = """
        SELECT *
        FROM MonitorStation
    """
    columns_monitor_station = ['CentroidLongitude', 'CentroidLatitude', 'Year', 'AverageTemperature']
    monitor_station_df = query_transform_dataframe(connection, query_monitor_station, columns_monitor_station)

    df = combined_dataframe(monitor_station_df, monitor_df)

    temp_df = temp_dataframe(df)

    columns = ['State', 'Year', 'AverageTemperature']
    assert(list(temp_df.columns) == columns)


def help_query():
    """
    query all the dataframes that are needed to generate the final dataframe 
    """
    connection = connect_to_db(3307, 'localhost')

    query_gas_conditions = """
        SELECT *
        FROM GasConditions 
    """
    gas_conditions_df_columns = ['GasName', 'State', 'Year', 'MeanValue', 'AverageAQI']
    gas_conditions_df = query_transform_dataframe(connection, query_gas_conditions, gas_conditions_df_columns)

    query_bee = """
        SELECT * 
        FROM Bee
    """
    columns_bee = ['State', 'Year', 'Colony', 'MaxColony', 'LostColony', 'PercentLost', 'AddColony', 'PercentRenovated', 'PercentLostByDisease']
    bee_df = query_transform_dataframe(connection, query_bee, columns_bee)

    query_monitor = """
        SELECT *
        FROM Monitor
    """
    columns_monitor = ['CentroidLongitude', 'CentroidLatitude', 'StationYear', 'RiskFactorsReportedYear', 'RiskFactorsReportedState']
    monitor_df = query_transform_dataframe(connection, query_monitor, columns_monitor)

    query_monitor_station = """
        SELECT *
        FROM MonitorStation
    """
    columns_monitor_station = ['CentroidLongitude', 'CentroidLatitude', 'Year', 'AverageTemperature']
    monitor_station_df = query_transform_dataframe(connection, query_monitor_station, columns_monitor_station)

    query_pesticide = """
        SELECT *
        FROM Pesticide
    """
    columns_pesticide = ['Year', 'State', 'LowEstimate', 'HighEstimate']
    pesticide_df = query_transform_dataframe(connection, query_pesticide, columns_pesticide)

    combined_df = combined_dataframe(monitor_station_df, monitor_df)
    temp_df = temp_dataframe(combined_df)

    return temp_df, pesticide_df, gas_conditions_df, bee_df

def test_final_dataframe():
    """
    test final_dataframe()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()

    final_df = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)
    assert(len(list(final_df.columns)) == 9)

    columns = ['State', 'Year', 'AverageTemperature', 'PercentLost', 'PercentLostByDisease', 'CO_conc', 'NO2_conc', 'SO2_conc', 'PesticideEstimate']
    assert(list(final_df.columns) == columns)


def test_check_linearity():
    """
    test check_linearity()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()
    
    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    sample_plt = check_linearity(data, 'AverageTemperature', 'images/average_temperature_linearity.png')
    assert(sample_plt.figure.get_size_inches()[0] == 10)
    assert(sample_plt.figure.get_size_inches()[1] == 6)
    #assert(sample_plt.figure._suptitle._text == "Relationship between AverageTemperature and PercentLost")


def test_check_vif():
    """
    test check_vif()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()

    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    vif_data = check_vif(data)
    assert(len(list(vif_data.columns)) == 2)
    assert(list(vif_data.columns)[0] == 'Variable')
    assert(list(vif_data.columns)[1] == 'VIF')


def test_correlation():
    """
    test correlation()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()

    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    graph = correlation(data, 'images/correlation_matrix.png')
    assert(graph.figure.get_size_inches()[0] == 10)
    assert(graph.figure.get_size_inches()[1] == 6)


def test_linear_model():
    """
    test linear_model()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()

    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    X, y, model = linear_model(data, "models/linear_model.pkl")
    assert(len(list(X.columns)) == 9)
    assert(y[0].dtype == np.float64)
    assert(isinstance(model, RegressionResultsWrapper))


def test_non_linear_model():
    """
    test non_linear_model()
    """
    temp_df, pesticide_df, gas_conditions_df, bee_df = help_query()

    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    X, y, model = linear_model(data, "models/linear_model.pkl")

    xgb_model = non_linear_model(X, y, "images/shap_train.png", "images/shap_overall.png")

    assert(isinstance(xgb_model, xgb.XGBRegressor))










