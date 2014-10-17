# mods is the list of mods you want to test
# mcVersions is the NEM list you want to test the mods on

mods = ["MinecraftForge", "ChickenChunks", "EnderStorage"]
mcVersions = ["1.6.4", "1.7.2", "1.7.10", "1.8"]


# Stuff bellow is to make all web requests cached.
# Most of it is "stolen" from NotEnoughMods_Tools.py and NotEnoughMods_Polling.py
import traceback
import gzip
import os
from StringIO import StringIO
from string import ascii_letters, digits
from commands.NEMP import NEMP_Class


def cached_fetch_page(self, url, decompress=True, timeout=10):
    self.cacheDir = os.path.join("nemcache")
    try:
        fname = normalize_filename(url)
        filepath = os.path.join(self.cacheDir, fname)

        if os.path.exists(filepath):
            print "Loading from cache,",filepath
            with open(filepath, "r") as f:
                return f.read()

        response = self.useragent.open(url, timeout=timeout)
        if response.info().get('Content-Encoding') == 'gzip' and decompress:
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf, mode='rb')
            data = f.read()
        else:
            data = response.read()


        print "Writing to cache,",filepath
        with open(filepath, "w") as f:
            f.write(data)

        return data
    except:
        traceback.print_exc()
        pass
        # most likely a timeout


def normalize_filename(name):
    return ''.join(c for c in name if c in "-_.() %s%s" % (ascii_letters, digits))


NEMP_Class.NotEnoughClasses.fetch_page = cached_fetch_page

NEM = NEMP_Class.NotEnoughClasses()

for mod in mods:
    # print getattr(NEM, NEM.mods[mod]["function"])(mod)
    try:
        result = getattr(NEM, NEM.mods[mod]["function"])(mod)
        real_name = NEM.mods[mod].get('name', mod)
        version = result['mc']

        print "\n" "<--------------------------->"
        print(mod + ": {}".format(result))

        if not result:
            print("Didn't get a reply from the parser. (got " + repr(result) + ")")
            break

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