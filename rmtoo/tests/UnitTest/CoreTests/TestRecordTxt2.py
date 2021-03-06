'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Record Text Test Class: try to run through all the possible states
  and error scenarios.
   
 (c) 2010-2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

import unittest
import StringIO

from rmtoo.lib.storagebackend.txtfile.TxtRecord import TxtRecord
from rmtoo.lib.storagebackend.txtfile.TxtParser import TxtParser
from rmtoo.lib.storagebackend.txtfile.TxtIOConfig import TxtIOConfig
from rmtoo.lib.configuration.Cfg import Cfg
from rmtoo.lib.logging import init_logger, tear_down_log_handler
from rmtoo.tests.lib.Utils import hide_timestamp

comment_line = "===DATETIMESTAMP===;rmtoo;INFO;TxtParser;" \
"split_next_record;84; 80:CommentsEverywhere:%s:" + TxtParser.comment_in_req + "\n"

class TestRecordTxt2(unittest.TestCase):

    def test_pos_01(self):
        "TestRecordTxt2: empty input"

        txt_doc = TxtRecord.from_string("", "Nothing", TxtIOConfig())

        self.assertEqual(len(txt_doc), 0)
        assert(txt_doc.get_comment() == "")

    def test_neg_01(self):
        "TestRecordTxt2: rubbish in input"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)
        txt_doc = TxtRecord.from_string("rubbish", "Rubbish",
                                        TxtIOConfig())

        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtParser;" \
        "split_entries;125; 79:Rubbish:1:Expected tag line not found\n"
        self.assertEquals(result_expected, lstderr)

    def test_neg_02(self):
        "TestRecordTxt2: only ':'"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        txt_doc = TxtRecord.from_string(":", "Rubbish", TxtIOConfig())
        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtParser;" \
        "split_entries;125; 79:Rubbish:1:Expected tag line not found\n"
        self.assertEquals(result_expected, lstderr)

    def test_neg_03(self):
        "TestRecordTxt2: no chars before ':'"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        txt_doc = TxtRecord.from_string(": something", "Rubbish",
                                        TxtIOConfig())
        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtParser;" \
        "split_entries;125; 79:Rubbish:1:Expected tag line not found\n"
        self.assertEquals(result_expected, lstderr)

    def test_neg_04(self):
        "TestRecordTxt2: long long line"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        cfg = Cfg.new_by_json_str('{"max_input_line_length": 7}')

        tioconfig = TxtIOConfig(cfg)
        txt_doc = TxtRecord.from_string("good: but too long",
                                        "TooLong", tioconfig)

        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;" \
        "check_line_length;77; 80:TooLong:1:line too long: is [18], " \
        "max allowed [7]\n"
        self.assertEquals(result_expected, lstderr)

    def test_neg_05(self):
        "TestRecordTxt2: long long line - check for lineno"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        cfg = Cfg.new_by_json_str('{"max_input_line_length": 7}')
        tioconfig = TxtIOConfig(cfg)
        txt_doc = TxtRecord.from_string("""# com
ok: yes
 no
# cs
# dds
good: but too long
# dds

""",
                                        "TooLong", tioconfig)

        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;" \
        "check_line_length;77; 80:TooLong:6:line too long: is [18], " \
        "max allowed [7]\n"
        self.assertEquals(result_expected, lstderr)

    def test_neg_06(self):
        "TestRecordTxt2: long long line - check for multiple errors"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        cfg = Cfg.new_by_json_str('{"max_input_line_length": 7}')
        tioconfig = TxtIOConfig(cfg)
        txt_doc = TxtRecord.from_string("""#1 com
ok: yes
 no
#4 cs
#5 dds
good: but too long
#7 dds
#8 hi
also good: but too long
#10 gsst
 dhd
#12 dhdh 
d:
#14
""",
                                        "TooLong", tioconfig)

        self.assertEqual(txt_doc.is_usable(), False)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;" \
        "check_line_length;77; 80:TooLong:6:line too long: is [18], " \
        "max allowed [7]\n" \
        "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;check_line_length;77; 80:" \
        "TooLong:9:line too long: is [23], max allowed [7]\n" \
        "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;check_line_length;77; 80:" \
        "TooLong:10:line too long: is [8], max allowed [7]\n" \
        "===DATETIMESTAMP===;rmtoo;ERROR;TxtRecord;check_line_length;77; 80:" \
        "TooLong:12:line too long: is [9], max allowed [7]\n" \
        "===DATETIMESTAMP===;rmtoo;INFO;TxtParser;split_next_record;84; 80:" \
        "TooLong:11:Compatibility info: Comments will be reordered when " \
        "they are re-written with rmtoo-tools. Please consult " \
        "rmtoo-req-format(5) or rmtoo-topic-format(5)\n"
        
        self.assertEquals(result_expected, lstderr)

    def test_neg_07(self):
        "TestRecordTxt2: test comments between content lines"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        tioconfig = TxtIOConfig()
        txt_doc = TxtRecord.from_string("""#1 com
t1: uuuu
#3 Comment not allowed here.
#4 Should emitt a warning
 vvvv
t2: uuuu
 vvvv
#8 Here a comment is also not allowed
 wwww
t3: uuuu
#11 Same as t1 but with additional 
#12 comment at the end of the requirement
 vvvv
#14 End comment for t3
t4: uuuu
 vvvv
#17 Same as t2 but with additional 
#18 comment at the end of the requirement
 wwww
#20 End comment for t4
""",
                                        "CommentsEverywhere", tioconfig)

        self.assertEqual(txt_doc.is_usable(), True)
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        result_expected = comment_line % 5 + comment_line % 9 + \
        comment_line % 13 + comment_line % 19
        
        self.assertEquals(result_expected, lstderr)

    def test_neg_08(self):
        "TestRecordTxt2: only intro content line"
        mstderr = StringIO.StringIO()
        init_logger(mstderr)

        tioconfig = TxtIOConfig()
        txt_doc = TxtRecord.from_string("#1 com",
                                        "OnlyEntryComment", tioconfig)

        self.assertEqual(txt_doc.is_usable(), True)
        self.assertEqual(txt_doc.get_comment(), "1 com\n")
        lstderr = hide_timestamp(mstderr.getvalue())
        tear_down_log_handler()
        
        self.assertEquals("", lstderr)
