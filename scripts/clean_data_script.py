import pandas as pd
import numpy as np
import us
import os
import click
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import *

@click.command()
@click.option('--data1_path_origin',  type=str, default='data/original/average_monthly_temperature_by_state_1950-2022.parquet')
@click.option('--data2_path_origin',  type=str, default='data/original/epest_county_estimates.parquet')
@click.option('--data3_path_origin',  type=str, default='data/original/save_the_bees.parquet')
@click.option('--data4_path_origin',  type=str, default='data/original/pollution_2000_2021.parquet')
@click.option('--data1_path_processed',  type=str, default='data/processed/average_monthly_temperature_by_state_1950-2022.csv')
@click.option('--data2_path_processed',  type=str, default='data/processed/epest_county_estimates.csv')
@click.option('--data3_path_processed',  type=str, default='data/processed/save_the_bees.csv')
@click.option('--data4_path_processed',  type=str, default='data/processed/pollution_2000_2021.csv')
@click.option('--data_help_2_path',  type=str, default='data/processed/helper.csv')
@click.option('--data_help_path',  type=str, default='data/processed/helper__.csv')

def main(data1_path_origin, data2_path_origin, data3_path_origin, data4_path_origin, data1_path_processed, data2_path_processed, data3_path_processed, data4_path_processed, data_help_2_path, data_help_path):

    data1, data2, data3, data4 = read_data(data1_path_origin, data2_path_origin, data3_path_origin, data4_path_origin)

    data1 = clean_data1(data1)
    data2 = clean_data2(data2)
    helper = helper_dataset(data3)
    data3 = clean_data3(data3, helper)
    data3 = clean_data3(data3, helper)
    data_help_2 = helper_dataset2(data2, data3)
    data4 = clean_data4(data4)

    data1.to_csv(data1_path_processed)
    data2.to_csv(data2_path_processed)
    data3.to_csv(data3_path_processed)
    data4.to_csv(data4_path_processed)
    data_help_2.to_csv(data_help_2_path)
    helper.to_csv(data_help_path)


if __name__ == '__main__':
    main()