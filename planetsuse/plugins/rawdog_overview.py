# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 noet ai:
# Add overview block.
# Copyright Pascal Bleser 2010, based on rawdog_rss by Jonathan Riddell
# May be copied only under the terms of the GNU GPL version 2 or later

import os, time, cgi, re
from StringIO import StringIO
import rawdoglib.plugins, rawdoglib.rawdog
from rawdoglib.rawdog import string_to_html, fill_template, load_file

from time import gmtime, strftime

import sys
from pprint import pprint

DAY_CHANGE_KEY = '_day_change_'

def config_option(config, key, value):
	if key == "overview_dayformat":
		config[key] = value
		return False
	return True

class Overview:
	def __init__(self, rawdog, config):
		self.items = []
		self.template = load_file("overview_template")
		self.day_template = load_file("overview_day_template")
		self.item_template = load_file("overview_item_template")
		self.lasttime = None
		if 'overview_dayformat' in config.config:
			self.format = config['overview_dayformat']
		else:
			self.format = config['dayformat']
			pass
		pass

	def output_items_heading(self, rawdog, config, f, article, article_date):
		tm = time.localtime(article_date)
		if config["daysections"] and (self.lasttime == None or tm[:3] != self.lasttime[:3]):
			item = {}
			item[DAY_CHANGE_KEY] = True # hm, hack...
			item['day'] = time.strftime(self.format, tm)
			self.items.append(item)
			pass
		self.lasttime = tm
		return True

	def output_item_bits(self, rawdog, config, feed, article, itembits):
		item = {}
		for k in ('name', 'title_no_link'):
			item[k] = itembits[k]
			pass
		self.items.append(item)
		pass

	def output_bits(self, rawdog, config, bits):
		fi = StringIO()
		i = 0
		d = 0
		for item in self.items:
			if DAY_CHANGE_KEY in item:
				d += 1
				if d == 1: item['first'] = True
				item['i'] = str(d)
				fi.write(fill_template(self.day_template, item))
			else:
				i += 1
				item['i'] = str(i)
				fi.write(fill_template(self.item_template, item))
				pass
		fi.flush()
		bits['overview_items'] = fi.getvalue()
		fi.close()

		f = StringIO()
		f.write(fill_template(self.template, bits))
		f.flush()
		bits['overview'] = f.getvalue()
		f.close()

		self.items = []
		pass

	pass

def startup(rawdog, config):
	plugin = Overview(rawdog, config)
	#rawdoglib.plugins.attach_hook("config_option", plugin.config_option)
	rawdoglib.plugins.attach_hook("output_items_heading", plugin.output_items_heading)
	rawdoglib.plugins.attach_hook("output_item_bits", plugin.output_item_bits)
	rawdoglib.plugins.attach_hook("output_bits", plugin.output_bits)
	return True

rawdoglib.plugins.attach_hook("config_option", config_option)
rawdoglib.plugins.attach_hook("startup", startup)

