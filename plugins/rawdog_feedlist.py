# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 noet ai:
# A simple feed list page generator for rawdog
# Copyright Pascal Bleser 2010, based on rawdog_rss by Jonathan Riddell
# May be copied only under the terms of the GNU GPL version 2 or later

import os, time, cgi, re
from StringIO import StringIO
import rawdoglib.plugins, rawdoglib.rawdog
from rawdoglib.rawdog import string_to_html, fill_template, load_file, encode_references
import codecs

from time import gmtime, strftime

columns = 3

class Feed_List:
    def __init__(self, rawdog, config):
        if config['defines'].has_key('outputfeedlist'):
            self.out_file = config['defines']['outputfeedlist']
        else:
            self.out_file = 'feedlist.html'

    def output_write(self, rawdog, config, articles):
		if config.no_feed_list:
			return True
		# prep map
		feedmap = {}
		feedbyname = {}
		for feed in config["feedslist"]:
			item = {}
			url = feed[0]
			name = feed[2]['define_name']
			item['name'] = name.encode('utf8')
			for d in (config['feeddefaults'], feed[2]):
				for k in filter(lambda x: x.startswith('define_'), d.iterkeys()):
					nk = re.sub(r'^define_', '', k)
					item[nk] = d[k]
					pass
				pass
			if 'face' in item:
				if not '.' in item['face']:
					item['face'] += '.png'
				if not '/' in item['face']:
					item['face'] = '../hackergotchi/' + item['face']

			item['feeds'] = []
			feedmap[url] = item
			if not name in feedbyname:
				feedbyname[name] = item
			pass

		#feeds = rawdog.feeds.values()
		#feeds.sort(lambda a, b: cmp(a.get_blog_owner_name(config).lower(), b.get_blog_owner_name(config).lower()))

		for feed in rawdog.feeds.values():
			itembits = {}
			itembits['lang'] = feed.lang
			for d in ('member', 'connect', 'gsoc'):
				if 'define_'+d in feed.args:
					itembits[d] = feed.args['define_'+d]

			itembits['url'] = cgi.escape(feed.url)
			title = feed.get_html_name(config)
			lizards_match = re.match(ur'^openSUSE\s+Lizards\s+\S+\s+(.+)$', title)
			if lizards_match:
				title = '@Lizards'
			itembits['title'] = title
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

		map = []

		i = 0
		for name in all_names:
			data = feedbyname[name]

			if config.lang:
				feeds = filter(lambda x: x['lang'] == config.lang, data['feeds'])
			else:
				feeds = data['feeds']
			if len(feeds) < 1:
				continue

			author = {}
			for k in filter(lambda x: x != 'feeds', data.keys()):
				author[k] = data[k]
				pass
			if i % columns == 0:
				author['wrap'] = True
			if i < columns:
				author['top'] = True

			i += 1
			author['feeds'] = []

			#for k in filter(lambda x: x != 'feeds', data.keys()):
			#	feed[k] = data[k]
			for feed in feeds:
				author['feeds'].append(feed)

			map.append(author)

		feedlist_template = load_file("feedlist_template.html", config)
		f = codecs.open(self.out_file, "wb", encoding="utf8")
		feedlist_vars = {}
		if config.lang:
			feedlist_vars['lang'] = config.lang
			feedlist_vars['lang_'+config.lang] = True
		feedlist_vars['feeds'] = map
		f.write(fill_template(feedlist_template, feedlist_vars))
		f.close()
		return True

def startup(rawdog, config):
	plugin = Feed_List(rawdog, config)
	rawdoglib.plugins.attach_hook("output_write", plugin.output_write)
	return True
rawdoglib.plugins.attach_hook("startup", startup)
