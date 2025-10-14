# scripts/fig1_cohort_task.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.config import dir_data, dir_plots

data_path = dir_data / "20251003_Elicitrevised.csv"
save_path = dir_plots / "fig1_cohort_task.png"

df = pd.read_csv(data_path, sep=";")
print(f"Loaded {len(df)} studies from {data_path.name}")

required_cols = ["Cohort", "Gait Task", "Citation"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")


pivot = df.pivot_table(index="Cohort", columns="Gait Task",
                       values="Citation", aggfunc="count", fill_value=0)


plt.figure(figsize=(10, 6))
ax = pivot.plot(kind="barh", stacked=True, colormap="tab20", edgecolor="none")
plt.title("Cohort vs. Gait Task Distribution", fontsize=14, pad=12)
plt.xlabel("Number of Studies")
plt.ylabel("Cohort")

# --- Legend fix ---
handles, labels = ax.get_legend_handles_labels()
label_map = {
    "Overground walking": "Only Overground walking",
    "Treadmill walking": "Only Treadmill walking"
}
new_labels = [label_map.get(lbl, lbl) for lbl in labels]
plt.legend(handles, new_labels, title="Gait Task", bbox_to_anchor=(1.02, 1),
           loc="upper left", facecolor="white", framealpha=0.9,
           fontsize=9, title_fontsize=10)

sns.despine()
plt.tight_layout()

# --- Save ---
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Plot saved to {save_path}")
