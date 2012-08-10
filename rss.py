#!/usr/local/bin/python
from xml.dom.minidom import parse
import os

def update_rss(rss_obj, fd, params):
    '''takes params and obj, updates obj with params'''
    subject_tag = rss_xml.getElementsByTagName('subject').firstChild
    subject_tag.data = params['subject']

    body_tag = rss_xml.getElementsByTagName('body').firstChild
    body_tag.data = params['body']

    seq_num_tag = rss_xml.getElementsByTagName('sequence_number').firstChild
    seq_num = int(seq_num_tag.data)
    seq_num += 1
    seq_num_tag.data = str(seq_num)

    date_tag = rss_xml.getElementsByTagName('date').firstChild
    date_tag.data = params['date']

    if params['verbose']:
        print 'modified rss file:\n{}'.format(rss_obj.toxml())

    rss_obj.writexml(fd)

def make_rss(params):
    '''takes a dict of params, and remakes the rss file if appropriate'''
    if not os.path.exists(params['location']):
        try:
            open(params['location'], 'w')
            make_rss(params)
        except Exception, err:
            print 'error: {0}\n\t{1}'.format(Exception, err)
    else:
        with open(params['location'], 'w+r') as fd:
            rss_xml = parse(fd)
            if params['verbose']:
                print 'existing rss file:\n{}'.format(rss_xml.toxml()) #debug
            current_subject = str(
                rss_xml.getElementsByTagName('subject').firstChild.data)
            current_body = str(
                rss_xml.getElementsByTagName('body').firstChild.data)
            if current_subject is params['subject'] and \
                current_body is not params['body']:
                update_rss(rss_obj, fd, params)
