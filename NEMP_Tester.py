# Config options
mods = ["ChickenChunks", "EnderTech-Drayshak", "Veinminer", "WarpBook"]  # A list of mods to test
caching = True  # Setting this to True rewrites the fetch_page function of NEMP_Class to cache web requests


# Stuff bellow is to make all web requests cached.
# Most of it is "stolen" from the NotEnoughMods_Tools.py
# and NotEnoughMods_Polling.py files in the NotEnoughMods repo
import traceback
import codecs
import os
import json
from string import ascii_letters, digits
from commands.NEMP import NEMP_Class


def cached_fetch_page(self, url, timeout=10, decode_json=False):
    self.cacheDir = os.path.join("nemcache")
    try:
        fname = normalize_filename(url)
        filepath = os.path.join(self.cacheDir, fname)

        if os.path.exists(filepath):
            print "Loading from cache,",filepath
            with codecs.open(filepath, encoding='utf-8', mode='r') as f:
                if decode_json:
                    return json.loads(f.read())
                else:
                    return f.read()

        request = self.requests_session.get(url, timeout=timeout)

        print "Writing to cache,",filepath
        with codecs.open(filepath, encoding='utf-8', mode='w') as f:
            if decode_json:
                f.write(request.text)
                return request.json()
            else:
                f.write(request.text)
                return request.text

    except:
        traceback.print_exc()
        pass
        # most likely a timeout


def normalize_filename(name):
    return ''.join(c for c in name if c in "-_.() %s%s" % (ascii_letters, digits))


if caching:
    NEMP_Class.NotEnoughClasses.fetch_page = cached_fetch_page

NEM = NEMP_Class.NotEnoughClasses()

for mod in mods:
    try:
        result = getattr(NEM, NEM.mods[mod]["function"])(mod)
        real_name = NEM.mods[mod].get('name', mod)

        if 'mc' in result:
            version = result['mc']
        else:
            version = NEM.mods[mod]["mc"]

        print "\n" "<--------------------------->"

        if not result:
            print(mod + "Didn't get a reply from the parser. (got " + repr(result) + ")")
            print "<--------------------------->" "\n"
            break

        print(mod + ": {}".format(result))

        if "mc" in result:
            if version != result["mc"]:
                print("Expected MC version {}, got {}".format(version, result["mc"]))
        else:
            print("Did not receive MC version from parser.")
        if "version" in result:
            print("!lmod {0} {1} {2}".format(version, real_name, unicode(result["version"])))
        if "dev" in result:
            print("!ldev {0} {1} {2}".format(version, real_name, unicode(result["dev"])))
        if "change" in result:
            print(" * " + result["change"])
        print "<--------------------------->" "\n"
    except Exception as error:
        print "\n" "<--------------------------->"
        print(mod + ": " + str(error))
        print(mod + " failed to be polled")
        print "<--------------------------->" "\n"