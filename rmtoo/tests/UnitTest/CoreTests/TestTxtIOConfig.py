'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Unit test for Topic

 (c) 2011-2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.storagebackend.txtfile.TxtIOConfig import TxtIOConfig
from rmtoo.lib.configuration.Cfg import Cfg

class TestTxtIOConfig:

    def test_pos_01(self):
        "TxtIOConfig: check new max line length setting"
        config = Cfg()
        config.set_value('max_input_line_length', 77)

        tic = TxtIOConfig(config, 'requirement')

        assert(tic.get_max_line_length() == 77)
