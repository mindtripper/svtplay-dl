# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-

from __future__ import absolute_import
import json
import re
import copy

from svtplay_dl.service import Service, OpenGraphThumbMixin
from svtplay_dl.fetcher.http import HTTP
from svtplay_dl.error import ServiceError


class Sr(Service, OpenGraphThumbMixin):
    supported_domains = ['sverigesradio.se']

    def get(self):
        data = self.get_urldata()

        match = re.search(r'data-audio-id="(\d+)"', data)
        match2 = re.search(r'data-audio-type="(\w+)"', data)
        if match and match2:
            aid = match.group(1)
            type = match2.group(1)
        else:
            yield ServiceError("Can't find audio info")
            return

        dataurl = "https://sverigesradio.se/sida/playerajax/" \
                  "getaudiourl?id={0}&type={1}&quality=high&format=iis".format(aid, type)
        data = self.http.request("get", dataurl).text
        playerinfo = json.loads(data)
        yield HTTP(copy.copy(self.config), playerinfo["audioUrl"], 128, output=self.output)
