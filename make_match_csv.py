import sqlite3
from matching.process import make_match_df, add_text_cols

OUTPATH = "/media/pers/elements/npscpluss_large_files/all_matches.csv"
DATABASE_PATH = "results.db"

if __name__ == "__main__":
    con = sqlite3.Connection(DATABASE_PATH)
    df_results = make_match_df(con)
    df_results = add_text_cols(df_results)
    df_results.to_csv(OUTPATH, index=False)
    con.close()