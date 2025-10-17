import os
import pandas as pd
import ast
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_indicators
from itertools import combinations
from utils.config import dir_data, dir_plots

# Load data
data_path = dir_data / "20251003_Elicitrevised.csv"
save_path = dir_plots / "fig4_steps_upset.png"
df = pd.read_csv(data_path, sep=";", engine="python")

# Safe parsing of preprocessing steps
def safe_parse(x):
    if pd.isna(x):
        return []
    try:
        parsed = ast.literal_eval(x)
        if isinstance(parsed, list):
            return [s.strip() for s in parsed if s.strip()]
        return [s.strip() for s in str(x).split(";") if s.strip()]
    except Exception:
        return [s.strip() for s in str(x).replace(",", ";").split(";") if s.strip()]

if "step_keywords" in df.columns:
    df["Pipeline_steps"] = df["step_keywords"].apply(safe_parse)
elif "corrected_keywords_VV" in df.columns:
    df["Pipeline_steps"] = df["corrected_keywords_VV"].apply(safe_parse)
else:
    raise ValueError("No valid step keywords column found in CSV.")

# Extract publication year from citation
if "Citation" in df.columns:
    df["Year"] = df["Citation"].astype(str).str.extract(r"(\d{4})").astype(float).astype("Int64")

# Stage mapping and colors
stage_map = {
    "Raw data": ["Raw data"],
    "Pre ICA - Signal Cleaning": [
        "Channel removal", "High-pass filter", "Low-pass filter",
        "Bandpass filter", "Notch filter", "Downsample"
    ],
    "Pre ICA - Data Preprocessing": [
        "Artifact Rejection", "Bad channel detection",
        "Re-reference", "Epoching"
    ],
    "ICA": ["IC decomposition", "IC rejection"],
    "Post ICA": ["Clustering", "Baseline correction", "Dipole fitting", "Normalization", "Despiking"],
}

color_map = {
    "Raw data": "black",
    "Pre ICA - Signal Cleaning": "#FF8C42",
    "Pre ICA - Data Preprocessing": "#20B2AA",
    "ICA": "#9370DB",
    "Post ICA": "#D9534F"
}

# Reverse mapping: step → stage and color
step_to_color = {s: color_map[stage] for stage, steps in stage_map.items() for s in steps}

# All unique steps and boolean indicators
all_steps = sorted({step for steps in df["Pipeline_steps"] for step in steps})
for step in all_steps:
    df[step] = df["Pipeline_steps"].apply(lambda s: step in s)
df = df.sort_values("Year", ascending=True)
upset_df = df[all_steps].astype(bool)

# Descriptive statistics
step_counts = df["Pipeline_steps"].explode().value_counts()
total_studies = len(df)
print("\n=== Descriptive Statistics ===")
print(f"Total studies: {total_studies}")
print(f"Unique preprocessing steps: {len(all_steps)}\n")
print("Most common preprocessing steps (count | % of studies):")
for step, count in step_counts.items():
    pct = (count / total_studies) * 100
    print(f"{step}: {count} | {pct:.1f}%")

# Pairwise co-occurrence counts
pair_counts = {}
for steps in df["Pipeline_steps"]:
    for combo in combinations(sorted(set(steps)), 2):
        pair_counts[combo] = pair_counts.get(combo, 0) + 1
pair_df = pd.DataFrame(
    [(a, b, c) for (a, b), c in pair_counts.items()],
    columns=["Step_A", "Step_B", "Co_occurrence"]
).sort_values("Co_occurrence", ascending=False)

print("\nTop 10 most frequent co-occurring step pairs:")
print(pair_df.head(10).to_string(index=False))

# Generate UpSet plot 
plt.figure(figsize=(18, 12))
upset = UpSet(
    from_indicators(all_steps, upset_df),
    show_counts=True,
    sort_by="degree",
    element_size=80,
    facecolor="black"
)
upset.plot()

# Color the step labels by stage
axes = plt.gcf().axes
for ax in axes:
    if hasattr(ax, 'get_yticklabels'):
        for label in ax.get_yticklabels():
            text = label.get_text()
            if text in step_to_color:
                label.set_color(step_to_color[text])
                label.set_fontweight("bold")

# Figure formatting
plt.suptitle("Overlap of EEG Preprocessing Steps Across Studies", fontsize=22, weight="bold")
plt.subplots_adjust(left=0.12, right=0.95, bottom=0.1, top=0.9)
plt.rcParams.update({
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 16
})

# Save plot
plt.savefig(save_path, dpi=600, bbox_inches="tight")
plt.show()

print(f"\nHigh-resolution colored UpSet plot saved to:\n{save_path}")
