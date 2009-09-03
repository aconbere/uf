from uf import XFN

import unittest

xfn_invalid = """<a href="http://anders.conbere.org" rel="tag">Anders Conbere</a>"""
xfn_valid = """<a href="http://anders.conbere.org" rel="contact colleague something">Anders Conbere</a>"""
    
def test_get_properties():
    parser = XFN()
    output = parser.parse(xfn_valid)
    assert({'contact': [u'http://anders.conbere.org'], 'colleague': [u'http://anders.conbere.org']} == output)
