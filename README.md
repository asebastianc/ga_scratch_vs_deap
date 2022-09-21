# Comparing genetic optimisation algorithms: scratch developed algorithm against published algorithm
This **repository** contains all the scripts, codes and datasets for *performing* two optimisation algorithms (GA's), *storing* corresponding results and *comparing* them.

## Requisites
`Python` is required for reproducing the analysis. Further documentation [here](https://www.python.org/).

## Reproducibility
In order to reproduce the analysis, it is necessary to follow the subsecuent steps:
1. Run both algorithms
2. Compare results

### Run both algorithms
As the aim of this work is to compare two optimisation algorithms (scratch developed algorithm & DEAP library algorithm), the user should run the two algorithms. The order in which they are performed is unimportant.

**Scratch algorithm**

Algorithm contained inside `scratch` folder within `code`. `scratch` contains two files:
- `scratch.py`: stores the complete implementation of the GA.
- `scratch_analysis.py`: performs the GA by calling objects from `scratch.py`.

For *running* and *saving* the findings of the **scratch algorithm** just excecute `scratch_analysis.py`, the *two procedures* mentioned will be automatically done (`furniture_products.csv` source dataset imported from `data` folder).

**DEAP algorithm**

Algorithm contained inside `distributed` folder within `code`. `distributed` contains one file:
- `distributed.py`: stores and performs the complete implementation of the DEAP GA.

For *running* and *saving* the findings of the **DEAP algorithm** just excecute `distributed.py`, the *two procedures* mentioned will be automatically done (`furniture_products.csv` source dataset imported from `data`).

### Compare results
Results from both algorithms are stored inside `results` folder, divided correspondingly into two subfolders: `scratch` and `distributed`.
For comparing the GA's open the `comparison` folder inside `code`, there will be three files:
- `box_plot.py`: creates a box plot comparing the objective values of the two GA's. Exports `box_plot.pdf` to `ìmages` folder.
- `line_plot.py`: creates a line plot comparing the `score ~ space` relation between both algorithms. Exports `line_plot.pdf` to `ìmages`.
- `cleaning.py`: contains a specific function in order to clean the results dataframes. `box_plot.py` and `line_plot.py` use this function.

## Report
Report available as `report.pdf` inside `report` folder. To replicate it please download and unzip `report.zip`, then compile it using `LaTex`.
