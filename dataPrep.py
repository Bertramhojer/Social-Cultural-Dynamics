import pandas as pd
import numpy as np

data = pd.read_csv("pitchScores.csv", sep = ",")

iqr = data[["pitchVariability"]]
mad = data[["pitchMAD"]]
pause = data[["pauseFreq"]]
speechrate = data[["speechRate"]]
