import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def enrichment_barplot(enrichr_results, n=20, scheme='blues'):
    """
    Plots enrichment results in barplot form
    
    Parameters
    ----------
    enrichr_results: pd.DataFrame
      - result dataframe from enrichrpy.enrichr.get_pathway_enrichment
    n: int
      - plot top N pathways, default=20
    scheme: str
      - altair color scheme to use. schemes listed here https://vega.github.io/vega/docs/schemes/
    """
    source = enrichr_results.copy()
    source['Num hits'] = [len(ls) for ls in source['Overlapping genes']]
    source['-log10(FDR)'] = -np.log10(source['Adjusted p-value'])
    source['Pathway'] = source['Term name'].to_list()
    
    if n is not None:
        source = source.sort_values('Adjusted p-value').iloc[:n]
    
    c = alt.Chart(source).mark_bar().encode(
        x=alt.X('-log10(FDR)'),
        y=alt.Y('Pathway', sort={"encoding": "x", "order": "descending"}),
        color=alt.Color('Num hits', scale=alt.Scale(scheme=scheme, domainMin=0))
    )
    xrule = (
        alt.Chart()
            .mark_rule(strokeDash=[8, 6], color="red", strokeWidth=2)
            .encode(x=alt.datum(-np.log10(.05)))
    )
    
    return c + xrule


def enrichment_dotplot(enrichr_results, n=20, hue='Z-score', scheme='viridis', log=True):
    """
    Plots enrichment results in dotplot form
    
    Parameters
    ----------
    enrichr_results: pd.DataFrame
      - result dataframe from enrichrpy.enrichr.get_pathway_enrichment
    n: int
      - plot top N pathways, default=20
    hue: str
      - variable to color the dotplot by, default='Combined score'
    scheme: str
      - altair color scheme to use. schemes listed here https://vega.github.io/vega/docs/schemes/
    """
    source = enrichr_results.copy()
    source['Num hits'] = [len(ls) for ls in source['Overlapping genes']]
    source['-log10(FDR)'] = -np.log10(source['Adjusted p-value'])
    source['Pathway'] = source['Term name'].to_list()
    source[f'log({hue})'] = np.log(source[hue])
    
    if n is not None:
        source = source.sort_values('Adjusted p-value').iloc[:n]
        
    
    
    c = alt.Chart(source).mark_circle().encode(
        x=alt.X('-log10(FDR):Q'),
        y=alt.Y('Pathway', sort={"encoding": "x", "order": "descending"}),
        size=alt.Size('Num hits'),
        color=alt.Color(hue if not log else f'log({hue})', scale=alt.Scale(scheme=scheme, domainMin=0))
    )
    xrule = (
        alt.Chart()
            .mark_rule(strokeDash=[8, 6], color="red", strokeWidth=2)
            .encode(x=alt.datum(-np.log10(.05)))
    )
    
    return (c + xrule).configure_axis(grid=True)
