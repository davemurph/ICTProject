import unittest
from _tests.HTMLTestRunner import HTMLTestRunner
from _tests.testcases import TestClientWithUser, TestClientFunctions, TestRoutes


suite1 = unittest.TestLoader().loadTestsFromTestCase(TestClientWithUser)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestClientFunctions)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestRoutes)

all_tests = unittest.TestSuite([suite1, suite2, suite3])

# method to run test suite using unittest's TextTestRunner
'''unittest.TextTestRunner(verbosity=2).run(all_tests)'''

outfile = open('C:\Users\Daithi\Documents\ICTProject\TestResults\CurrClientReport.html', 'w')
runner = HTMLTestRunner(stream = outfile,
						title = 'Currency Converter Client Testing',
						verbosity = 2,
						description = 'Currency Converter Client - Unit test results')

runner.run(all_tests)