# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 noet ai:
# XXX
# Copyright Pascal Bleser 2010, based on rawdog_rss by Jonathan Riddell
# May be copied only under the terms of the GNU GPL version 2 or later

import os, time, cgi, re
from StringIO import StringIO
import rawdoglib.plugins, rawdoglib.rawdog
from rawdoglib.rawdog import string_to_html, fill_template, load_file

from time import gmtime, strftime

import sys
from pprint import pprint

class Overview:
	def __init__(self, rawdog, config):
		self.items = []
		self.template = load_file("overview_template")
		self.item_template = load_file("overview_item_template")
		pass

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
		for item in self.items:
			i += 1
			item['i'] = str(i)
			fi.write(fill_template(self.item_template, item))
		fi.flush()
		if 'i' in bits:
			del bits['i']
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
	rawdoglib.plugins.attach_hook("output_item_bits", plugin.output_item_bits)
	rawdoglib.plugins.attach_hook("output_bits", plugin.output_bits)
	return True
rawdoglib.plugins.attach_hook("startup", startup)
