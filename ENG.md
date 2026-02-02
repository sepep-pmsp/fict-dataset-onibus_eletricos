# Metodology Avaliation Notebooks

[Portuguese Version](README.md)

This repository has 2 notebooks, [SAUDE.ipynb](SAUDE.ipynb) and [SIM_MONTE_CARLO.ipynb](SIM_MONTE_CARLO.ipynb), and they work as documentation for the methodoly of the calculus of health (affected people) and the Monte Carlo Simulation respectively.

This repository was made based on:

1) https://github.com/sepep-pmsp/dash_onibus_eletricos.git
2) https://github.com/sepep-pmsp/onibus_eletricos_saude.git

## DATA
The needed data for running these notebooks are available on this link: https://cloudprodamazhotmail-my.sharepoint.com/:f:/g/personal/oliviaamann_prefeitura_sp_gov_br/IgAy5CupuJ1vQbjsBfV3offGAaMEtRSfylBJUv_yVwjjErk?e=R0n7g3

1) Download the data.zip file on the cloned repository folder.
2) Unzip data folder.
3) Garantee that the folder structure is  se a estrutura das pasta é: `fict-dataset-onibus_eletricos/data/manual_data/`. If the folder structure is not that, the notebooks will return errors when loading the csv archives.
4) Inside the `data/manual_data/` folder, the needed archives are 2: `calculo-emissao-poluentes-diario_2025-12-31_silver.csv` (needed to run SIM_MONTE_CARLO.ipynb) and `linestring_2025-12-31_silver.csv` (needed to run SAUDE.ipynb).

Both archives are real public data, extracted from the Olho Vivo API, by our team on the 31th December, 2025. 

Other used data are the IBGE's census sectors (2022 census), downloaded and treated automatically by the functions on [setores_censitarios.ipynb](setores_censitarios.py), called by the [SAUDE.ipynb](SAUDE.ipynb) notebook.

## [MONTE CARLO SIMULATION](SIM_MONTE_CARLO.ipynb)

This notebook demonstrate how our Monte Carlo Simulation was made to create hypotetycal scenarios where some diesel buses are replaced with electric buses. On our current version, we are only cconsidering the CO2 emition, but the same methodology will be used to estimate other pollutants and the affected population.

Our objective is to create scenarios where we can use both the amout of diesel buses to be replaced or the amout of avoided CO2 emition as starting points.

## [HEALTH](SAUDE.ipynb)

On this notebook we demonstrate how the amount of affect people by MP and NOx polluttants was estimated. Our methodology is considering only the residents, as it uses the census sector data.