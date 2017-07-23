import unittest
import JMeterInstaller


class JMeterInstallerTests(unittest.TestCase):

    def test_install(self):
        jmi = JMeterInstaller.JMeterInstaller()
        res = jmi.install()
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
