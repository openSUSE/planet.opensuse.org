# upgrade_1_2: import state from rawdog 1.x state files to rawdog 2.x
# Copyright 2003, 2004, 2005 Adam Sampson <ats@offog.org>
#
# rawdog is free software; you can redistribute and/or modify it
# under the terms of that license as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# rawdog is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rawdog; see the file COPYING. If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA, or see http://www.gnu.org/.

import os, time, difflib
import cPickle as pickle
from rawdog import Rawdog
from persister import Persister

def format_time(secs):
	"""Turn a Unix time into a human-readable string."""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))

def approximately_equal(a, b):
	"""Return whether two strings are approximately equal."""
	if a == b:
		return True
	return difflib.get_close_matches(a, [b], 1, 0.6) != []

def upgrade(olddir, newdir):
	"""Given a rawdog 1.x state directory and a rawdog 2.x state directory,
	copy the ordering information from the old one into the new one. Since
	rawdog 2.0 mangles articles in a slightly different way, this needs to
	do approximate matching to find corresponding articles."""
	print "Importing state from " + olddir + " into " + newdir

	print "Loading old state"
	f = open(olddir + "/state")
	oldrawdog = pickle.load(f)

	print "Loading new state"
	os.chdir(newdir)
	persister = Persister("state", Rawdog)
	newrawdog = persister.load()

	print "Copying feed state"
	oldfeeds = {}
	newfeeds = {}
	for url, oldfeed in oldrawdog.feeds.items():
		if newrawdog.feeds.has_key(url):
			last_update = oldfeed.last_update
			print "Setting feed", url, "last update time to", format_time(last_update)
			newrawdog.feeds[url].last_update = last_update
			oldfeeds[url] = {}
			newfeeds[url] = {}
		else:
			print "Old feed", url, "not in new state"

	print "Copying article state"

	# Seperate out the articles by feed.
	for oldhash, oldarticle in oldrawdog.articles.items():
		if oldfeeds.has_key(oldarticle.feed):
			oldfeeds[oldarticle.feed][oldhash] = oldarticle
	for newhash, newarticle in newrawdog.articles.items():
		if newfeeds.has_key(newarticle.feed):
			newfeeds[newarticle.feed][newhash] = newarticle

	# Now fuzzily match articles.
	for url, oldarticles in oldfeeds.items():
		for newhash, newarticle in newfeeds[url].items():
			matches = []
			for oldhash, oldarticle in oldarticles.items():
				score = 0

				olink = oldarticle.link
				nlink = newarticle.entry_info.get("link")
				if olink is not None and nlink is not None and olink == nlink:
					score += 1

				otitle = oldarticle.title
				ntitle = newarticle.entry_info.get("title")
				if otitle is not None and ntitle is not None and approximately_equal(otitle, ntitle):
					score += 1

				odesc = oldarticle.description
				ndesc = newarticle.entry_info.get("description")
				if odesc is not None and ndesc is not None and approximately_equal(odesc, ndesc):
					score += 1

				matches.append((score, oldhash))

			matches.sort()
			if matches != [] and matches[-1][0] > 1:
				oldhash = matches[-1][1]
				oldarticle = oldarticles[oldhash]
				newarticle.sequence = oldarticle.sequence
				newarticle.last_seen = oldarticle.last_seen
				newarticle.added = oldarticle.added
				print "Matched new", newhash, "to old", oldhash, "in", url
			else:
				print "No match for", newhash, "in", url


	print "Saving new state"
	newrawdog.modified()
	persister.save()

	print "Done"

