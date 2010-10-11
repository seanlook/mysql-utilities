#!/usr/bin/env python

import os
import replicate
from mysql.utilities.common import MySQLUtilError
from mysql.utilities.common import MUTException

class test(replicate.test):
    """check parameters for the replicate utility
    This test executes the replicate utility parameters. It uses the
    replicate test as a parent for setup and teardown methods.
    """

    def check_prerequisites(self):
        return replicate.test.check_prerequisites(self)

    def setup(self):
        return replicate.test.setup(self)

    def run(self):
        self.res_fname = self.testdir + "result.txt"
                      
        comment = "Test case 1 - use the test feature"
        res = self.run_test_case(self.server2, self.server1, self.s2_serverid,
                                 comment, "--test-db=db_not_there_yet", True)
        if not res:
            raise MUTException("%s: failed" % comment)

        try:
            res = self.server2.exec_query("STOP SLAVE")
        except:
            pass

        comment = "Test case 2 - show the help"
        res = self.run_test_case(self.server1, self.server2, self.s1_serverid,
                                 comment, "--help", True)
        if not res:
            raise MUTException("%s: failed" % comment)

        comment = "Test case 3 - use the verbose feature"
        res = self.run_test_case(self.server2, self.server1, self.s2_serverid,
                                 comment, " --verbose", True)
        if not res:
            raise MUTException("%s: failed" % comment)

        try:
            res = self.server2.exec_query("STOP SLAVE")
        except:
            pass
        
        self.remove_result("# status:")
        self.remove_result("# error: ")
        self.mask_result("# CHANGE MASTER TO MASTER_HOST",
                         "MASTER_LOG_POS = ", "MASTER_LOG_POST = XXXX")
        self.mask_result("# CHANGE MASTER TO MASTER_HOST",
                         "MASTER_PORT = ", "MASTER_PORT = XXXX")
        self.mask_result("# master id =", "= ", "= XXX")
        self.mask_result("#  slave id =", "= ", "= XXX")

        return True

    def get_result(self):
        return self.compare(__name__, self.results)
    
    def record(self):
        return self.save_result_file(__name__, self.results)
    
    def cleanup(self):
        return replicate.test.cleanup(self)


