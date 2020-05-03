# Social-Cultural-Dynamics
Repository of python code for running ABM-simulation and analysing social interaction

This repository contains 5 different scripts;
* dataPrep.py

* mainABM.py
* rulebook.py
* runBatch.py

* server.py

# Contents
Each script has a different use-case;

'dataPrep.py' is very short and quite simply used to load the pitch-scores from a csv and creating a 1-D pandas dataframe for each measure.

'mainABM.py' is the main-script that contains the model class. It specifies an Agent-class object and a Model-class object containing agent as well as model-rules for progressing the model through each iterative time-step. It is within this script that all agent-level and model-level variables are specified.

'rulebook.py' contains all rule-based interactions that is performed by agents through each iteration if they are interacting with another agent.

'runBatch.py' allows the user to run multiple iterations of the model and save the final data-output for each iteration rather than to run single instantiations of the model multiple times. One can potentially add varying parameters, but varying parameters aren't used for this model since the agent-pool is static.

'server.py' is a visualization tool that opens a local-host illustrating the grid on which agent's a placed and showcases how agents interact as well as keep track of a variety of variables such as overall encounters and the unique measures of each individual agent.