# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 noet ai:
# A simple feed list page generator for rawdog
# Copyright Pascal Bleser 2010, based on rawdog_rss by Jonathan Riddell
# May be copied only under the terms of the GNU GPL version 2 or later

import os, time, cgi, re
from StringIO import StringIO
import rawdoglib.plugins, rawdoglib.rawdog
from rawdoglib.rawdog import string_to_html, fill_template, load_file

from time import gmtime, strftime

columns = 3

class Feed_List:
    def __init__(self, rawdog, config):
        if config['defines'].has_key('outputfeedlist'):
            self.out_file = config['defines']['outputfeedlist']
        else:
            self.out_file = 'feedlist.html'

    def output_write(self, rawdog, config, articles):
		# prep map
		feedmap = {}
		feedbyname = {}
		for feed in config["feedslist"]:
			item = {}
			url = feed[0]
			name = feed[2]['define_name']
			item['name'] = name
			if 'define_irc' in feed[2]:
				item['irc'] = feed[2]['define_irc']
			if 'define_face' in feed[2]:
				item['face'] = feed[2]['define_face']
			item['feeds'] = []
			feedmap[url] = item
			if not name in feedbyname:
				feedbyname[name] = item
			pass

		#feeds = rawdog.feeds.values()
		#feeds.sort(lambda a, b: cmp(a.get_blog_owner_name(config).lower(), b.get_blog_owner_name(config).lower()))

		for feed in rawdog.feeds.values():
			itembits = {}
			itembits['url'] = cgi.escape(feed.url)
			itembits['title'] = feed.get_html_name(config) #feed_info['title_detail']
			if 'link' in feed.feed_info:
				link = feed.feed_info['link']
				lm = re.match(r'^(http://lizards\.opensuse\.org)/?$', link)
				if lm:
					link = lm.group(1)
					# fix lizards link
					m = re.match(r'^http://lizards\.opensuse\.org(/author/.+?)/feed', feed.url)
					if m:
						link += m.group(1)
					else:
						link = None
					pass
			else:
				#print "WARNING: no link in " + feed.url
				link = None
				if re.match(r'^https?://.+', itembits['title']):
					del itembits['title']
				pass
			if link:
				itembits['link'] = link

			name = feed.args['define_name']
			itembits['author'] = name

			if name in feedbyname:
				feedbyname[name]['feeds'].append(itembits)
			else:
				print "WARNING: no name match found in feedbyname for "+name

			pass

		all_names = feedbyname.keys()
		all_names.sort()
		feed_template = load_file("feedlist_feed_template")
		author_template = load_file("feedlist_author_template")
		author_f = StringIO()
		i = 0
		for name in all_names:
			data = feedbyname[name]
			feed_f = StringIO()
			feed_vars = {}
			for k in filter(lambda x: x != 'feeds', data.keys()):
				feed_vars[k] = data[k]
			for feed in data['feeds']:
				for k, v in feed.iteritems():
					feed_vars[k] = v
				feed_f.write(fill_template(feed_template, feed_vars))
			
			author_vars = data
			if i % columns == 0:
				author_vars['wrap'] = True
			if i < columns:
				author_vars['top'] = True
			#elif 'wrap' in author_vars:
			#	del author_vars['wrap']
			i += 1
			feed_f.flush()
			author_vars['feeds'] = feed_f.getvalue()
			feed_f.close()
			author_f.write(fill_template(author_template, author_vars))

		feedlist_template = load_file("feedlist_template")
		f = open(self.out_file, "w")
		feedlist_vars = {}
		author_f.flush()
		feedlist_vars['feeds'] = author_f.getvalue()
		author_f.close()
		f.write(fill_template(feedlist_template, feedlist_vars))
		f.close()
		return True

def startup(rawdog, config):
	feed_list = Feed_List(rawdog, config)
	rawdoglib.plugins.attach_hook("output_write", feed_list.output_write)
	return True
rawdoglib.plugins.attach_hook("startup", startup)
