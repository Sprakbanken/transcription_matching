import sqlite3
from matching.process import make_match_df, add_text_cols

if __name__ == "__main__":
    DB = "results.db"
    con = sqlite3.Connection(DB)
    df_results = make_match_df(con)
    df_results = add_text_cols(df_results)
    df_results.to_csv("/media/pers/elements/npscpluss_large_files/all_matches.csv", index=False)
    con.close()