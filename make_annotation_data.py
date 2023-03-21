import pandas as pd
import numpy as np

RESULT_CSV_PATH = "all_matches.csv"
ANNOTATED_DATASET_PATH = "data/annotated_dataset.csv"

if __name__ == "__main__":
    result_df = pd.read_csv(RESULT_CSV_PATH)
    sampledata = result_df.sample(2000, random_state=1)
    sampledata["missing_start_word"] = np.nan
    sampledata["missing_end_word"] = np.nan
    sampledata["wrong_match"] = np.nan
    sampledata["wrong_language"] = np.nan
    sampledata["low_quality"] = np.nan
    sampledata.to_csv(ANNOTATED_DATASET_PATH, index=False)