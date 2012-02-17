# -*- coding: utf-8 -*-
# A simple RSS 2.0 generator for rawdog
# Copyright Jonathan Riddell 2008
# Modified by Pascal Bleser 2010 for Planet openSUSE
# May be copied only under the terms of the GNU GPL version 2 or later
#
# Writes RSS feed at the end of a rawdog run 
# Put in <configdir>/plugins/rawdog_rss.py
# Add "define outputxml /path/to/feed.rss" to config to set file out

import os, time, cgi, sys
import rawdoglib.plugins, rawdoglib.rawdog
import libxml2
import urllib
import locale

from time import gmtime, strftime

class RSS_Feed:
    def __init__(self, rawdog, config):
        self.write = False
        if config['defines'].has_key('outputxml'):
            self.out_file = config['defines']['outputxml']
        else:
            self.out_file = 'rss20.xml'
        self.doc_open()

        self.xml_articles = self.xml.xpathEval('/rss/channel')[0]

        self.xml_articles.newChild(None, 'title', "Planet openSUSE")

        if 'linksite' in config.config:
            link = config['linksite']
        else:
            link = 'http://planet.opensuse.org'
        self.xml_articles.newChild(None, 'link', link)
        if config.lang:
            self.xml_articles.newChild(None, 'language', config.lang)
        self.xml_articles.newChild(None, 'description', "Planet openSUSE - " + link)
        atomLink = self.xml_articles.newChild(None, 'atom:link', None)

        if 'linkxml' in config.config:
            href = config['linkxml']
        else:
            href = 'http://planet.opensuse.org/rss20.xml'
        atomLink.setProp('href', href)
        atomLink.setProp('rel', 'self')
        atomLink.setProp('type', 'application/rss+xml')

        if config['defines'].has_key('outputfoaf'):
            self.foaf_file = config['defines']['outputfoaf']
        else:
            self.foaf_file = 'foafroll.xml'

        self.foaf_articles = self.foafdoc_open()
        self.foaf_articles.newChild(None, 'foaf:name', "Planet openSUSE")
        self.foaf_articles.newChild(None, 'foaf:homepage', link)
        seeAlso = self.foaf_articles.newChild(None, 'rdfs:seeAlso', None)
        seeAlso.setProp('rdf:resource', '')

        if config['defines'].has_key('outputopml'):
            self.opml_file = config['defines']['outputopml']
        else:
            self.opml_file = 'opml.xml'

        self.opml_articles = self.opmldoc_open()

    def doc_open(self):
        self.doc = libxml2.newDoc("1.0")
        self.xml = self.doc.newChild(None, 'rss', None)

        self.xml.setProp('version', "2.0")            
        self.xml.setProp('xmlns:dc', "http://purl.org/dc/elements/1.1/")            
        self.xml.setProp('xmlns:atom', 'http://www.w3.org/2005/Atom')

        self.xml.newChild(None, 'channel', None)

    def foafdoc_open(self):
        self.foafdoc = libxml2.newDoc("1.0")
        self.foafxml = self.foafdoc.newChild(None, 'rdf:RDF', None)

        self.foafxml.setProp('xmlns:rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.foafxml.setProp('xmlns:rdfs', "http://www.w3.org/2000/01/rdf-schema#")
        self.foafxml.setProp('xmlns:foaf', "http://xmlns.com/foaf/0.1/")
        self.foafxml.setProp('xmlns:rss', "http://purl.org/rss/1.0/")
        self.foafxml.setProp('xmlns:dc', "http://purl.org/dc/elements/1.1/")

        return self.foafxml.newChild(None, 'foaf:Group', None)

    def opmldoc_open(self):
        self.opmldoc = libxml2.newDoc("1.0")
        self.opmlxml = self.opmldoc.newChild(None, 'opml', None)
        self.opmlxml.setProp('version', "1.1")

        head = self.opmlxml.newChild(None, 'head', None)
        head.newChild(None, 'title', "Planet openSUSE")
        head.newChild(None, 'dateCreated', strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + " +0000")
        head.newChild(None, 'dateModified', strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + " +0000")        
        head.newChild(None, 'ownerName', "openSUSE Admins")
        head.newChild(None, 'ownerEmail', "admin@opensuse.org")

        return self.opmlxml.newChild(None, 'body', None)

    def describe(self, parent, description):
        try:
            parent.newChild(None, 'description', description)
        except TypeError:
            print "TypeError in description"

    def __article_sync(self, xml_article, rawdog, config, article):
        entry_info = article.entry_info
	guid = xml_article.newChild(None, 'guid', article.hash)
        guid.setProp('isPermaLink', 'false')
        if 'title' in entry_info:
            title = unicode(entry_info['title'].encode('utf8'), 'utf8') #, 'ignore')
        else:
            title = u'(no title)'
        for feed in config["feedslist"]:
            if feed[0] == article.feed:
                title = feed[2]["define_name"] + u": " + title
        xml_article.newChild(None, 'title', title.encode('utf8'))
        actual_locale = locale.getdefaultlocale()
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF8')
            date = strftime("%a, %d %b %Y %H:%M:%S", gmtime(article.date)) + " +0000"
        finally:
            locale.setlocale(locale.LC_TIME, actual_locale)
            pass
        xml_article.newChild(None, 'pubDate', date)
        if entry_info.has_key('link'):
            try:
                xml_article.newChild(None, 'link', entry_info['link'])
            except UnicodeEncodeError:
                pass

        if entry_info.has_key('content'):
            for content in entry_info['content']:
                content = content['value']
        elif entry_info.has_key('summary_detail'):
            content = entry_info['summary_detail']['value']
        else:
            content = ""
        content = cgi.escape(content).encode('utf8', 'ignore')
        self.describe(xml_article, content)

        return True

    def __write(self):
        self.doc.saveFormatFile(self.out_file, 1)
        self.doc.freeDoc()

    def output_write(self, rawdog, config, articles):
        self.write = True
        for article in articles:
            if article.date is not None:
                article_feed = rawdog.feeds[article.feed]
                if config.lang and article_feed.lang != config.lang:
                    continue
                xml_article = self.xml_articles.newChild(None, 'item', None)
                self.__article_sync(xml_article, rawdog, config, article)

        self.__write()
        return True

    def shutdown(self, rawdog, config):
        if not self.write:
            return True

        for feed in config["feedslist"]:
            member = self.foaf_articles.newChild(None, 'foaf:member', None)
            agent = member.newChild(None, 'foaf:Agent', None)
            agent.newChild(None, 'foaf:name', feed[2]['define_name'].encode('utf8'))
            weblog = agent.newChild(None, 'foaf:weblog', None)
            document = weblog.newChild(None, 'foaf:Document', None)
            document.setProp('rdf:about', feed[0])
            seealso = document.newChild(None, 'rdfs:seeAlso', None)
            channel = seealso.newChild(None, 'rss:channel', None)
            channel.setProp('rdf:about', '')

            outline = self.opml_articles.newChild(None, 'outline', None)
            outline.setProp('text', feed[2]['define_name'].encode('utf8'))
            outline.setProp('xmlUrl', feed[0])

        self.foafdoc.saveFormatFile(self.foaf_file, 1)
        self.foafdoc.freeDoc()

        self.opmldoc.saveFormatFile(self.opml_file, 1)
        self.opmldoc.freeDoc()
        return True

def startup(rawdog, config):
    rss_feed = RSS_Feed(rawdog, config)
    rawdoglib.plugins.attach_hook("output_write", rss_feed.output_write)
    rawdoglib.plugins.attach_hook("shutdown", rss_feed.shutdown)
    return True

rawdoglib.plugins.attach_hook("startup", startup)
