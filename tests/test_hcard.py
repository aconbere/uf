import sys
from pkg_resources import resource_filename
sys.path.append(".")

from uf import hCard

def test_valid_hcard():
    parser = hCard()
    with open(resource_filename("uf", "examples/hcard.html"), "r") as f:
        vcard = parser.parse(f)
        url = vcard.contents['url'][0].value
        fn = vcard.contents['fn'][0].value
        email = vcard.contents['email'][0].value
        tel = vcard.contents['tel'][0].value
        assert(u'http://www.commerce.net/' == url)
        assert(u'CommerceNet' == fn)
        assert(u'info@commerce.net' == email)
