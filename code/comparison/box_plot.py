import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cleaning import clean_datasets

scratch = pd.read_csv("../../results/scratch/scratch_results.csv")
distributed = pd.read_csv("../../results/distributed/distributed_results.csv")

df = clean_datasets(scratch, distributed, "Space", "Score", "Scratch", "Distributed")

scratch = df[df["GA"] == "Scratch GA"]
scratch = scratch.drop_duplicates("Score")

distributed = df[df["GA"] == "Distributed GA"]
distributed = distributed.drop_duplicates("Score")

sns.set_style("ticks")

fig, axes = plt.subplots(1, 2)
sns.boxplot(x = scratch["GA"], y = scratch["Score"], orient = 'v', ax = axes[0], color = "#8B8B8B", linewidth = 0.5)
sns.boxplot(x = distributed["GA"], y = distributed["Score"], orient = 'v', ax = axes[1], color = "#D0D0D0", linewidth = 0.5)
for ax in axes:
    ax.set_xlabel(None)
fig.supxlabel("Algorithms")
plt.tight_layout()
plt.savefig("../../images/box_plot.pdf")