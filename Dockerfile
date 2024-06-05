FROM quay.io/jupyter/scipy-notebook:2024-02-24

RUN conda install -y \
    python=3.11.9 \
    numpy=1.26.4 \
    pandas=2.2.2 \
    pytest=8.2.0 \
    us=3.1.1 \
    click=8.1.7 \
    altair=5.2.0 \
    mysql-connector-python=8.3 \ 
    vegafusion=1.6.5 \
    vl-convert-python=1.2.3 \ 
    seaborn=0.13.2 \
    matplotlib=3.8.3 \
    scikit-learn=1.2.0 \
    xgboost=2.0.3 \
    statsmodels=0.14.1 \
    shap=0.45.0 \
    quarto=1.4.550