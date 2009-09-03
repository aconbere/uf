import sys
from pkg_resources import resource_filename
sys.path.append(".")

from uf import hCal


def test_valid_hcal():
    parser = hCal()
    with open(resource_filename("uf", "examples/hcal.html"), "r") as f:
        vcal = parser.parse(f)
        assert("http://www.web2con.com/" == vcal.contents['vevent'][0].contents['url'][0].value)
        assert("Web 2.0 Conference" == vcal.contents['vevent'][0].contents['summary'][0].value)
        assert("Argent Hotel, San Francisco, CA" == vcal.contents['vevent'][0].contents['location'][0].value)
