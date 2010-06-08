# vim: sw=4 ts=4 noet ai:
# -*- coding: utf-8 -*-

import utils
import rawdoglib.plugins, rawdoglib.rawdog

class Shorten:
    def __init__(self, rawdog, config):
        pass

    def alter_post(self, box, title, link):
        html = box.value
        if html != None:
            sh = utils.truncate_html_words(html, 500, '<span class="readmore">&hellip;</span>')
            if sh != None and len(sh) < len(html):
                readmore = rawdoglib.rawdog.translations.gettext('read more').decode("utf8")
                sh += "\n<div class=\"readmore\"><a href=\"%s\" class=\"readmore\">%s</a></div>" % (link, readmore)
                box.value = sh
                pass
            pass
        return True

def startup(rawdog, config):
    plugin = Shorten(rawdog, config)
    rawdoglib.plugins.attach_hook("alter_post", plugin.alter_post)
    return True

rawdoglib.plugins.attach_hook("startup", startup)
