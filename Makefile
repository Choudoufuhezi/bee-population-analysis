data/processed/average_monthly_temperature_by_state_1950-2022.csv data/processed/epest_county_estimates.csv data/processed/save_the_bees.csv data/processed/pollution_2000_2021.csv data/processed/helper.csv:
		python scripts/clean_data_script.py

scripts/output.sql:
		python scripts/to_ddl_script.py

clean:
		rm -rf data/processed/average_monthly_temperature_by_state_1950-2022.csv
		rm -rf data/processed/epest_county_estimates.csv
		rm -rf data/processed/save_the_bees.csv
		rm -rf data/processed/pollution_2000_2021.csv 
		rm -rf data/processed/helper.csv
		rm -rf scripts/output.sql


all: data/processed/average_monthly_temperature_by_state_1950-2022.csv \
		data/processed/epest_county_estimates.csv \
		data/processed/save_the_bees.csv \
		data/processed/pollution_2000_2021.csv \
		data/processed/helper.csv \
		scripts/output.sql
