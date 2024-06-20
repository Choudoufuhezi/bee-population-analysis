# Bee Population Analysis
**Project title**: Assessing the Influence of Pesticide Usage, Parasitic Factors, and Climate on Honey Bee Populations in the United States (2015-2019)

Contributors:

- Hanxi Chen
- Tianyu Duan
- Hanlin Zhao

## Project Summary

Analyzing the Impact of Pesticide Usage, Parasitic Factors, and Climate on Honey Bee Populations in the United States (2015-2019) using Data Visualizations, Pre-Processing ETL (extract, transform, and load) with MySQL, OLS Regression, and XGBoost Models.

## Dependencies

The project is currently being managed using [Docker](https://www.docker.com/), a virtual container platform. It involves two images: `bee_population_analysis`, built on the base image of `jupyter/scipy-notebook`, and the `mysql` Docker image.

## Instructions

1. Make sure you have installed and correctly set up [Docker](https://www.docker.com/) on your device. If not, please install it.
   
2. Please clone the repository by copying and pasting the following command into your terminal:
   
   `git clone https://github.com/Choudoufuhezi/bee_population_analysis.git`
  
3. Switch to the project directory by entering the following command into your terminal :

   `cd bee_population_analysis`

4. Before conducting the analysis, ensure the file is cleaned and prepared appropriately  :

   `docker-compose run clean_analysis`

5. run the analysis :

   `docker-compose run run_analysis`

## Licenses

`bee_population_analysis` was created by Hanxi Chen, Tianyu Duan, Hanlin Zhao. It is licensed under the terms of the MIT license.

## Dataset 

In crafting our analytical framework, we have chosen four datasets to reveal the complex interplay between various factors influencing honey bee populations and agricultural ecosystems. Firstly, we draw upon the [Pesticide Usage Data](https://www.kaggle.com/datasets/konradb/pesticide-usage-in-the-united-states/data), acquired from the National Water-Quality Assessment Project, offering insights into pesticide application trends across different states. 

Complementing this, the [Honey Bee Health Data](https://www.kaggle.com/datasets/m000sey/save-the-honey-bees/data), spanning from 2015 to 2022 and originally collected by the USDA, furnishes critical information on honey bee populations, facilitating a nuanced understanding of their health dynamics. Furthermore, [NOAA's Climate Data](https://www.kaggle.com/datasets/justinrwong/average-monthly-temperature-by-us-state), providing temperature insights by U.S. state, adds a crucial dimension to our analysis by elucidating the impact of climatic variations on honey bee behavior and pesticide usage patterns. 

Lastly, the [US Pollution Data (2000-2023)](https://www.kaggle.com/datasets/guslovesmath/us-pollution-data-200-to-2022), sourced from the U.S. Environmental Protection Agency, serves as a comprehensive resource for assessing air quality and pollution levels, aiding in delineating the environmental stressors influencing honey bee health. Each dataset was selected after careful consideration of factors such as reliability, relevance to our research objectives, and accessibility, aiming to provide a robust foundation for our investigation into sustainable agricultural practices and biodiversity conservation efforts.

