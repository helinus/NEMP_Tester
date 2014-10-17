# mods is the list of mods you want to test
# mcVersions is the NEM list you want to test the mods on

mod = "ChickenChunks"
mcVersions = ["1.6.4", "1.7.2", "1.7.10", "1.8"]


# Stuff to make it not tax NEM too much.
import traceback
import gzip
import os
from StringIO import StringIO
from time import time
from string import ascii_letters, digits
from commands.NEMP import NEMP_Class

# "stolen" from NotEnoughMods_Tools.py
def cached_fetch_page(self, url, decompress=True, timeout=10, cache=True):
    self.cacheDir = os.path.join("nemcache")
    self.cache_FileLastUpdated = {}
    self.cache_period = 24 * 60 * 60  # once per day
    try:
        fname = normalize_filename(url)
        filepath = os.path.join(self.cacheDir, fname)

        if cache == True:
            if fname in self.cache_FileLastUpdated:
                lastUpdated = self.cache_FileLastUpdated[fname]

                if time() - lastUpdated > self.cache_period:
                    pass
                else:
                    # print "Loading from cache,",filepath
                    with open(filepath, "r") as f:
                        return f.read()
            else:
                if os.path.exists(filepath):
                    # print "Loading from cache,",filepath
                    self.cache_FileLastUpdated[fname] = time()

                    with open(filepath, "r") as f:
                        return f.read()

        response = self.useragent.open(url, timeout=timeout)
        if response.info().get('Content-Encoding') == 'gzip' and decompress:
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf, mode='rb')
            data = f.read()
        else:
            data = response.read()

        if cache == True:
            # print "Writing to cache,",filepath
            with open(filepath, "w") as f:
                f.write(data)
            self.cache_FileLastUpdated[fname] = time()

        return data
    except:
        traceback.print_exc()
        pass
        # most likely a timeout
def normalize_filename(name):
    return ''.join(c for c in name if c in "-_.() %s%s" % (ascii_letters, digits))

NEMP_Class.NotEnoughClasses.fetch_page = cached_fetch_page

NEM = NEMP_Class.NotEnoughClasses()

print getattr(NEM, NEM.mods[mod]["function"])(mod)