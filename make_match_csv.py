import sqlite3
import argparse
import re

from matching.process import make_match_df, add_text_cols, add_context_cols

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str,
                    help="Path to the CSV file containing the matched dataset")
parser.add_argument("-c", "--context", action="store_true",
                    help=("Include 'context_before' and 'context_after' with "
                          "preceding and subsequent text from the proceedings"))
args = parser.parse_args()


DATABASE_PATH = "results.db"
DATE_PATTERN = r".*(\d{4}\-\d{2}\-\d{2})_.*"

NPSC_TEST_DATES = ["2017-02-07", "2017-12-19", "2018-05-30", "2017-11-22"]
NPSC_EVAL_DATES = ["2018-03-07", "2018-01-09", "2017-02-09", "2018-06-11", "2018-02-01"]


def make_split(date):
    if date in NPSC_EVAL_DATES:
        return "eval"
    elif date in NPSC_TEST_DATES:
        return "test"
    else:
        return "train"


if __name__ == "__main__":

    con = sqlite3.Connection(DATABASE_PATH)
    df_results = make_match_df(con)
    df_results = add_text_cols(df_results)
    df_results["meeting_date"] = df_results.proceedingsfile.apply(
        lambda x: re.sub(DATE_PATTERN, r"\1", x)
    )

    df_results["split"] = df_results.meeting_date.apply(lambda x: make_split(x))

    if args.context:
        df_results = add_context_cols(df_results)
    df_results.to_csv(args.path, index=False)
    con.close()
