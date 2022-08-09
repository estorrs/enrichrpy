# enrichrpy
A tool for gene set enrichment (GSEA) plots and analysis in Python. Built on top of Enrichr API.

## Installation

enrichrpy is easily installed with the pip package manager.

Python>=3.6 required.

```bash
pip install enrichrpy
```

## Basic Usage

A collab notebook with basic usage examples is available [here](https://github.com/estorrs/enrichrpy/blob/main/notebooks/basic_usage.ipynb)

#### Enrichr GSEA statistics

```python
import enrichrpy.enrichr as een
import enrichrpy.plotting as epl

genes = [
    'TYROBP', 'HLA-DRA', 'SPP1', 'LAPTM5', 'C1QB',
    'FCER1G', 'GPNMB', 'FCGR3A', 'RGS1', 'HLA-DPA1',
    'ITGB2', 'C1QC', 'HLA-DPB1', 'IFI30', 'SRGN',
    'APOC1', 'CD68', 'HLA-DRB1', 'C1QA', 'LYZ',
    'APOE', 'HLA-DQB1', 'CTSB', 'HLA-DQA1', 'CD74',
    'AIF1', 'FCGR2A', 'CD14', 'S100A9', 'CTSS'
]

df = een.get_pathway_enrichment(genes, gene_set_library='GO_Biological_Process_2021')
df
```

[[/images/datatable.jpg|datatable]]

#### Enrichment bar plot

```python
epl.enrichment_barplot(df, n=20)
```

[[/images/barplot.jpg|barplot]]

#### Enrichment dot plot

```python
epl.enrichment_dotplot(df, n=20, hue='Z-score', log=True)
```

[[/images/dotplot.jpg|dotplot]]
