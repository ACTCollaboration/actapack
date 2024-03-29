from actapack import utils
from actapack.products import Product

import os

class DataModel(*Product.__subclasses__()):

    def __init__(self, **kwargs):
        """A wrapper class that mixes in all Product subclasses. Also grabs any
        qid-related information to be used in subclass methods, e.g., if a
        product's filenames are labeled by particular array, frequency, etc.

        Notes
        -----
        This class is the only class a user should need. It exposes all product
        methods implemented in this package.
        """
        super().__init__(**kwargs)

    @classmethod
    def from_config(cls, config_name):
        """Build a DataModel instance from configuration files distributed in
        the actapack package.

        Parameters
        ----------
        config_name : str
            The name of the configuration file. If does not end in '.yaml', 
            '.yaml' will be appended.

        Returns
        -------
        DataModel
            Instance corresponding to the collection of products and subproducts
            indicated in the named configuration file.
        """
        dm_kwargs = {}
        
        # first get the datamodel dictionary and system path dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'datamodels/{config_name}'
        datamodel_fn = utils.get_package_fn('actapack', basename)
        datamodel_dict = utils.config_from_yaml_file(datamodel_fn)

        actapack_fn = os.path.join(os.environ['HOME'], '.actapack_config.yaml')
        actapack_config = utils.config_from_yaml_file(actapack_fn)
        system_path_dict = actapack_config[os.path.splitext(config_name)[0]]

        # evaluate the (sub)product dicts and add in the system paths.
        # handle special case of qids_dict separately

        # qids_config: the config basename
        qids_config = datamodel_dict.pop('qids_config')
        if not qids_config.endswith('.yaml'):
            qids_config += '.yaml'

        # qids_fn: the actual config full filename
        basename = f'qids/{qids_config}'
        qids_fn = utils.get_package_fn('actapack', basename)

        # qids_dict: the contents of the filename
        qids_dict = utils.config_from_yaml_file(qids_fn)
        dm_kwargs['qids'] = qids_dict

        dm_kwargs['paths'] = {}
        for product in datamodel_dict:
            dm_kwargs[product] = {}
            dm_kwargs['paths'][product] = {}
            for subproduct, subproduct_config in datamodel_dict[product].items():
                # subproduct_config: the config basename
                if not subproduct_config.endswith('.yaml'):
                    subproduct_config += '.yaml'

                # subproduct_fn: the actual config full filename
                basename = f'products/{product}/{subproduct_config}'
                subproduct_fn = utils.get_package_fn('actapack', basename)

                # subproduct_dict: the contents of the filename
                subproduct_dict = utils.config_from_yaml_file(subproduct_fn)

                # NOTE: check for compatibility of this subproduct with the
                # data_model, meaning the requested qids_dict is allowed
                subproduct = subproduct.split('_config')[0] # remove _config

                if subproduct_dict['allowed_qids_configs'] is not None:
                    if qids_config not in subproduct_dict['allowed_qids_configs']:
                        assert subproduct_dict['allowed_qids_configs'] == 'all', \
                            f'qids_config {qids_config} not allowed by product {product}, ' + \
                            f"subproduct {subproduct} configuration file"

                # if compatible, add to the dm_kwargs
                dm_kwargs[product][subproduct] = subproduct_dict

                # if in user .actapack_config.yaml file, add subproduct path
                if product in system_path_dict:
                    if f'{subproduct}_path' in system_path_dict[product]:
                        subproduct_path = system_path_dict[product][f'{subproduct}_path']
                        dm_kwargs['paths'][product][subproduct] = subproduct_path

        return cls(**dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")