import pandas as pd
import numpy as np

if __name__ == "__main__":
    result_df = pd.read_csv("all_matches.csv")
    sampledata = result_df.sample(2000, random_state=1)
    sampledata["missing_start_word"] = np.nan
    sampledata["missing_end_word"] = np.nan
    sampledata["wrong_match"] = np.nan
    sampledata["wrong_language"] = np.nan
    sampledata["low_quality"] = np.nan
    sampledata.to_csv("data/annotated_dataset.csv", index=False)