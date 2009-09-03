from lxml import etree
from BeautifulSoup import BeautifulSoup
import filters
import vobject
import sys
import os
from pkg_resources import resource_filename

class Parser(object):
    filters = []
    def _open_stream(self, source):
        """
        _open_stream takes either a string or a file like object, and returns the body
        of that input. (a string)
        """
        if hasattr(source, 'read'):
            stream = source.read()
        else:
            if isinstance(source, unicode):
                stream = source.encode('utf-8')
            elif isinstance(source, str):
                stream = source
            else:
                stream = str(source)
        return stream

    def parse(self, stream):
        """
        Parse takes a stream, in this case either a string or a file like object
        (anything that impliments a read function), this could be a url opened with
        urllib, or an opened file.
        """
        return self.run_filters(self._open_stream(stream))

    def add_filter(self, filter):
        self.filters.append(filter)

    def run_filters(self, input):
        def _run_filters(filters, input):
            while filters:
                filter = filters.pop()
                return _run_filters(filters, filter(input)) 
            return input
        return _run_filters(self.filters, input)

class XHTMLParser(Parser):
    xsl_file = ""
    root_element = ""
    
    def __init__(self):
        self.add_filter(self._transform())
        self.add_filter(self._serialize())

    def _serialize(self):
        """
        The serialize filter takes a stream and returns an etree representation of that xml
        """
        def xml_filter(stream):
            return etree.HTML(self._open_stream(stream))
        return xml_filter

    def _transform(self):
        """
        Transfroms the xml representation of a microformat into a more suitable format via xsl
        In most cases this will be converting it into the format that the microformat
        derives from.
        
        Example.
            hCal is an implimentation of vCal, the transform here turns an xmlized
            hCal into a properly formed vCal
        """
        def xsl_filter(xml_etree):
            xsl = etree.parse(self.xsl_file)
            transform = etree.XSLT(xsl)
            return transform(xml_etree)
        return xsl_filter

    def _cut_xml(self):
        """
        This is a yet to be implimented filter that should take an xml representation (etree)
        of the html data, and then cut it into a list of the fragments it will be parsing.
        
        Example.
            A single html document might include many hCards, this filter will take the
            xmlized form of that document and return a list of those hCards as xml fragments
        
        This should go /before/ the _transform filter but /after/ the serialize
        """
        def xpath_filter(xml_etree):
            xpath = "//*[contains(@class,'%s')]" % (self.root_element,)
            return xml_etree.xpath(xpath)
        return xpath_filter

class vObjParser(XHTMLParser):
    """
    The vObjParser is used to convert XHTML to vObjects
    """
    def __init__(self):
        self.add_filter(filters.to_vobject)
        self.add_filter(filters.to_str)
        super(vObjParser, self).__init__()

class hCard(vObjParser):
    """
    Parses hCards in vCards in vObject
    """
    root_element = "vcard"
    xsl_file = resource_filename("uf", "xsl/xhtml2vcard.xsl")

class hCal(vObjParser):
    """
    Parses hCals into vCals in vObject
    """
    root_element = "vcal"
    xsl_file = resource_filename("uf", "xsl/xhtml2vcal.xsl")

class hAtom(XHTMLParser):
    """
    Parses hAtoms into Atoms in feedparser
    """
    root_element = "hentry"
    xsl_file = resource_filename("uf", "xsl/hAtom2Atom.xsl")

    def __init__(self):
        self.add_filter(filters.atom2python)
        self.add_filter(filters.to_str)
        super(hAtom, self).__init__()

class LinkParser(Parser):
    """
    LinkParsers uses the rel attribute to assign meta data to the urls.
    This is the parent class of XFNParser and RelTagParser
    
    Right now this only handles 'a' tags, to obey the spec it should
    be able to grab either 'a' or 'link' tags.
    """
    properties = set()

    def __init__(self):
        self.add_filter(self._retrieve_links())
        self.add_filter(self._transform())

    # it would be nice to be able to send in a Beautiful SoupStrainer
    # so we don't parse the whole page everytime
    
    def _transform(self):
        def soup_filter(stream):
            return BeautifulSoup(stream)
        return soup_filter

    def attr_filter(self, prop):
        """
        a factory for creating attribute filters.
        Used to figure out if a tag has particular attribute values.
        """
                    
        return lambda attr: attr is not None\
            and prop in attr.split(' ')

    def attr_not_empty_filter(self):
        """
        a factory for creating a filter to test
        if an element has a particular arrtibute
        """
        return lambda attr: attr is not None\
            and attr is not ""

    def get_links_with_property(self, soup, prop):
        """
        returns links with certain rel values
        """
        return soup.findAll('a', {'rel': self.attr_filter(prop), 'href': self.attr_not_empty_filter()})
    
    def _retrieve_links(self):
        """
        returns a dictionary where the keys are properties of the spec
        and the values are lists of urls that were founds for that.
        """
        def _parse_links_filter(soup):
            links = {}

            for prop in self.properties:
                retrieved_links = self.get_links_with_property(soup, prop)
                links[prop] = []
            
                for link in retrieved_links:
                    links[prop].append(link.get('href'))

                if links[prop] == []:
                    del links[prop]
            return links
        return _parse_links_filter

class XFN(LinkParser):
    """
    XFNParser is a link parser that looks for rel attributes in the list of
    approved propererties for xfn.
    """
    
    properties = set(['me', 'contact', 'acquaintance', 'friend',
                  'met', 'co-worker', 'colleague',
                  'co-resident', 'neighbor', 'child',
                  'parent', 'sibling', 'spouse', 'kin',
                  'muse', 'crush', 'date', 'sweatheart',
                  ])

    def get_rels_me(self):
        return get_links_with_property('me')

class RelTag(LinkParser):
    """
    Very simple extension of the LinkParser class, returns a list of urls that matched
    the rel="tag" attribute
    """
    
    properties = set(['tag'])
