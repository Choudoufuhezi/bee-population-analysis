import click
from pybeepop.to_ddl import connect_to_db
from pybeepop.analysis import *

@click.command()
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
def main(average_temperature_path, co_conc_path, no2_conc_path, so2_conc_path, percent_lost_by_disease_path, pesticide_estimate_path, correlation_path, linear_model_path, shap_train_path, shap_overall_path, vif_path):
    connection = connect_to_db(3306, 'cpsc368-project-group1-init_db-1')

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




