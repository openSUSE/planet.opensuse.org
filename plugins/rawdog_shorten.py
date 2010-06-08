# -*- coding: utf-8 -*-

import utils
import rawdoglib.plugins, rawdoglib.rawdog

class Shorten:
    def __init__(self, rawdog, config):
        pass

    def alter_post(self, box, title, link):
        html = box.value
        sh = utils.truncate_html_words(html, 100, '<span class="readmore">&hellip;</span>')
        if len(sh) < len(html):
            sh += "\n<div class=\"readmore\"><a href=\"%s\" class=\"readmore\">read more</a></div>" % link
            box.value = sh
            pass
        return True

def startup(rawdog, config):
    plugin = Shorten(rawdog, config)
    rawdoglib.plugins.attach_hook("alter_post", plugin.alter_post)
    return True

rawdoglib.plugins.attach_hook("startup", startup)
