# -*- coding: utf-8 -*-

# For testing processors, we have to add the _lib directory to the system path
# before they'll import.
import os, sys
sys.path.append(os.path.join(os.pardir, os.pardir, "_lib"))

# Create a test suite and run it.
# XXX: We could use nose here, and indeed one could easily run nosetests on the
# tests directory. This lets us reduce our list of requirements, and it's only
# four lines, and yes, I'm insecure about not using simpler discovery like nose!
import unittest
if __name__ == "__main__":
    suite = unittest.TestLoader().discover('.', pattern = "test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite)

