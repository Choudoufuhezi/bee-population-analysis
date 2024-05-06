import pandas as pd
import numpy as np
import us
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import *

def test_read_csvs():
    """
    test the read_csv() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    assert(isinstance(data1, pd.DataFrame))
    assert(isinstance(data2, pd.DataFrame))
    assert(isinstance(data3, pd.DataFrame))
    assert(isinstance(data4, pd.DataFrame))



def test_clean_data1():
    """
    test the clean_data1() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    
    data1 = clean_data1(data1) 
    assert(len(data1) == 175)
    assert(data1.columns[0] == "year")
    assert(data1.columns[1] == "state")
    assert(data1.columns[2] == "average_temp")
    assert(data1.columns[3] == "centroid_lon")
    assert(data1.columns[4] == "centroid_lat")


def test_clean_data2():
    """
    test the clean_data2() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    
    data2 = clean_data2(data2) 
    assert(len(data2) == 875)
    assert(data2.columns[0] == "COMPOUND")
    assert(data2.columns[1] == "YEAR")
    assert(data2.columns[2] == "EPEST_LOW_KG")
    assert(data2.columns[3] == "EPEST_HIGH_KG")
    assert(data2.columns[4] == "STATE")


def test_helper_dataset():
    """
    test the helper_dataset() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    
    helper = helper_dataset(data3) 
    assert(len(helper) == 175)
    assert(helper.columns[0] == "percent_renovated")
    assert(helper.columns[1] == "percent_lost")



def test_clean_data3():
    """
    test the clean_data3() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    helper = helper_dataset(data3) 
    data3 = clean_data3(data3, helper)
    assert(len(data3) == 175)
    assert(data3.columns[0] == "state")
    assert(data3.columns[1] == "year")
    assert(data3.columns[2] == "num_colonies")
    assert(data3.columns[3] == "max_colonies")
    assert(data3.columns[4] == "lost_colonies")
    assert(data3.columns[5] == "percent_lost")
    assert(data3.columns[6] == "added_colonies")
    assert(data3.columns[7] == "renovated_colonies")
    assert(data3.columns[8] == "percent_renovated")
    assert(data3.columns[9] == "varroa_mites")
    assert(data3.columns[10] == "diseases")



def test_helper_dataset2():
    """
    test the helper_dataset2() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    helper = helper_dataset(data3) 
    data2 = clean_data2(data2)
    data3 = clean_data3(data3, helper)
    data_help_2 = helper_dataset2(data2, data3)
    assert(len(data_help_2) == 1050)
    assert(data_help_2.columns[0] == "Name")
    assert(data_help_2.columns[1] == "YEAR")
    assert(data_help_2.columns[2] == "STATE")


def test_clean_data4():
    """
    test the clean_data4() function
    """
    data1, data2, data3, data4 = read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet",
                                        "data/original/epest_county_estimates.parquet", 
                                        "data/original/save_the_bees.parquet",
                                        "data/original/pollution_2000_2021.parquet")
    data4 = clean_data4(data4)
    assert(len(data4) == 700)
    assert(data4.columns[0] == "Year")
    assert(data4.columns[1] == "State")
    assert(data4.columns[2] == "Pollutant")
    assert(data4.columns[3] == "AQI")
    assert(data4.columns[4] == "Mean")













    



    

