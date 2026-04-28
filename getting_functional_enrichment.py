import requests
import os
import time #STRING asks that we wait 1 second in between queries

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

def convert_IDs_to_string(loc_slices):
    ## snippet adapted from string api examples

    string_api_url = "https://version-12-0.string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"

    for loc in loc_slices:
        for slice in loc_slices[loc]:
            time.sleep(2)
            params = {

                "identifiers": "\r".join(loc_slices[loc][slice]['IDs']),  # your protein list
                "species": NCBI_taxon,  # NCBI/STRING taxon identifier
                "echo_query": 1,  # see your input identifiers in the output
                "caller_identity": "www.awesome_app.org"  # your app name

            }

            request_url = "/".join([string_api_url, output_format, method])
            results = requests.post(request_url, data=params)
            with open(os.path.join(general_path, 'ID_tables', f'{loc} - {slice}.tsv'), 'w') as f:
                f.write(results.text)
            print(f'{loc} - {slice} done')




## def get_string_functional_annotation(string_IDs):

general_path = r'C:\Users\gomam\Estágio ITQB\Growth curve MIC PA 11k 13k\PsortB\Results\Loc_comparisons'
strains = ['11k', '13k', 's14', 'RP']
NCBI_taxon = 1282

paths_to_venn_txts = get_path_to_venn_txts(general_path)
loc_slices = get_loc_intersections(paths_to_venn_txts, strains)
string_IDs = convert_IDs_to_string(loc_slices)

