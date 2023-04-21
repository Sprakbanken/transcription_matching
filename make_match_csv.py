import sqlite3
from matching.process import make_match_df, add_text_cols, add_context_cols
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str,
                    help="Path to the CSV file containing the matched dataset")
parser.add_argument("-c", "--context", action="store_true",
                    help=("Include 'context_before' and 'context_after' with "
                          "preceding and subsequent text from the proceedings"))
args = parser.parse_args()


DATABASE_PATH = "results.db"

if __name__ == "__main__":

    con = sqlite3.Connection(DATABASE_PATH)
    df_results = make_match_df(con)
    df_results = add_text_cols(df_results)
    if args.context:
        df_results = add_context_cols(df_results)
    df_results.to_csv(args.path, index=False)
    con.close()
