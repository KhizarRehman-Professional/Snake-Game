import pandas as pd # type: ignore
import numpy as np # type: ignore
import os
from datetime import datetime

CSV_FILE = "scores.csv"

class StatsTracker:
    """
    Tracks game sessions and performs EDA using pandas and numpy.
    Demonstrates: data wrangling, basic analysis, CSV I/O.
    """

    def __init__(self):
        if os.path.exists(CSV_FILE):
            self.df = pd.read_csv(CSV_FILE)
        else:
            self.df = pd.DataFrame(columns=["session", "score", "mode", "date"])

    def save_session(self, score, mode="Human"):
        session_num = len(self.df) + 1
        new_row = {
            "session": session_num,
            "score": score,
            "mode": mode,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Data wrangling: append new row
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(CSV_FILE, index=False)
        print(f"[Stats] Session {session_num} saved: Score={score}, Mode={mode}")

    def print_summary(self):
        if self.df.empty:
            print("No sessions recorded yet.")
            return

        scores = self.df["score"].astype(int)

        print("\n========== EDA Summary ==========")
        print(f"Total Sessions  : {len(self.df)}")
        print(f"Highest Score   : {np.max(scores)}")
        print(f"Lowest Score    : {np.min(scores)}")
        print(f"Average Score   : {np.mean(scores):.2f}")
        print(f"Std Deviation   : {np.std(scores):.2f}")
        print(f"Median Score    : {np.median(scores):.2f}")
        print("\n--- Sessions by Mode ---")
        print(self.df.groupby("mode")["score"].describe().to_string())
        print("=================================\n")

    def get_scores(self):
        return self.df.copy()

    def get_best_sessions(self, top_n=5):
        """Data wrangling: filter and sort top sessions"""
        df = self.df.copy()
        df["score"] = df["score"].astype(int)
        return df.nlargest(top_n, "score")[["session", "score", "mode"]]