import requests
import os
import time
import pandas as pd
import argparse


def get_path_to_venn_txts(path):
    paths_to_venn_txts = dict()
    cell_locs = ['CellWall', 'Cytoplasmic', 'CytoplasmicMembrane', 'Extracellular', 'Context']
    for loc in cell_locs:
        if loc == 'Context':
            loc_path = os.path.join(path, 'Identified_Proteins.txt')
            paths_to_venn_txts[loc] = loc_path
        else:
            loc_path = os.path.join(path, loc + '.txt')
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

def get_STRING_IDs(loc_slices,NCBI_taxon, caller_id, path):
    ## snippet adapted from string api examples

    new_loc_slices = dict()
    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "tsv"
    method = "get_string_ids"

    for loc in loc_slices:
        os.makedirs(os.path.join(path, 'ID_tables',f'{loc}'), exist_ok=True)
        new_loc_slices[loc] = dict()
        for slice in loc_slices[loc]:
            time.sleep(1)
            params = {

                "identifiers": "\r".join(loc_slices[loc][slice]['IDs']),
                "species": NCBI_taxon,
                "echo_query": 1,
                "caller_identity": caller_id

            }

            request_url = "/".join([string_api_url, output_format, method])
            results = requests.post(request_url, data=params)
            if len(results.text.splitlines()) > 3:
                with open(os.path.join(path, 'ID_tables', f'{loc}', f'{slice}.tsv'), 'w') as f:
                    f.write(results.text)
                print(f'{loc} - {slice} STRING IDs done')
                new_loc_slices[loc][slice] = loc_slices[loc][slice]
            else:
                print('STRING IDs not computed there were not enough query proteins')

    loc_slices = new_loc_slices
    return loc_slices

def get_STRING_enrichment(loc_slices,NCBI_taxon, caller_id, path):

    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "tsv"
    method = "enrichment"

    request_url = "/".join([string_api_url, output_format, method])

    for loc in loc_slices:
        os.makedirs(os.path.join(path, 'Enrichment', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(1)
            df_query = pd.read_csv(os.path.join(path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep = '\t', header = 0)
            if 'Error' in df_query.columns:
                with open(os.path.join(path, 'Enrichment', f'{loc}', f'{slice}.tsv'), 'w') as f:
                    f.write('It was not possible to provide functional enrichment data for this section because none of the proteins \n were identified by STRING')
            else:
                query_IDs = df_query['stringId'].tolist()

            if loc != 'Context':
                df_context = pd.read_csv(os.path.join(path, 'ID_tables', 'Context', f'{slice}.tsv'), sep='\t', header=0)
                context_IDs = df_context['stringId'].tolist()


            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "caller_identity": caller_id

            }

            if loc != 'Context':
                params["background_string_identifiers"] = "%0d".join(context_IDs)

            results = requests.post(request_url, data=params)
            #if results.text.startswith('')
            with open(os.path.join(path, 'Enrichment', f'{loc}', f'{slice}.tsv'), 'w') as f:
                f.write(results.text)
            print(f'{loc} - {slice} Enrichment done')

def get_network_images(loc_slices,NCBI_taxon, caller_id, path):

    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "image"
    method = "network"

    request_url = "/".join([string_api_url, output_format, method])

    for loc in loc_slices:
        os.makedirs(os.path.join(path, 'Network_figures', f'{loc}'), exist_ok=True)
        for slice in loc_slices[loc]:
            time.sleep(1)

            df_query = pd.read_csv(os.path.join(path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep="\t", header=0)
            query_IDs = df_query['stringId'].tolist()

            params = {

                "identifiers": "%0d".join(query_IDs),
                "species": NCBI_taxon,
                "required_score": 150,
                "flat_node_design": 1,
                "caller_identity": caller_id

            }
            results = requests.post(request_url, data=params)
            if results.status_code == 200:
                with open(os.path.join(path, 'Network_figures', f'{loc}', f'{slice}.svg'), 'wb') as f:
                    f.write(results.content)
                print(f'{loc} - {slice} network image saved')
            else:
                print(f"Failed to retrieve network image. Status code: {results.status_code}")

def get_results_links(loc_slices,NCBI_taxon, path):

    string_api_url = "https://string-db.org/cgi"
    method = "network"

    request_url = "/".join([string_api_url, method])
    links_txt = 'Links to STRING result pages: \n Cell Localization \t Strain Intersection \t Link \n'
    for loc in loc_slices:
        for slice in loc_slices[loc]:
            time.sleep(1)

            df_query = pd.read_csv(os.path.join(path, 'ID_tables', f'{loc}', f'{slice}.tsv'), sep="\t",
                                   header=0)
            query_IDs = df_query['stringId'].tolist()

            params = f'identifiers={"%0d".join(query_IDs)}&species={NCBI_taxon}&required_score=150&flat_node_design=1'

            link = f'{request_url}?{params}'
            links_txt = links_txt + f'{loc} \t {slice} \t {link} \n'
            print(f'{loc} - {slice} link saved')

    with open(os.path.join(path, 'Links_to_results.tsv'), 'w') as f:
        f.write(links_txt)

def parse_args():

    parser = argparse.ArgumentParser(description=('Batch query STRING\'s database for functional annotation, ' 
                                                  'GO-term enrichment and protein interaction networks of a given sub-cellular localization '
                                                  'from a given strain\'s proteome in the context of all the observed strain\'s proteome '
                                                  'for the given sub-cellular localization.'),  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p','--pathtoworkingdirectory',required=True, help='Path to working directory where the proteome intersection .txt\'s are located')

    parser.add_argument('-s','--strains',nargs='+', required=True, help='list of strains considered')

    parser.add_argument('-t','--taxon', required=True, help='NCBI Taxon ID')

    parser.add_argument('-c', '--caller-id', type=str, required=True, help='Caller ID for STRING')

    parser.add_argument('-e','--enrichment', action='store_true', help= 'get functional enrichment table .tsv')

    parser.add_argument('-n','--network', action='store_true', help= 'get protein network image .png\'s')

    parser.add_argument('-l','--link', action='store_true', help= 'get links to the STRING query results pages')

    return parser.parse_args()

def main(args):
    NCBI_taxon = args.taxon
    strains = args.strains
    caller_id = args.caller_id
    path = args.pathtoworkingdirectory

    paths_to_venn_txts = get_path_to_venn_txts(path)
    loc_intersections = get_loc_intersections(paths_to_venn_txts, strains)
    loc_slices = get_STRING_IDs(loc_intersections, NCBI_taxon, caller_id, path)

    if args.enrichment:
        get_STRING_enrichment(loc_slices,NCBI_taxon, caller_id, path)
    if args.network:
        get_network_images(loc_slices, NCBI_taxon, caller_id, path)
    if args.link:
        get_results_links(loc_slices, NCBI_taxon, path)

if __name__ == "__main__":
    args = parse_args()
    main(args)
