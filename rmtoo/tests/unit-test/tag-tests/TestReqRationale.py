#
# rmtoo
#   Free and Open Source Requirements Management Tool
#
# Unit test for ReqRationale
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

from rmtoo.modules.ReqRationale import ReqRationale
from rmtoo.lib.Requirement import Requirement
from rmtoo.lib.RMTException import RMTException
from rmtoo.tests.lib.ReqTag import create_parameters
from rmtoo.lib.storagebackend.RecordEntry import RecordEntry

class TestReqRationale:

    def test_positive_01(self):
        "Requirement Tag Rationale - no tag given"
        opts, config, req = create_parameters()

        rt = ReqRationale(opts, config)
        name, value = rt.rewrite("Rationale-test", req)
        assert(name=="Rationale")
        assert(value==None)

    def test_positive_02(self):
        "Requirement Tag Rationale - Rationale set"
        opts, config, req = create_parameters()
        req = {"Rationale": RecordEntry("Rationale", "something")}

        rt = ReqRationale(opts, config)
        name, value = rt.rewrite("Rationale-test", req)
        assert(name=="Rationale")
        assert(value=="something")

