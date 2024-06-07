import sys
import os
import click
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.to_ddl import *

@click.command()
@click.option('--sql_path', type = str, default = "scripts/output.sql")
@click.option('--temperature_data_path', type = str, default = "data/processed/average_monthly_temperature_by_state_1950-2022.csv")
@click.option('--bee_data_path', type = str, default = "data/processed/save_the_bees.csv")
@click.option('--pollution_data_path', type = str, default = "data/processed/pollution_2000_2021.csv")
@click.option('--helper_data_path', type = str, default = "data/processed/helper.csv")
@click.option('--epest_data_path', type = str, default = "data/processed/epest_county_estimates.csv")

def main(sql_path, temperature_data_path, bee_data_path, pollution_data_path, helper_data_path, epest_data_path):
    init_tables(sql_path)
    create_sql_MonitorStation(temperature_data_path, sql_path)
    create_sql_Bee(bee_data_path, sql_path)
    create_sql_detect(temperature_data_path, bee_data_path, sql_path)
    create_sql_GasConditions(pollution_data_path, sql_path)
    create_sql_Influence(pollution_data_path, bee_data_path, sql_path)
    create_sql_RiskFactors(helper_data_path, sql_path)
    create_sql_Monitor(temperature_data_path, helper_data_path, sql_path)
    create_sql_Kill(bee_data_path, pollution_data_path, sql_path)
    create_sql_Parasite(bee_data_path, sql_path)
    create_sql_Pesticide(epest_data_path, sql_path)

    connection = connect_to_db(3306, 'cpsc368-project-group1-init_db-1')
    load_sql_to_db(connection, sql_path)


if __name__ == '__main__':
    main()




