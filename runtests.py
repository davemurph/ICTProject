import unittest
import _tests.HTMLTestRunner
from _tests.testcases_flask_testing import TestClientWithUser, TestClientFunctions, TestRoutes


suite1 = unittest.TestLoader().loadTestsFromTestCase(TestClientWithUser)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestClientFunctions)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestRoutes)


all_tests = unittest.TestSuite([suite1, suite2, suite3])

'''unittest.TextTestRunner(verbosity=2).run(all_tests)'''

outfile = open('C:\Users\Daithi\Documents\ICTProject\TestResults\Report.html', 'w')
runner = _tests.HTMLTestRunner.HTMLTestRunner(
				stream = outfile,
				title = 'Currency Converter Client Testing',
				verbosity = 2,
				description = 'Currency Converter Client - Unit test results')

runner.run(all_tests)