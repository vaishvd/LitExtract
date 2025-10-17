import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
import colorsys
from utils.config import dir_cleancsv, dir_plots

# Load data
data_path = os.path.join(dir_cleancsv, "Artifact_Methods_cleaned.csv")
save_path = dir_plots / "fig5_artifactrej.png"
df_artifact = pd.read_csv(data_path)
df_artifact["Citation"] = df_artifact["citation"].fillna("Unknown Study").astype(str).str.strip()

# Order studies by year
if "Year" in df_artifact.columns:
    df_artifact = df_artifact.sort_values("Year")
studies = df_artifact["Citation"].unique()

# Prepare pivot table 
methods = df_artifact["artifactrej_methods"].unique()
pivot = pd.DataFrame(0, index=studies, columns=methods)
for title, group in df_artifact.groupby("Citation"):
    for m in group["artifactrej_methods"]:
        pivot.loc[title, m] = 1

# Descriptive statistics
method_counts = df_artifact["artifactrej_methods"].value_counts()
avg_methods_per_study = pivot.sum(axis=1).mean()
multi_method_studies = (pivot.sum(axis=1) > 1).sum()

print("Descriptive Statistics")
print(f"Total studies with artifact rejection analyzed: {len(studies)}")
print(f"Total unique artifact rejection methods: {len(methods)}\n")
print("Most common methods:")
print(method_counts.head(10).to_string())
print(f"\nAverage number of methods per study: {avg_methods_per_study:.2f}")
print(f"Number of studies using multiple methods: {multi_method_studies}")

# Assign distinct base colors per method
palette_base = sns.color_palette("tab20", n_colors=len(methods))
method_base_colors = {method: palette_base[i % len(palette_base)] for i, method in enumerate(methods)}

# Map frequency to intensity (darker = more common)
max_count = method_counts.max()
method_colors = {}
min_light, max_light = 0.3, 0.9  # lightest = 0.9, darkest = 0.3
for method in methods:
    # base color in RGB
    r, g, b = method_base_colors[method]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    # darker = more frequent
    freq = method_counts.get(method, 0)
    l_new = max_light - (freq / max_count) * (max_light - min_light)
    r_new, g_new, b_new = colorsys.hls_to_rgb(h, l_new, s)
    method_colors[method] = (r_new, g_new, b_new)

# Plot setup
fig_width = max(18, len(pivot) * 0.25)
fig_height = 10
plt.figure(figsize=(fig_width, fig_height), dpi=600)

bottoms = np.zeros(len(pivot))
for method in pivot.columns:
    plt.bar(
        pivot.index,
        pivot[method],
        bottom=bottoms,
        color=method_colors[method],
        label=method,
        width=0.8
    )
    bottoms += pivot[method].values

plt.xlabel("Studies (Citations)", fontsize=14)
plt.ylabel("Artifact Rejection Methods Used (n per study)", fontsize=14)
plt.title("Artifact Rejection Methods Across Studies", fontsize=20, weight="bold", pad=15)
plt.xticks(rotation=90, ha="center", fontsize=8)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Gradient legend based on frequency
sorted_methods = method_counts.sort_values(ascending=False).index.tolist()
legend_patches = [
    Patch(color=method_colors[m], label=f"{m} ({method_counts[m]})") for m in sorted_methods
]
plt.legend(
    handles=legend_patches,
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    title="Artifact Rejection Methods\n(total count)",
    fontsize=10,
    title_fontsize=12,
    frameon=False
)

plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.savefig(save_path, dpi=600, bbox_inches="tight")
plt.show()

print(f"\nPlot saved to: {save_path}")
