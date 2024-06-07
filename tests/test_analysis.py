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
from src.to_ddl import *


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










