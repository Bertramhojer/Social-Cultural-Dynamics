## Social-Cultural-Dynamics

![Model Visualisation](visualisation.gif)

# Files
Repository of python code for running ABM-simulation and analysing social interaction

This repository contains 5 different python scripts that handle the simulation in the form of an Agent-Based Model;
* dataPrep.py
* mainABM.py
* rulebook.py
* runBatch.py
* server.py

The repository further comprises 3 R-markdowns handling data-analysis;
* dataPrep.Rmd
* Analysis.Rmd
* Classification.Rmd

## Contents
# Python-files

'dataPrep.py' is very short and quite simply used to load the pitch-scores from a csv and creating a 1-D pandas dataframe for each measure.

'mainABM.py' is the main-script that contains the model class. It specifies an Agent-class object and a Model-class object containing agent as well as model-rules for progressing the model through each iterative time-step. It is within this script that all agent-level and model-level variables are specified.

'rulebook.py' contains all rule-based interactions that is performed by agents through each iteration if they are interacting with another agent.

'runBatch.py' allows the user to run multiple iterations of the model and save the final data-output for each iteration rather than to run single instantiations of the model multiple times. One can potentially add varying parameters, but varying parameters aren't used for this model since the agent-pool is static.

'server.py' is a visualization tool that opens a local-host illustrating the grid on which agent's a placed and showcases how agents interact as well as keep track of a variety of variables such as overall encounters and the unique measures of each individual agent.

# R-files

'dataPrep.Rmd' handles the initial wrangling of the data to make it have the right dimensions for the ABM and to ease the process of loading the data into the ABM.

'Analysis.Rmd' contains code for all a priori bayesian regression analyses made to investigate the original data on acoustic profiles. This includes brms models for prior and posterior distribution as well as hypothesis checks. It furthermore includes post-simulation bayesian analyses of all simulated variables and hypothesis checks that allow investigation into which variables might prove good predictors in a predictive framework. Finally it includes a few interaction models.

'Classification.Rmd' comprises functions that allow you to run a logistic regression and to wrap this logistic regression in a function that cross-validates your model on multiple configurations of your data. It furthermore contains code for plotting the accuracy of the compaired models.