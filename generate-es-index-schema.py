import logging
import json
import warnings

import pandas as pd

import argparse
from argparse import RawTextHelpFormatter

from elasticsearch import Elasticsearch, RequestsHttpConnection

LOG_FORMAT = "[%(asctime)s] - %(message)s"
DEBUG_LOG_FORMAT = "[%(asctime)s - %(name)s - %(levelname)s] - %(message)s"

HEAD_COLUMN = ['name', 'type', 'aggregatable', 'description']
DICT_INDEX_FIELDS = {}


def configure_logging(debug):
    """
    Configure logging.
    This function sets basic attributes for logging.
    :param debug: set the debug mode
    """
    if not debug:
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT)
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format=DEBUG_LOG_FORMAT)


def parse_args():
    """
    Setup command line argument parsing with argparse.
    """
    parser = argparse.ArgumentParser(
        description="generate es index schema script argument parser",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument('index_name', help="es index name")

    parser.add_argument("-m", "--method",
                        required=True,
                        help="method of fetching index data (cleint \n\n")

    parser.add_argument("-f", "--file",
                        default="schema.csv",
                        help="schema file\n\n")

    parser.add_argument("-d", "--debug",
                        action='store_true',
                        help="set debug mode for logging\n\n")

    return parser.parse_args()


def get_mapping(index_name, method):
    if method == "dump":
        logging.debug("opening the file dump")
        with open('mapping') as file:
            mapping = json.load(file)
    elif method == "client":
        # es = Elasticsearch()
        logging.debug("connecting to elasticsearch using client")
        es = Elasticsearch("https://admin:admin@localhost:9200",
                           verify_certs=False,
                           connection_class=RequestsHttpConnection)

        mapping = es.indices.get_mapping(index_name)
    else:
        log.error("method incorrect (should be either `dump` or `client`")
        sys.exit(0)

    return mapping[index_name]['mappings']['items']


def generate_schema(items, prefix):

    fields = items['properties']
    names = list(fields.keys())

    for name in names:
        if 'type' in fields[name].keys():
            if prefix != '':
                line = [prefix + "." + name]
            else:
                line = [name]
            line.extend([fields[name]['type'], "true", "'NA'"])
            DICT_INDEX_FIELDS[prefix + "." + name] = line
        elif 'properties' in fields[name].keys():
            generate_schema(fields[name], str(name))


def create_schema_file(source_file):
    # convert the dictionary to a dataframe and sort base on 'name'
    df = pd.DataFrame(columns=HEAD_COLUMN, data=list(DICT_INDEX_FIELDS.values()))
    df.sort_values('name')
 
    # convert the dataframe to a csv
    df.to_csv(source_file, sep=',', index=False)


def main():
    """
    A script for generating schema template of an index.

    The script can be run via the command line:
        $ python3 generate-es-index-schema.py index_name -m client

    Examples:
    --------

    * Create a schema file `git.csv` of the index `git-enriched` using the dump menthod:
            $ curl -XGET -k "https://admin:admin@localhost:9200/git-enriched/" > mapping
            $ python3 generate-es-index-schema.py git-enriched -m dump -f git.csv
    """

    args = parse_args()

    index_name = str(args.index_name)
    source_file = str(args.file) if args.file else "schema.csv"
    method = str(args.method)

    configure_logging(args.debug)
    logging.info("start")

    logging.info("fetching mapping for " + index_name)
    mapping_items = get_mapping(index_name, method)
    logging.info("mapping fetched")

    logging.info("generating schema for " + index_name)
    generate_schema(mapping_items, '')
    logging.info("schema generated")

    logging.info("generating schema file, " + source_file)
    create_schema_file(source_file)  
    logging.info("schema file generated")


if __name__ == '__main__':
    try:
        warnings.filterwarnings("ignore")
        main()
        logging.info("done!")
    except KeyboardInterrupt:
        sys.stderr.write("\n\nReceived Ctrl-C or other break signal. Exiting.\n")
        sys.exit(0)
