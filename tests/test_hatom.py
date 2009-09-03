import sys
from pkg_resources import resource_filename
sys.path.append(".")

from uf import hAtom

def test_valid_hatom():
    parser = hAtom()
    with open(resource_filename("uf", "examples/hatom.html"), "r") as f:
        atom = parser.parse(f)
