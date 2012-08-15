#!/usr/local/bin/python
#from xml.dom.minidom import parse, parseString #changing to etree implementation
import xml.etree.ElementTree as etree
import os

#def update_rss(rss_xml, params)
def update_rss(tree, params):
    '''takes params and obj, updates obj with params'''
    with open(params['location'], 'w') as fd:
        #subject_node = get_node_by_id(rss_obj, 'subject', 'title')
        subject_node = tree.find('./channel/item/title')

        if params['verbose']:
            print 'subject_node: {}'.format(subject_node.text)

        subject_node = params['subject']

        #if subject_node.hasChildNodes():
        #    subject_tag = subject_node.firstChild
        #    subject_tag.data = params['subject']
        #else:
        #    subject_node.
        #    print 'no Node with id="subject" in xml file'

        #body_node = get_node_by_id(rss_obj, 'body', 'description')
        body_node = tree.find('./channel/item/description')

        if params['verbose']:
            print 'body_node: {}'.format(body_node.text)

        body_node.text = params['body']

        #if body_node != None:
        #    body_tag = body_node.firstChild
        #    body_tag.data = params['body']
        #else:
        #    print 'no Node with id="body" in xml file'

        sequence_number_node = tree.find('./channel/item/sequence_number')

        if params['verbose']:
            print 'sequence_number: {}'.format(sequence_number_node.text)

        if sequence_number_node.text != None:
            seq_num = int(sequence_number_node.text)
        else:
            seq_num = 0
        seq_num += 1
        sequence_number_node.text = str(seq_num)

        #try:
        #    seq_num_tag = rss_xml.getElementsByTagName('sequence_number')[0].firstChild
        #    seq_num = int(seq_num_tag.data)
        #    seq_num += 1
        #    seq_num_tag.data = str(seq_num)
        #except:
        #    print 'no "sequence_number" tag found in template.xml'

        date_node = tree.find('./channel/item/date')
        if params['verbose']:
             print 'date: {}'.format(date_node.text)

        date_node.text = params['date'][0]

        #try:
        #    date_tag = rss_xml.getElementsByTagName('date')[0].firstChild
        #    date_tag.data = params['date']
        #except:
        #    print 'no "date" tag found in template.xml'

        if params['verbose']:
            print 'modified rss file:\n{}'.format(etree.dump(tree))

        #rss_obj.writexml(fd)
        tree.write(params['location'])

#def get_node_by_id(xml, this_id, this_tag):
#    '''this method will retrieve a node based on id
#    assuming that the id is unique.'''
#    nodes = xml.getElementsByTagName(this_tag)
#    for node in nodes:
#        if 'id' in node.attributes.keys():
#            #print 'node.attributes["id"]: {0}\nthis_id: {1}\nthis_id==node.attributes["id"].value:{2}'.format(node.attributes['id'].value, this_id, (this_id == node.attributes["id"].value))
#            if (node.attributes['id'].value == this_id):
#                #print 'desired_node: {}'.format(node)        
#                return node
#    print 'no Node with id="{}" in xml'.format(this_id)
#    return None

def make_rss(params):
    '''takes a dict of params, and remakes the rss file if appropriate'''
    if not os.path.exists(params['location']):
        try:
            open(params['location'], 'w')
            make_rss(params)
        except Exception, err:
            print 'error: {0}\n\t{1}'.format(Exception, err)
    else:
        try:
            tree = etree.parse(params['location'])
        except:
            tree = etree.parse('template.xml')



        #with open(params['location'], 'r') as fd:
        #    try:
        #        rss_xml = parse(fd)
        #        if params['verbose']:
        #            print 'existing rss file:\n{}'.format(rss_xml.toxml()) #debug
        #            if params['verbose']:
        #                print 'rss_xml: {}'.format(rss_xml.toxml())
        #    except:
        #        with open('./template.xml','r') as fd2:
        #            rss_xml = parse(fd2)
        #            print 'existing rss file empty or not present.'
        #            if params['verbose']:
        #                print 'rss_xml: {} (from template)'.format(rss_xml.toxml())

        try:
            current_subject = tree.find('./channel/item/title')
        except:
            current_subject = ''

        try:
            current_body = tree.find('./channel/item/description')
        except:
            current_body = ''

        #try:
        #    current_subject = get_node_by_id(rss_xml, 'subject', 'title')
        #    print 'current_subject: {}'.format(current_subject)
        #    if current_subject.hasChildNodes():
        #        print 'current_subject: {}'.format(current_subject.firstChild.data)
        #        current_subject = current_subject.firstChild.data
        #    else:
        #        current_subject = ''
        #except:
        #    current_subject = ''
        #try:
        #    current_body = get_node_by_id(rss_xml, 'body', 'description')
        #    print 'current_body: {}'.format(current_body)
        #    if current_body.hasChildNodes:
        #        print 'current_body: {}'.format(current_body.firstChild.data)
        #        current_body = current_body.firstChild.data
        #except:
        #    current_body = ''

        if current_subject.text is not params['subject'] and \
            current_body.text is not params['body']:
            if params['verbose']:
                 print 'tree: {}'.format(etree.dump(tree))
                 #print 'rss_xml: {}'.format(rss_xml.toprettyxml())
            update_rss(tree, params)
            #update_rss(rss_xml, params)
