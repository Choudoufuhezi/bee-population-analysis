data/processed/average_monthly_temperature_by_state_1950-2022.csv data/processed/epest_county_estimates.csv data/processed/save_the_bees.csv data/processed/pollution_2000_2021.csv data/processed/helper.csv data/processed/helper__.csv:
		python scripts/clean_data_script.py

scripts/output.sql:
		python scripts/to_ddl_script.py

images/year_percentage_lost.png images/year_temperature.png images/year_pesticide.png images/year_aqi.png images/plot1.png images/plot2.png images/plot3.png images/plot4.png images/plot5.png:
		python scripts/analysis_script.py

images/average_temperature_linearity.png images/co_conc_linearity.png images/no2_conc_linearity.png images/so2_conc_linearity.png images/percent_lost_by_disease_linearity.png images/pesticide_estimate_linearity.png:
		python scripts/analysis_script.py

images/correlation_matrix.png models/linear_model.pkl images/shap_train.png images/shap_overall.png data/processed/vif.csv:
		python scripts/analysis_script.py

docs/index.html:
		quarto render 

clean:
		rm -rf scripts/output.sql
		rm -rf models/linear_model.pkl 
		rm -rf data/processed/vif.csv
		rm -rf images/*
		rm -rf data/processed/*
		rm -rf docs/*
		rm -rf reports/analysis_report_files

all: data/processed/average_monthly_temperature_by_state_1950-2022.csv \
		data/processed/epest_county_estimates.csv \
		data/processed/save_the_bees.csv \
		data/processed/pollution_2000_2021.csv \
		data/processed/helper.csv \
		data/processed/helper.csv data/processed/helper__.csv \
		scripts/output.sql \
		images/year_temperature.png \
		images/year_pesticide.png \
		images/year_aqi.png \
		images/year_percentage_lost.png \
		images/plot1.png \
		images/plot2.png \
		images/plot3.png \
		images/plot4.png \
		images/plot5.png \
		images/average_temperature_linearity.png \
		images/co_conc_linearity.png \
		images/no2_conc_linearity.png \
		images/so2_conc_linearity.png \
		images/percent_lost_by_disease_linearity.png \
		images/pesticide_estimate_linearity.png \
		images/correlation_matrix.png \
		models/linear_model.pkl \
		images/shap_train.png \
		images/shap_overall.png \
		data/processed/vif.csv \
		docs/index.html
