"""
The serializer library takes a url, and attempts to convert the returned output
into valid xml. Decoupling this system from the parser allows for much greater
granularity in terms of the pre and post processing of the microformats.
"""

import lxml
