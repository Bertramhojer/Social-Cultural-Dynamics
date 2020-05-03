# import MESA batchrunner module
from mesa.batchrunner import BatchRunner
from mainABM import *

fixed_params = {"width": 16,
				"height": 16,
				"N": 50}

batch_run = BatchRunner(Model,
						fixed_parameters = fixed_params,
						iterations = 10,
						max_steps = 500,
						agent_reporters = {"interactions": "unique_interactions",
									"interaction_time": "interaction_time",
									"conversation_time": "conversation_time",
									"change_IQR": "change_iqr",
									"change_MAD": "change_mad",
									"change_Speechrate": "change_speechrate",
									"change_PauseFreq": "change_pause",
									"social_sync": "social_sync",
									"activity": "activity",
									"IQR": "iqr"})

batch_run.run_all()

#batch_data = batch_run.get_agent_vars_dataframe()
#batch_data.to_csv("batch_data.csv")