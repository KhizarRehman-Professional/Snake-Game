# visualize.py - Matplotlib Visualization + Graphs

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

def show_dashboard(df: pd.DataFrame):
    """
    Shows a multi-chart dashboard of game stats.
    Covers: line graph, bar chart, histogram, pie chart.
    """
    if df.empty or len(df) < 1:
        print("Not enough data to visualize. Play some games first!")
        return

    scores = df["score"].astype(int)
    sessions = df["session"].astype(int)

    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("Snake Game - Stats Dashboard", fontsize=16, fontweight="bold")

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.4)

    # ── 1. Score over time (Line Graph) ──────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(sessions, scores, marker="o", color="#2ecc71", linewidth=2, markersize=5)
    ax1.fill_between(sessions, scores, alpha=0.15, color="#2ecc71")
    ax1.set_title("Score Over Sessions")
    ax1.set_xlabel("Session")
    ax1.set_ylabel("Score")
    ax1.grid(True, linestyle="--", alpha=0.5)

    # ── 2. Bar chart: score per session ──────────────────────────────────
    ax2 = fig.add_subplot(gs[1, :2])
    colors = ["#e74c3c" if s == scores.max() else "#3498db" for s in scores]
    ax2.bar(sessions, scores, color=colors, edgecolor="white", linewidth=0.5)
    ax2.set_title("Score Per Session (Red = Best)")
    ax2.set_xlabel("Session")
    ax2.set_ylabel("Score")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    # ── 3. Histogram of score distribution ───────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(scores, bins=max(5, len(scores)//2), color="#9b59b6", edgecolor="white")
    ax3.set_title("Score Distribution")
    ax3.set_xlabel("Score")
    ax3.set_ylabel("Frequency")

    # ── 4. Pie chart: Human vs AI sessions ───────────────────────────────
    ax4 = fig.add_subplot(gs[1, 2])
    mode_counts = df["mode"].value_counts()
    ax4.pie(mode_counts, labels=mode_counts.index,
            autopct="%1.0f%%", colors=["#3498db", "#e67e22"],
            startangle=90, wedgeprops={"edgecolor": "white"})
    ax4.set_title("Human vs AI Sessions")

    plt.savefig("stats_dashboard.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("[Visualize] Dashboard saved as stats_dashboard.png")


def show_numpy_analysis(df: pd.DataFrame):
    """Extra NumPy-based analysis plot"""
    if df.empty:
        return
    scores = df["score"].astype(int).values
    mean = np.mean(scores)
    std = np.std(scores)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(scores, "o-", color="#2ecc71", label="Scores")
    ax.axhline(mean, color="#e74c3c", linestyle="--", label=f"Mean: {mean:.1f}")
    ax.axhline(mean + std, color="#f39c12", linestyle=":", label=f"+1 STD: {mean+std:.1f}")
    ax.axhline(mean - std, color="#f39c12", linestyle=":", label=f"-1 STD: {mean-std:.1f}")
    ax.fill_between(range(len(scores)), mean - std, mean + std, alpha=0.1, color="#f39c12")
    ax.set_title("NumPy Statistical Analysis")
    ax.set_xlabel("Session")
    ax.set_ylabel("Score")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("numpy_analysis.png", dpi=120)
    plt.show()
    print("[Visualize] NumPy analysis saved as numpy_analysis.png")
