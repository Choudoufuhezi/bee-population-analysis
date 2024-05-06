FROM quay.io/jupyter/scipy-notebook:2024-02-24

RUN conda install -y \
    python=3.11.9 \
    numpy=1.26.4 \
    pandas=2.2.2 \
    pytest=8.2.0 \
    us=3.1.1 