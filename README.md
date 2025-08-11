# LitExtract

This repository contains scripts for automated literature retrieval from biomedical publications, for the paper "Preprocessing on the Move:An Overview of Preprocessing Pipelines in Gait-related Mobile EEG".  

## Installation

Use poetry to install the dependencies

## Suggested workflow
The [`scripts`](scripts) folder contains codes to retreive and filter articles from PubMed, extract the methods section as .txt files and store them in your local PC. These files can be parsed for parameters of interest using a script with LLM. The workflow is as follows,

```mermaid
graph TD;
  A[retrieve_articles.py] -->|Fetches articles relevant to keywords from PubMed| B[filter_researcharticles.py];
  B -->|Filters research articles| C[extractmethods.py];
  C -->|Extracts methodology sections

%% Styling for better visualization %%
  style A fill:#f9ebae,stroke:#333,stroke-width:2px;
  style B fill:#b3e5fc,stroke:#333,stroke-width:2px;
  style C fill:#c8e6c9,stroke:#333,stroke-width:2px;
```

## Prompting
To extract parameters from selected articles, the prompts are saved in [`utils/prompts.txt`](utils/prompts.txt)

## Authors
- v.vinod@neurologie.uni-kiel.de
- j.welzel@neurologie.uni-kiel.de
