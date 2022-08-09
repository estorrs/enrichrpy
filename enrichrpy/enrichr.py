import pandas as pd
import requests

# order of keys for results returned by enrichr
KEYS = [
    'Rank',
    'Term name',
    'P-value',
    'Z-score',
    'Combined score',
    'Overlapping genes',
    'Adjusted p-value',
    'Old p-value',
    'Old adjusted p-value'
]

# Enrichr base url
BASE_URL = 'https://maayanlab.cloud/Enrichr'


def get_enrichr_libraries(names_only=True):
    url = f'{BASE_URL}/datasetStatistics'
    r = requests.get(url)

    if names_only:
        return [d['libraryName'] for d in r.json()['statistics']]
    return r.json()

    

def register_gene_list(genes, description=None):
    """
    Register gene list with Enrichr
    
    Parameters
    ----------
    genes - collection of genes to be registered
    description - description of gene set, optional

    Returns
    -------
    result: dict
      - dict containing user_list_id to use with retrieve_enrichment
    """
    url = f'{BASE_URL}/addList'
    payload = {
        'list': (None, '\n'.join(genes)),
        'description': (None, description)
    }
    
    r = requests.post(url, files=payload)

    if r.status_code == 200:
        return r.json()
    
    raise RuntimeError(f'Invalid response: {r.status_code} \n{r.text}')


def retrieve_enrichment(user_list_id, gene_set_library='GO_Biological_Process_2021'):
    """
    enrichment for registered gene list with Enrichr

    Parameters
    ----------
    user_list_id - id returned by register_gene_list
    gene_set_library - library/pathway/ontology to apply GSEA with. default is GO_Biological_Process_2021. for list of possible libraries/pathways/ontologies see https://maayanlab.cloud/Enrichr/

    Returns
    -------
    results: pd.DataFrame
      - result table from GSEA analysis
    """

    url = f'{BASE_URL}/enrich'
    params = {
        'userListId': user_list_id,
        'backgroundType': gene_set_library
    }
    r = requests.get(url, params=params)

    if r.status_code == 200:
        results = []
        for ls in r.json()[gene_set_library]:
            results.append({k:v for k, v in zip(KEYS, ls)})
        return pd.DataFrame(results)
    
    raise RuntimeError(f'Invalid response: {r.status_code} \n{r.text}')


def get_pathway_enrichment(genes, gene_set_library='GO_Biological_Process_2021'):
    """
    Run pathway enrichment for particular gene set

    Parameters
    ----------
    genes - collection of genes to be used in GSEA
    gene_set_library - library/pathway/ontology to apply GSEA with. default is GO_Biological_Process_2021. for list of possible libraries/pathways/ontologies see https://maayanlab.cloud/Enrichr/

    Returns
    -------
    results: pd.DataFrame
      - result table from GSEA analysis
    """
    response = register_gene_list(genes)
    return retrieve_enrichment(response['userListId'], gene_set_library=gene_set_library)
