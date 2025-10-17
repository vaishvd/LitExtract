import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.config import dir_data, dir_plots
from itertools import product

# Load data
data_path = dir_data / "20251003_Elicitrevised.csv"
save_path = dir_plots / "fig2_eeg_gait_heatmap.png"
df = pd.read_csv(data_path, sep=";")
print(f"Loaded {len(df)} studies from {data_path.name}\n")

# Clean column names
df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)

# Explode multi-value columns using Cartesian product 
rows = []
for _, row in df.iterrows():
    eeg_types = [e.strip() for e in str(row.get("Type_of_EEG_electrodes", "")).split(";") if e.strip()]
    gait_systems = [g.strip() for g in str(row.get("Gait_measurement_system", "")).split(";") if g.strip()]
    for eeg, gait in product(eeg_types, gait_systems):
        rows.append({"Type_of_EEG_electrodes": eeg, "Gait_measurement_system": gait})

df_expanded = pd.DataFrame(rows)

# Pivot for heatmap
heat_data = df_expanded.groupby(
    ["Type_of_EEG_electrodes", "Gait_measurement_system"]
).size().unstack(fill_value=0)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(
    heat_data,
    annot=True,
    fmt="d",
    cmap="OrRd", 
    linewidths=0.5,
    linecolor="gray",
    cbar=False
)
plt.title("EEG Electrode Types vs Gait Measurement Systems", fontsize=16, weight='bold')
plt.ylabel("Type of EEG Electrodes", fontsize=12)
plt.xlabel("Gait Measurement System", fontsize=12)
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig(save_path, dpi=600, bbox_inches="tight")
plt.show()

# Descriptive statistics
print("Number of studies per EEG electrode type:")
print(df_expanded["Type_of_EEG_electrodes"].value_counts(), "\n")

print("Number of studies per gait measurement system:")
print(df_expanded["Gait_measurement_system"].value_counts(), "\n")

print("EEG electrode type vs gait measurement system (cross-tabulation):")
print(heat_data, "\n")

print("Percentage distribution (row-wise):")
heat_percent = heat_data.div(heat_data.sum(axis=1), axis=0) * 100
print(heat_percent.round(1))

# Descriptive statistics with percentages 
print("Number of studies per EEG electrode type:")
counts_eeg = df_expanded["Type_of_EEG_electrodes"].value_counts()
percent_eeg = df_expanded["Type_of_EEG_electrodes"].value_counts(normalize=True) * 100
df_eeg_stats = pd.DataFrame({"Count": counts_eeg, "Percentage (%)": percent_eeg.round(1)})
print(df_eeg_stats, "\n")

print("Number of studies per gait measurement system:")
counts_gait = df_expanded["Gait_measurement_system"].value_counts()
percent_gait = df_expanded["Gait_measurement_system"].value_counts(normalize=True) * 100
df_gait_stats = pd.DataFrame({"Count": counts_gait, "Percentage (%)": percent_gait.round(1)})
print(df_gait_stats, "\n")

print("EEG electrode type vs gait measurement system (cross-tabulation with percentages):")
cross_tab = df_expanded.groupby(["Type_of_EEG_electrodes", "Gait_measurement_system"]).size().unstack(fill_value=0)
cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
cross_tab_percent = cross_tab_percent.round(1)
cross_tab_combined = cross_tab.astype(str) + " (" + cross_tab_percent.astype(str) + "%)"
print(cross_tab_combined)

