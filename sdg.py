#!/usr/bin/python
#######################################################################################
#######################################################################################
#
#	Name: sdg.py
#	Usage:
#	Description: Contains class and methods for synthetic data generation
#
#
#
#
#	Modification Log:
#	2019-03-19			Annie Castner				Initial creation
#
#######################################################################################

import numpy as np
import pandas as pd
from utilities import sdg_utils
import yaml
import json


def main():
    # Load Configs
    configs = yaml.safe_load(open("./config.yaml"))

    # Load Schema
    with open(configs['schema']) as f:
        schema = json.load(f)

    function_map = configs['data type functions']

    dfs = pd.DataFrame()

    for field in schema['fields']:
        if 'subtype' in field.keys():
            func1 = function_map[field['type']]
            func = getattr(sdg_utils, func1[field['subtype']])

        else:
            func = getattr(sdg_utils, function_map[field['type']])
        params = field['parameters']
        params['name'] = field['name']
        params['size'] = configs['output']['length']

        data = func(**params)
        dfs = pd.concat([dfs, data], axis=1)

    dfs.to_csv(configs['output']['location'], index=False)


if __name__ == '__main__':
    main()



