# import MESA batchrunner module
from mesa.batchrunner import BatchRunner
from mainABM import *

fixed_params = {"width": 16,
				"height": 16,
				"N": 67}

batch_run = BatchRunner(Model,
						fixed_parameters = fixed_params,
						iterations = 1000,
						max_steps = 1000,
						agent_reporters = {"interactions": "unique_interactions",
									"interaction_time": "interaction_time",
									"conversation_time": "conversation_time",
									"change_IQR": "change_iqr",
									"change_MAD": "change_mad",
									"change_Speechrate": "change_speechrate",
									"change_PauseFreq": "change_pause",
									"abs_change_IQR": "abs_change_iqr",
									"abs_change_MAD": "abs_change_mad",
									"abs_change_Speechrate": "abs_change_speechrate",
									"abs_change_PauseFreq": "abs_change_pause",
									"activity": "activity",
									"IQR": "iqr",
									"speechrate": "speechrate",
									"pauseFreq": "pause",
									"mad": "mad",
									"diagnosis": "diagnosis"})



batch_run.run_all()

batch_data = batch_run.get_agent_vars_dataframe()
batch_data.to_csv("batch_1000_1000.csv")