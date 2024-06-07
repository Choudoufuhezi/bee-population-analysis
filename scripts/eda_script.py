import altair as alt
import pandas as pd
import click
import re
import sys
import os
alt.renderers.enable('mimetype')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.eda import * 
from src.to_ddl import * 

@click.command()
@click.option('--year_lost_path', type = str, default = "images/year_lost.png")
@click.option('--year_temperature_path', type = str, default = "images/year_temperature.png")
@click.option('--year_pesticide_path', type = str, default = "images/year_pesticide.png")
@click.option('--year_aqi_path', type = str, default = "images/year_aqi.png")
@click.option('--state_bee_loss_path', type = str, default = "images/state_bee_loss.png")
@click.option('--loss_disease_parasite_path', type = str, default = "images/loss_disease_parasite.png")
@click.option('--population_change_path', type = str, default = "images/population_change.png")
@click.option('--temp_change_path', type = str, default = "images/temp_change.png")
def main(year_lost_path, year_temperature_path, year_pesticide_path, year_aqi_path, state_bee_loss_path, loss_disease_parasite_path, population_change_path, temp_change_path):
    connection = connect_to_db(3306, 'cpsc368-project-group1-init_db-1')

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

    concat_plots(Illinois_plot_1, Massachusetts_plot_1, Kansas_plot_1, Georgia_plot_1, loss_disease_parasite_path)
    concat_plots(Utah_plot_2, Massachusetts_plot_2, North_Dakota_plot_2, Georgia_plot_2, population_change_path)
    concat_plots(Utah_plot_5, Illinois_plot_5, North_Dakota_plot_5, Kansas_plot_5, temp_change_path)


if __name__ == "__main__":
    main()
