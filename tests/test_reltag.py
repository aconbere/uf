import sys
sys.path.append(".")

from uf import RelTag

reltag_valid = """<a href="http://anders.conbere.org" rel="tag">Anders Conbere</a>"""
reltag_invalid = """<a href="http://anders.conbere.org" rel="contact colleague something">Anders Conbere</a>"""
    
def test_get_properties():
    parser = RelTag()
    output = parser.parse(reltag_valid)
    assert([u'http://anders.conbere.org'] == output['tag'])
