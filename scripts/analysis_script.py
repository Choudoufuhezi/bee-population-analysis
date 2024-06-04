import altair as alt
import pandas as pd
import click
import re
import sys
import os
alt.renderers.enable('mimetype')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.analysis import *

@click.command()
@click.option('--year_lost_path', type = str, default = "images/year_lost.png")
@click.option('--year_temperature_path', type = str, default = "images/year_temperature.png")
@click.option('--year_pesticide_path', type = str, default = "images/year_pesticide.png")
@click.option('--year_aqi_path', type = str, default = "images/year_aqi.png")
@click.option('--state_bee_loss_path', type = str, default = "images/state_bee_loss.png")
@click.option('--plot_1_path', type = str, default = "images/plot1.png")
@click.option('--plot_2_path', type = str, default = "images/plot2.png")
@click.option('--plot_3_path', type = str, default = "images/plot3.png")
@click.option('--plot_4_path', type = str, default = "images/plot4.png")
@click.option('--plot_5_path', type = str, default = "images/plot5.png")
@click.option('--average_temperature_path', type = str, default = "images/average_temperature_linearity.png")
@click.option('--co_conc_path', type = str, default = "images/co_conc_linearity.png")
@click.option('--no2_conc_path', type = str, default = "images/no2_conc_linearity.png")
@click.option('--so2_conc_path', type = str, default = "images/so2_conc_linearity.png")
@click.option('--percent_lost_by_disease_path', type = str, default = "images/percent_lost_by_disease_linearity.png")
@click.option('--pesticide_estimate_path', type = str, default = "images/pesticide_estimate_linearity.png")
@click.option('--correlation_path', type = str, default = "images/correlation_matrix.png")
@click.option('--linear_model_path', type = str, default = "models/linear_model.pkl")
@click.option('--shap_train_path', type = str, default = "images/shap_train.png")
@click.option('--shap_overall_path', type = str, default = "images/shap_overall.png")
@click.option('--vif_path', type = str, default = "data/processed/vif.csv")
@click.option('--sql_file_path', type = str, default = "scripts/output.sql")
def main(year_lost_path, year_temperature_path, year_pesticide_path, year_aqi_path, state_bee_loss_path, plot_1_path, plot_2_path, plot_3_path, plot_4_path, plot_5_path, average_temperature_path, co_conc_path, no2_conc_path, so2_conc_path, percent_lost_by_disease_path, pesticide_estimate_path, correlation_path, linear_model_path, shap_train_path, shap_overall_path, vif_path, sql_file_path):
    connection = connect_to_db(3306, 'cpsc368-project-group1-init_db-1')

    load_sql_to_db(connection, sql_file_path)

    year_percentage_lost(connection, year_lost_path)
    year_temperature(connection, year_temperature_path)
    year_pesticide(connection, year_pesticide_path)
    year_AQI(connection, year_aqi_path)
    top_ten_states_bee_loss(connection, state_bee_loss_path)

    ten_states = top_ten_states(connection)

    for state in ten_states:
        query_percentage_diseaselost = f"""
            SELECT Year, PercentLostByDisease
            FROM Bee
            WHERE State = '{state}'
            ORDER BY Year
        """
        years_lost, percentage_lost_by_disease = fetch_percentage_diseaselost(connection, query_percentage_diseaselost)

        query_parasite = f"""
            SELECT Year, PercentAffected
            FROM Parasite
            WHERE State = '{state}'
            ORDER BY Year
        """
        years_parasite, percentage_parasite = fetch_parasite(connection, query_parasite)

        query_colony_tracker = f"""
            SELECT Year, Colony, LostColony, AddColony
            FROM Bee
            WHERE State = '{state}'
            ORDER BY Year
        """
        colony_years, colony_values, lost_colonies, added_colonies = fetch_colony_tracker(connection, query_colony_tracker)

        query_pesticide_usage = f"""
            SELECT Year, LowEstimate, HighEstimate
            FROM Pesticide
            WHERE State = '{state}'
            ORDER BY Year
        """
        years, low_estimate, high_estimate = fetch_pesticide_usage(connection, query_pesticide_usage)

        query_aqi = f"""
            SELECT Year, Name, AverageAQI
            FROM GasConditions
            WHERE State = '{state}'
            ORDER BY Year
        """
        gas_data, aqi_data = fetch_aqi(connection, query_aqi)

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

        globals()[re.sub(r'[^a-zA-Z0-9]', '_', str(state)) + "_plot_1"] = plot_1_render(state, years_parasite, years_lost, percentage_parasite, percentage_lost_by_disease)
        globals()[re.sub(r'[^a-zA-Z0-9]', '_', str(state)) + "_plot_2"] = plot_2_render(state, colony_years, colony_values, lost_colonies, added_colonies)
        globals()[re.sub(r'[^a-zA-Z0-9]', '_', str(state)) + "_plot_3"] = plot_3_render(state, years, low_estimate, high_estimate)
        globals()[re.sub(r'[^a-zA-Z0-9]', '_', str(state)) + "_plot_4"] = plot_4_render(state, aqi_data)
        globals()[re.sub(r'[^a-zA-Z0-9]', '_', str(state)) + "_plot_5"] = plot_5_render(state, years, temperatures)

    concat_plots(Utah_plot_1, Washington_plot_1, Illinois_plot_1, Massachusetts_plot_1, Virginia_plot_1, North_Dakota_plot_1, New_Jersey_plot_1, Kansas_plot_1, Georgia_plot_1, Texas_plot_1, plot_1_path)
    concat_plots(Utah_plot_2, Washington_plot_2, Illinois_plot_2, Massachusetts_plot_2, Virginia_plot_2, North_Dakota_plot_2, New_Jersey_plot_2, Kansas_plot_2, Georgia_plot_2, Texas_plot_2, plot_2_path)
    concat_plots(Utah_plot_3, Washington_plot_3, Illinois_plot_3, Massachusetts_plot_3, Virginia_plot_3, North_Dakota_plot_3, New_Jersey_plot_3, Kansas_plot_3, Georgia_plot_3, Texas_plot_3, plot_3_path)
    concat_plots(Utah_plot_4, Washington_plot_4, Illinois_plot_4, Massachusetts_plot_4, Virginia_plot_4, North_Dakota_plot_4, New_Jersey_plot_4, Kansas_plot_4, Georgia_plot_4, Texas_plot_4, plot_4_path)
    concat_plots(Utah_plot_5, Washington_plot_5, Illinois_plot_5, Massachusetts_plot_5, Virginia_plot_5, North_Dakota_plot_5, New_Jersey_plot_5, Kansas_plot_5, Georgia_plot_5, Texas_plot_5, plot_5_path)
   
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

    data = final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df)

    data["AverageTemperature"] = data["AverageTemperature"].astype(float)
    data["CO_conc"] = data["CO_conc"].astype(float)
    data["NO2_conc"] = data["NO2_conc"].astype(float)
    data["SO2_conc"] = data["SO2_conc"].astype(float)
    data["PercentLostByDisease"] = data["PercentLostByDisease"].astype(float)
    data["PesticideEstimate"] = data["PesticideEstimate"].astype(float)
    data["PercentLost"] = data["PercentLost"].astype(float)

    check_linearity(data, 'AverageTemperature', average_temperature_path)
    check_linearity(data, 'CO_conc', co_conc_path)
    check_linearity(data, 'NO2_conc', no2_conc_path)
    check_linearity(data, 'SO2_conc', so2_conc_path)
    check_linearity(data, 'PercentLostByDisease', percent_lost_by_disease_path)
    check_linearity(data, 'PesticideEstimate', pesticide_estimate_path)

    vif_data = check_vif(data)
    vif_data.to_csv(vif_path)

    correlation(data, correlation_path)

    X, y, model = linear_model(data, linear_model_path)
    
    non_linear_model(X, y, shap_train_path, shap_overall_path)


if __name__ == "__main__":
    main()




