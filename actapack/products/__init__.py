# Add an import statement for your module
from .map import *
from .beam import *

# If you are adding a product you can use the following template
# in your module. Please only define the product class in this 
# module.

### PRODUCT TEMPLATE in module file hotdog.py ###

# from .product import Product, make_implements_decorator

# import numpy as np

# class HotDog(Product):

#     implementedmethods = []
#     implements = make_implements_decorator(implementedmethods)
    
#     def __init__(self, **kwargs):
#         # each product needs a system path and a dictionary to hold a 
#         # filename template (see get_hotdog_fn)
#         product_tag = os.path.splitext(os.path.basename(__file__))[0]
#         setattr(self, f'{product_tag}_path', kwargs.pop(f'{product_tag}_path'))
#         setattr(self, f'{product_tag}_dict', kwargs.pop(f'{product_tag}_dict'))
#         super().__init__(**kwargs)

#     @implements(Product.get_fn)
#     def get_hotdog_fn(self, qid, condiment='mustard'):
#         # use self.hotdog_path, self.hotdog_dict, arguments
#         fn_template = self.hotdog_dict['hotdog_file_template']

#         fn_kwargs = {}
#         fn_kwargs.update(self.qid_dict[qid]) # add info about the requested array
#         fn_kwargs.update(dict(               # add args passed to this method
#             condiment=condiment
#         ))

#         fn = fn_template.format(**fn_kwargs) # format the file string

#         return os.path.join(self.hotdog_path, fn)

#     @implements(Product.read_product)
#     def read_hotdog(self, qid, condiment='mustard', *args, **kwargs):
#         # use get_hotdog_fn and some external library to load the data
#         fn = self.get_hotdog_fn(qid, condiment=condiment)
#         return np.loadtxt(fn, *args, **kwargs)