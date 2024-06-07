import sys
import os
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.to_ddl import * 


def test_init_tables():
    """
    test the initialization fo the tables
    """
    assert(init_tables("scripts/output.sql"), True)


def test_MonitorStation():
    """
    test the create MonitorStation table function
    """
    assert(create_sql_MonitorStation("data/processed/average_monthly_temperature_by_state_1950-2022.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_MonitorStation("data/processed/average_monthly_temperature_by_state_1950-2021.csv", "scripts/output.sql"), False)


def test_Bee():
    """
    test the create bee table function
    """
    assert(create_sql_Bee("data/processed/save_the_bees.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_Bee("data/processed/save_the_bee.csv", "scripts/output.sql"), False)


def test_detect():
    """
    test the create detect table function
    """
    assert(create_sql_detect("data/processed/average_monthly_temperature_by_state_1950-2022.csv", "data/processed/save_the_bees.csv", "scripts/output.sql"), True)

    #first input path do not exist
    assert(create_sql_detect("data/processed/average_monthly_temperature_by_state_1950-2021.csv", "data/processed/save_the_bees.csv", "scripts/output.sql"), False)

    #second input path do not exist
    assert(create_sql_detect("data/processed/average_monthly_temperature_by_state_1950-2022.csv", "data/processed/save_the_bee.csv", "scripts/output.sql"), False)

    #both input pathes do not exist 
    assert(create_sql_detect("data/processed/average_monthly_temperature_by_state_1950-2021.csv", "data/processed/save_the_bee.csv", "scripts/output.sql"), False)


def test_GasConditions():
    """
    test the create GasConditions table function
    """
    assert(create_sql_GasConditions("data/processed/pollution_2000_2021.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_GasConditions("data/processed/pollution_2000_2022.csv", "scripts/output.sql"), False)


def test_Influence():
    """
    test the create Influence table function
    """
    assert(create_sql_Influence("data/processed/pollution_2000_2021.csv", "data/processed/save_the_bees.csv", "scripts/output.sql"), True)

    #first input path do not exist
    assert(create_sql_Influence("data/processed/pollution_2000_2022.csv", "data/processed/save_the_bees.csv", "scripts/output.sql"), False)

    #second input path do not exist
    assert(create_sql_Influence("data/processed/pollution_2000_2021.csv", "data/processed/save_the_bee.csv", "scripts/output.sql"), False)

    #both input pathes do not exist 
    assert(create_sql_Influence("data/processed/pollution_2000_2022.csv", "data/processed/save_the_bee.csv", "scripts/output.sql"), False)


def test_RiskFactors():
    """
    test the create RiskFactors table function
    """
    assert(create_sql_RiskFactors("data/processed/helper.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_RiskFactors("data/processed/helper1.csv", "scripts/output.sql"), False)


def test_Monitor():
    """
    test the create Monitor table function
    """
    assert(create_sql_Monitor("data/processed/average_monthly_temperature_by_state_1950-2022.csv","data/processed/helper.csv", "scripts/output.sql"), True)

    #first input path do not exist
    assert(create_sql_Monitor("data/processed/average_monthly_temperature_by_state_1950-2021.csv","data/processed/helper.csv", "scripts/output.sql"), False)

    #second input path do not exist
    assert(create_sql_Monitor("data/processed/average_monthly_temperature_by_state_1950-2022.csv","data/processed/helper1.csv", "scripts/output.sql"), False)

    #both input pathes do not exist 
    assert(create_sql_Monitor("data/processed/average_monthly_temperature_by_state_1950-2021.csv","data/processed/helper1.csv", "scripts/output.sql"), False)


def test_Kill():
    """
    test the create Kill table function
    """
    assert(create_sql_Kill("data/processed/save_the_bees.csv","data/processed/pollution_2000_2021.csv", "scripts/output.sql"), True)

    #first input path do not exist
    assert(create_sql_Kill("data/processed/save_the_bee.csv","data/processed/pollution_2000_2021.csv", "scripts/output.sql"), False)

    #second input path do not exist
    assert(create_sql_Kill("data/processed/save_the_bees.csv","data/processed/pollution_2000_2020.csv", "scripts/output.sql"), False)

    #both input pathes do not exist 
    assert(create_sql_Kill("data/processed/save_the_bee.csv","data/processed/pollution_2000_2020.csv", "scripts/output.sql"), False)


def test_Parasite():
    """
    test the create Parasite table function
    """
    assert(create_sql_Parasite("data/processed/save_the_bees.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_Parasite("data/processed/save_the_bee.csv", "scripts/output.sql"), False)


def test_Pesticide():
    """
    test the create Pesticide table function
    """
    assert(create_sql_Pesticide("data/processed/epest_county_estimates.csv", "scripts/output.sql"), True)

    #input path that do not exist
    assert(create_sql_Pesticide("data/processed/epest_county_estimate.csv", "scripts/output.sql"), False)


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
    init_tables("scripts/output.sql")
    connection = connect_to_db(3307, 'localhost')
    assert(load_sql_to_db(connection, "scripts/output.sql"), True)
    assert(load_sql_to_db(connection, "scripts/output1.sql"), False)
