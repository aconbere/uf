"""
Microformat parsing library using lxml, vobject, and knowing good xsl transforms to create python object representations of microformats.

supported formats
=================
 * hAtom
 * hCard
 * hCal
 * xfn
 * rel="tag"

Example usage:
==============
    import uf
    f = open("http://mysite.com/myprofile")
    p = uf.hCard()
    hCard = p.parse(f)

Dependancies:
=============
 * lxml - http://codespeak.net/lxml/
 * vobject - http://vobject.skyhouseconsulting.com/
 * feedparser - http://feedparser.org/
 * openanything - http://diveintopython.org/download/diveintopython-examples-5.4.zip

known bugs
==========

Well I don't handle multiple hCards or hCals right now, essentially it relies on
the implimentor to hand it an html fragment. The code is there right now to open
file streams, but it just needs a little lxml.html or beautiful soup love to parse
out the list of fragments.

"""

from parser import hCard, hCal, hAtom, XFN, RelTag
