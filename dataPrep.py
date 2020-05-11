import pandas as pd
import numpy as np

data = pd.read_csv("participantScores.csv", sep = ",")

iqr = data[["pitchVariability"]]
mad = data[["pitchMAD"]]
pause = data[["pauseFreq"]]
speechrate = data[["speechRate"]]
diagnosis = data[["Diagnosis"]]
