import os
import sys
import hashlib
import urllib2
import tempfile
import zipfile
import distutils.core


class JMeterInstaller(object):

    def __init__(self):
        self.jmeter_version = "2.11"
        self.jmeter_dir = "apache-jmeter-%s/" % self.jmeter_version
        self.download_dir = tempfile.mkdtemp() + "/"
        self.hashes = {"jmeter.zip": "c7efb7d1e950caeb5a5720bf0b2445893ca8fe61",
                       "jmp-standard.zip": "5df124bc039a3cef291a3e9054110a1ff1ae8441",
                       "jmp-extras.zip": "1f6ac7c3200a5d9f42f55217bf0c287fdbba485c",
                       "jmp-extraslibs.zip": "1087fdf9506ecfed202bea7625a227f6bdc14918"}

    def clean(self):
        if os.path.exists(self.download_dir):
            print("Removing %s" % self.download_dir)
            distutils.dir_util.remove_tree(self.download_dir)

    def get_file(self, url, local_path):
        print("Downloading " + url)
        stream = urllib2.urlopen(url)
        with(open(self.download_dir + local_path, "wb")) as f:
            f.write(stream.read())

        with(open(f.name, "rb")) as written:
            hash = hashlib.sha1(written.read()).hexdigest()
            if self.hashes[local_path] != hash:
                self.clean()
                raise Exception("File hash mismatch. Expected %s but received %s" % (
                    self.hashes[local_path], hash))

    def unzip_plugin(self, zip_file, to_dir):
        out = self.jmeter_dir + to_dir
        with(zipfile.ZipFile(self.download_dir + zip_file, "r")) as z:
            z.extractall(out)
            distutils.dir_util.copy_tree(out + "/lib", self.jmeter_dir + "/lib")
            distutils.dir_util.remove_tree(out + "/lib")
        print("JMeter Plugin copied to JMeter lib directory. README for the plugin available at %s%s" % (
            self.jmeter_dir, to_dir))

    def install_jmeter(self):
        if not os.path.exists(self.jmeter_dir):
            print("Download JMeter")

            jmeter_file = "https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-%s.zip" % self.jmeter_version
            self.get_file(jmeter_file, "jmeter.zip")

            with(zipfile.ZipFile(self.download_dir + "jmeter.zip", "r")) as z:
                z.extractall()

            os.chmod(self.jmeter_dir + "/bin/jmeter.sh", 0755)
        else:
            print("JMeter directory [%s] exists... skipping" % self.jmeter_dir)

    def install_plugins(self):
        print("Installing JMeter Plugins")

        base_url = 'http://jmeter-plugins.org/downloads/file/'
        plugins = [['JMeterPlugins-Standard', '1.1.2', 'jmp-standard'],
                   ['JMeterPlugins-Extras', '1.1.2', 'jmp-extras'],
                   ['JMeterPlugins-ExtrasLibs', '1.1.2', 'jmp-extraslibs']]

        for plugin in plugins:
            if not os.path.exists(self.jmeter_dir + "lib/ext/" + plugin[0] + ".jar"):
                self.get_file(
                    base_url + plugin[0] + "-" + plugin[1] + ".zip", plugin[2] + ".zip")

                self.unzip_plugin(plugin[2] + ".zip", plugin[2])
            else:
                print("%s appear to exist in %slib/ext" %
                      (plugin[0], self.jmeter_dir))

    def install(self):
        try:
            self.install_jmeter()
            self.install_plugins()
            self.clean()
            return os.path.exists(self.jmeter_dir)
        except:
            self.clean()
            print "Unexpected error:", sys.exc_info()
            raise


if __name__ == '__main__':
    jmi = JMeterInstaller()
    res = jmi.install()
    print("Does jmeter install path %s exist? %s" % (jmi.jmeter_dir, res))
