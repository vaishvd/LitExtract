import pandas as pd
import matplotlib.pyplot as plt
from utils.config import dir_data, dir_plots
from pathlib import Path

# Load data
data_path = dir_data / "20251003_Elicitrevised.csv"
save_path = dir_plots / "fig1_cohort_task.png"

df = pd.read_csv(data_path, sep=";")
print(f"Loaded {len(df)} studies from {data_path.name}\n")

# Data cleaning
df.columns = df.columns.str.strip().str.replace(r"[\s\-]+", "_", regex=True)
df = df.dropna(subset=["Cohort", "Gait_Task"], how="all")

pivot = df.pivot_table(
    index="Cohort",
    columns="Gait_Task",
    values="Citation",
    aggfunc="count",
    fill_value=0
)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
pivot.plot(
    kind="barh",
    stacked=True,
    colormap="tab20",
    edgecolor="none",
    ax=ax
)

ax.set_title("Cohort vs Gait Task Distribution", fontsize=13, weight="bold", pad=15)
ax.set_xlabel("Number of Studies", fontsize=11)
ax.set_ylabel("Cohort", fontsize=11)

label_map = {
    "Overground walking": "Only Overground walking",
    "Treadmill walking": "Only Treadmill walking"
}
handles, labels = ax.get_legend_handles_labels()
new_labels = [label_map.get(lbl, lbl) for lbl in labels]

legend = ax.legend(
    handles,
    new_labels,
    title="Gait Task",
    loc="upper right",           
    bbox_to_anchor=(0.98, 0.98),  
    facecolor="white",
    framealpha=0.9,
    fontsize=9,
    title_fontsize=10,
    borderpad=0.6,
    labelspacing=0.3,
)
legend.get_frame().set_linewidth(0.5)

ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.7)
plt.tight_layout(pad=2.0)

# Save plot
save_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Plot saved to: {save_path}\n")

# Descriptive Statistics
print("Descriptive Statistics\n")

cohort_counts = df["Cohort"].value_counts(dropna=False)
print("Number of studies per cohort:")
print(cohort_counts, "\n")

task_counts = df["Gait_Task"].value_counts(dropna=False)
print("Number of studies per gait task:")
print(task_counts, "\n")

cohort_gait_table = pd.crosstab(df["Cohort"], df["Gait_Task"])
print("Cohort vs Gait Task (cross-tabulation):")
print(cohort_gait_table, "\n")

cohort_gait_percent = cohort_gait_table.div(cohort_gait_table.sum(axis=1), axis=0) * 100
print("Percentage distribution (row-wise):")
print(cohort_gait_percent.round(1))
