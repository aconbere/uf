import sys
sys.path.append(".")

from uf.parser import Parser

def test_parser():
    parser = Parser()
    assert(parser)

def test_parser_open_stream():
    parser = Parser()
    stream = parser._open_stream("string")
    assert(stream == "string")

def test_parser_parse():
    parser = Parser()
    stream = "string"
    parsed_stream = parser.parse(stream)
    assert(parsed_stream == stream)
