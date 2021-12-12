# Mathematical Modelling in Physiology and Medicine 2021 Coursework

This repository contains the Python code to reproduce all the figures in the coursework for [EMATM0007: Mathematical Modelling in Physiology and Medicine](https://www.bris.ac.uk/unit-programme-catalogue/UnitDetails.jsa;jsessionid=557B7CD21C5BEDD4093DA92C0DA5C5F4?ayrCode=31%2F32&unitCode=EMATM0007). Each python file may be run individually to obtain the plot - there are no dependencies on any other python file.

In this work, we conduct a model comparison and analysis on the paper [Minimal model for signal-induced Ca2+ oscillations and for their frequency encoding through protein phosphorylation](https://www.pnas.org/content/pnas/87/4/1461.full.pdf). We introduce the biological model in terms of a system of ODEs and compare model approaches to ones found in the literature. We conduct show how the system dynamics change in time for various parameter sets. We give a phase plane analysis to qualitatively determine features in the non-linear system. We end by conducting a bifurcation analysis on the system of ODEs. 

## Requirements
- Python 3.8
- Install python external modules using `pip install -r requirements.txt` after activating virtualenv.

## Notes
Reproduction of figure 6 may be done using the corresponding code but requires parallelisation and the use of multiple cores. For ease of reproduction, we recommend downloading 'max_values_list_Z.pkl' and 'vm3_value_list.pkl' and instead running 'figure_6_after_parallel.py'.
