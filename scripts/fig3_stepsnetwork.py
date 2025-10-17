import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyArrowPatch
from matplotlib.lines import Line2D
from collections import Counter, defaultdict
from math import sqrt
from utils.config import dir_cleancsv, dir_plots

save_path = dir_plots / "fig3_stepsnetwork.png"

# Load cleaned CSVs
steps_df = pd.read_csv(os.path.join(dir_cleancsv, "Step_Keywords_cleaned.csv"))
outcomes_df = pd.read_csv(os.path.join(dir_cleancsv, "Outcome_Keywords_cleaned.csv"))

# Standardize column names
steps_df.columns = steps_df.columns.str.strip().str.lower().str.replace(r"[\s\-]+", "_", regex=True)
outcomes_df.columns = outcomes_df.columns.str.strip().str.lower().str.replace(r"[\s\-]+", "_", regex=True)

# Merge keywords by study
steps_grouped = steps_df.groupby('citation')['step_keywords'].apply(lambda x: ';'.join(x.dropna())).reset_index()
outcomes_grouped = outcomes_df.groupby('citation')['outcome_keywords_script'].apply(lambda x: ';'.join(x.dropna())).reset_index()
outcomes_grouped.rename(columns={'outcome_keywords_script': 'outcome_keywords'}, inplace=True)


# Merge using lowercase column name 
df = pd.merge(
    steps_grouped,
    outcomes_grouped,
    on='citation',  # lowercase now
    how='outer'
).fillna("")


# Preprocessing stages
stage_map = {
    "Raw data": ["Raw data"],
    "Pre ICA - Signal Cleaning": ["Channel removal", "High-pass filter", "Low-pass filter",
                                  "Bandpass filter", "Notch filter", "Downsample"],
    "Pre ICA - Data Preprocessing": ["Artifact Rejection", "Bad channel detection", "Re-reference", "Epoching"],
    "ICA": ["IC decomposition", "IC rejection"],
    "Post ICA": ["Clustering", "Baseline correction", "Dipole fitting", "Normalization", "Despiking"],
    "Outcome": ["PSD", "ERD/ERS", "ERSP", "CMC"]
}

# Count steps and transitions 
step_counts = Counter()
transition_counts = Counter()

for _, row in df.iterrows():
    steps = [s for s in row["step_keywords"].split(";") if s]
    outcomes = [o for o in row["outcome_keywords"].split(";") if o]

    step_counts.update(steps)

    # Step-to-step transitions
    for i in range(len(steps)-1):
        transition_counts[(steps[i], steps[i+1])] += 1
    # Step-to-outcome transitions
    if steps and outcomes:
        last_step = steps[-1]
        for out in outcomes:
            transition_counts[(last_step, out)] += 1

total_studies = len(df)

# Print descriptive statistics with percentages 
print("=== Preprocessing Steps (Count & %) ===")
for step, count in step_counts.most_common():
    pct = (count / total_studies) * 100
    print(f"{step}: {count} ({pct:.1f}%)")

print("\n=== Top 20 Step Transitions (Count & %) ===")
for (src, dst), count in transition_counts.most_common(20):
    pct = (count / sum(transition_counts.values())) * 100
    print(f"{src} -> {dst}: {count} ({pct:.1f}%)")

# Node stage mapping 
node_stage = {key: stage for stage, keys in stage_map.items() for key in keys}
layer_order = ["Raw data", "Pre ICA - Signal Cleaning", "Pre ICA - Data Preprocessing", "ICA", "Post ICA", "Outcome"]
stage_y = {stage: -i for i, stage in enumerate(layer_order)}

def get_node_positions(G, node_stage):
    """Arrange nodes by stage and center them horizontally."""
    positions = {}
    x_coords = defaultdict(int)
    for node in G.nodes():
        stage = node_stage.get(node, "Raw data")
        y = stage_y.get(stage, -10)
        positions[node] = (x_coords[y], y)
        x_coords[y] += 1
    for y_val, count in x_coords.items():
        nodes_at_y = [n for n, pos in positions.items() if pos[1] == y_val]
        for i, node in enumerate(nodes_at_y):
            positions[node] = (i - (count - 1)/2.0, y_val)
    return positions

# Plotting
def plot_preprocessing_flow(transition_counts, node_stage_map, title="EEG Preprocessing Flow Across Studies"):
    G = nx.DiGraph()
    for (src, dst), weight in transition_counts.items():
        G.add_edge(src, dst, weight=weight)

    # Node colors
    color_map = {
        "Raw data": "#A9A9A9",
        "Pre ICA - Signal Cleaning": "#FF8C42",
        "Pre ICA - Data Preprocessing": "#20B2AA",
        "ICA": "#9370DB",
        "Post ICA": "#D9534F",
        "Outcome": "#3CB371"
    }

    node_colors = [color_map.get(node_stage_map.get(node, "Raw data"), "gray") for node in G.nodes()]
    node_sizes = [300 + 200 * G.degree(n) for n in G.nodes()]
    pos = get_node_positions(G, node_stage_map)

    fig, ax = plt.subplots(figsize=(30, 16), dpi=600)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=20, font_weight="bold", ax=ax)

    # Draw edges with weight-based style
    def edge_style(weight):
        if weight <= 5:
            return "#d3d3d3", 1.5  
        elif weight <= 10:
            return "#696363", 2.0  
        elif weight <= 15:
            return "#612943a9", 2.5 
        elif weight <= 20:
            return "#022f81", 3.0 
        elif weight <= 30:
            return "#460372", 3.6  
        elif weight <= 35:
            return "#361c0a", 4.0  
        else:  
            return "black", 4.5


    for u, v in G.edges():
        w = G[u][v]['weight']
        color, width = edge_style(w)
        start, end = pos[u], pos[v]
        dx, dy = end[0]-start[0], end[1]-start[1]
        dist = sqrt(dx**2 + dy**2)
        if dist == 0: continue
        node_radius = 0.3
        arrow_start = (start[0] + dx*node_radius/dist, start[1] + dy*node_radius/dist)
        arrow_end = (end[0] - dx*node_radius/dist, end[1] - dy*node_radius/dist)
        arrow = FancyArrowPatch(posA=arrow_start, posB=arrow_end, connectionstyle="arc3,rad=0.2",
                                arrowstyle="->", mutation_scale=20, color=color, linewidth=width, alpha=0.8)
        ax.add_patch(arrow)

    # Legends
    node_legend = [Patch(facecolor=c, edgecolor="black", label=stage) for stage, c in color_map.items()]
    edge_legend = [
        Line2D([0], [0], color="#d3d3d3", lw=2, label="1–5 articles"),
        Line2D([0], [0], color="#696363", lw=2, label="6–10 articles"),
        Line2D([0], [0], color="#612943a9", lw=2, label="11–15 articles"),
        Line2D([0], [0], color="#022f81", lw=2, label="16–20 articles"),
        Line2D([0], [0], color="#460372", lw=2, label="21–30 articles"),
        Line2D([0], [0], color="#361c0a", lw=2, label="31–35 articles"),
        Line2D([0], [0], color="black", lw=2, label="36+ articles")
    ]
    first_legend = ax.legend(handles=node_legend, title="Preprocessing Stages", fontsize=16, loc="upper left", bbox_to_anchor=(0.85,0.55))
    ax.add_artist(first_legend)
    ax.legend(handles=edge_legend, title="Step Transition Frequency", fontsize=16, loc="upper left", bbox_to_anchor=(0.95,0.27))

    plt.title(title, fontsize=22, weight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(save_path, dpi=600, bbox_inches="tight")
    plt.show()

# Run plot
plot_preprocessing_flow(transition_counts, node_stage)

print(f"\nPlot saved to: {save_path}")