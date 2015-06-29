import xml.etree.ElementTree as etree
import bz2
from pypwikt.page import Page

__author__ = 'marigs'


def pages_from_xml_txt(xml_filename):
    f = open(xml_filename)
    for x in _pages_from_xml(f):
        yield x


def pages_from_xml_bz2(xml_filename, config):
    f = bz2.BZ2File(xml_filename, 'r')
    for x in _pages_from_xml(f, config):
        yield x


def _pages_from_xml(xml_file, config):
    for event, elem in etree.iterparse(xml_file, events=('start-ns', 'start', 'end')):
        #print event, elem
        if event == 'start-ns':
            ns, url = elem
            if not ns:
                ns_url = '{' + url + '}'
        if event == 'end' and elem.tag == ns_url + 'page':
            title = unicode(elem.find(ns_url + 'title').text)
            if not ':' in title and title != 'Main Page':
                rev_id = unicode(elem.find(ns_url + 'revision').find(ns_url+'id').text)
                rev_ts = unicode(elem.find(ns_url + 'revision').find(ns_url+'timestamp').text)
                text = unicode(elem.find(ns_url + 'revision').find(ns_url+'text').text)
                page = config.get_class_page()(title, rev_id, rev_ts, text)
                yield page
            elem.clear()
