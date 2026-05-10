import requests
import os
import time #STRING asks that we wait 1 second in between queries
import pandas as pd


def get_path_to_venn_txts(general_path):
    paths_to_venn_txts = dict()
    cell_locs = ['CellWall', 'Cytoplasmic', 'CytoplasmicMembrane', 'Extracellular', 'Context']
    for loc in cell_locs:
        if loc == 'Context':
            loc_path = os.path.join(general_path, 'Identified_Proteins.txt')
            paths_to_venn_txts[loc] = loc_path
        else:
            loc_path = os.path.join(general_path, loc + '.txt')
            paths_to_venn_txts[loc] = loc_path


    return paths_to_venn_txts

def get_loc_intersections(paths_to_venn_txts, strains):
    loc_intersections = dict()
    for loc in paths_to_venn_txts.keys():
        loc_intersections[loc] = dict()
        with open(paths_to_venn_txts[loc], 'r') as f:
            for line in f:
                line = line.strip().split()
                if any(item in strains for item in line):
                    slice_name = "-".join(line[:-2])
                    loc_intersections[loc][slice_name] = dict()
                    loc_intersections[loc][slice_name]['size'] = line[-2]
                    loc_intersections[loc][slice_name]['IDs'] = [line[-1]]
                if len(line) == 1:
                    loc_intersections[loc][slice_name]['IDs'].append(line[0])
    return loc_intersections

def get_STRING_IDs(loc_slices):
    ## snippet adapted from string api examples

    new_loc_slices = dict()
    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "tsv"
    method = "get_string_ids"

    for loc in loc_slices:
        os.makedirs(os.path.join(general_path, 'ID_tables',f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(1)
            params = {

                "identifiers": "\r".join(loc_slices[loc][slice]['IDs']),
                "species": NCBI_taxon,
                "echo_query": 1,
                "caller_identity": "Goncalo Maria"

            }

            request_url = "/".join([string_api_url, output_format, method])
            results = requests.post(request_url, data=params)
            if len(results.text.splitlines()) > 3:
                with open(os.path.join(general_path, 'ID_tables', f'{loc}', f'{slice}.tsv'), 'w') as f:
                    f.write(results.text)
                print(f'{loc} - {slice} STRING IDs done')
            else:
                print('STRING IDs not computed there were not enough query proteins')


def get_STRING_enrichment(loc_slices):

    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "tsv"
    method = "enrichment"

    request_url = "/".join([string_api_url, output_format, method])

    for loc in loc_slices:
        os.makedirs(os.path.join(general_path, 'Enrichment', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(2)
            df_query = pd.read_csv(os.path.join(general_path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep = '\t', header = 0)
            if 'Error' in df_query.columns:
                with open(os.path.join(general_path, 'Enrichment', f'{loc}', f'{slice}.tsv'), 'w') as f:
                    f.write('It was not possible to provide functional enrichment data for this section because none of the proteins \n were identified by STRING')
            else:
                query_IDs = df_query['stringId'].tolist()

            if loc != 'Context':
                df_context = pd.read_csv(os.path.join(general_path, 'ID_tables', 'Context', f'{slice}.tsv'), sep='\t', header=0)
                context_IDs = df_context['stringId'].tolist()


            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "caller_identity": "Goncalo Maria"

            }

            if loc != 'Context':
                params["background_string_identifiers"] = "%0d".join(context_IDs)

            results = requests.post(request_url, data=params)
            #if results.text.startswith('')
            with open(os.path.join(general_path, 'Enrichment', f'{loc}', f'{slice}.tsv'), 'w') as f:
                f.write(results.text)
            print(f'{loc} - {slice} Enrichment done')

def get_STRING_enrichment_figures(loc_slices):
    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "svg"
    method = "enrichmentfigure"

    request_url = "/".join([string_api_url, output_format, method])

    for loc in loc_slices:
        os.makedirs(os.path.join(general_path, 'Function_figures', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(2)
            df_query = pd.read_csv(os.path.join(general_path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep="\t", header = 0)
            query_IDs = df_query['stringId'].tolist()

            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "caller_identity": "Goncalo Maria",
                "category": "Process",
                "color_palette": "yellow_purple",
                "group_by_similarity": 0.8,
                "x_axis" : "signal"

            }
            results = requests.post(request_url, data=params)
            if results.status_code == 200:
                with open(os.path.join(general_path, 'Function_figures', f'{loc}', f'{slice}.svg'), 'wb') as f:
                    f.write(results.content)
                print(f'{loc} - {slice} image saved')
            else:
                print(f"Failed to retrieve image. Status code: {results.status_code}")

def get_network_images(loc_slices):

    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "image"
    method = "network"

    request_url = "/".join([string_api_url, output_format, method])

    for loc in loc_slices:
        os.makedirs(os.path.join(general_path, 'Network_figures', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(2)

            df_query = pd.read_csv(os.path.join(general_path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep="\t", header=0)
            query_IDs = df_query['stringId'].tolist()

            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "required_score": 150,
                "flat_node_design": 1,
                "caller_identity": "Goncalo Maria"

            }
            results = requests.post(request_url, data=params)
            if results.status_code == 200:
                with open(os.path.join(general_path, 'Network_figures', f'{loc}', f'{slice}.svg'), 'wb') as f:
                    f.write(results.content)
                print(f'{loc} - {slice} network image saved')
            else:
                print(f"Failed to retrieve network image. Status code: {results.status_code}")

def get_results_links(loc_slices):

    string_api_url = "https://string-db.org/cgi"
    method = "network"

    request_url = "/".join([string_api_url, method])
    links_txt = 'Links to STRING result pages: \n Cell Localization \t Strain Intersection \t Link \n'
    for loc in loc_slices:
        os.makedirs(os.path.join(general_path, 'Network_figures', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(1)

            df_query = pd.read_csv(os.path.join(general_path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep="\t",
                                   header=0)
            query_IDs = df_query['stringId'].tolist()

            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "required_score": 150,
                "flat_node_design": 1,
                "caller_identity": "Goncalo Maria"

            }
            response = requests.post(request_url, data=params)
            link = response.url
            links_txt = links_txt + f'{loc} \t {slice} \t {link} \n'
            print(f'{loc} - {slice} link saved')

    with open(os.path.join(general_path, 'Links_to_results.tsv'), 'w') as f:
        f.write(links_txt)

general_path = r'C:\Users\gomam\Estágio ITQB\Growth curve MIC PA 11k 13k\PsortB\Results\Loc_comparisons'
strains = ['11k', '13k', 's14', 'RP']
NCBI_taxon = 1282

paths_to_venn_txts = get_path_to_venn_txts(general_path)

loc_slices = get_loc_intersections(paths_to_venn_txts, strains)
get_STRING_IDs(loc_slices)
get_results_links(loc_slices)


