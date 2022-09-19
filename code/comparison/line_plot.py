import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from cleaning import clean_datasets

scratch = pd.read_csv("../../results/scratch/scratch_results.csv")
distributed = pd.read_csv("../../results/distributed/distributed_results.csv")

df = clean_datasets(scratch, distributed, "Space", "Score", "Scratch", "Distributed")

sns.set_style("ticks")

custom_palette = ["#000000", "#8B8B8B"]
sns.set_palette(custom_palette)

sns.lineplot(x = "Space", y = "Score", hue = "GA", ci = None, data = df)
plt.xticks(np.arange(int(df["Space"].min()), int(df["Space"].max()) + 1, 0.5))
plt.yticks(np.arange(df["Score"].min(), df["Score"].max() + 100, 500))
plt.axvline(x = 6.5, ymin = 0, ymax = 0.98, color = "red", label = r"Constraint $\theta$")
plt.legend(loc = 2, bbox_to_anchor = (0.008, 0.98), fontsize = "small")
plt.tight_layout()
plt.savefig("../../images/line_plot.pdf")