import ExceedanceCheckModule as ECM
import MailerService as MS
import MonitoringGui as MG
import unittest
from unittest import mock
import time

class TestRuntimeModule(unittest.TestCase):
    
    @mock.patch.object(ECM, 'log')
    def test_check_for_excess_info(self, mock_log):
        ECM.check_for_excess(80, 90, 50, 'CPU')
        mock_log.assert_called_with('info', 'CPU', 90, 80, 50)

    @mock.patch.object(ECM, 'log')
    def test_check_for_excess_warning(self, mock_log):
        ECM.check_for_excess(80, 90, 85, 'RAM')
        mock_log.assert_called_with('warning', 'RAM', 90, 80, 85)

    @mock.patch.object(MS, 'send_email')
    @mock.patch.object(ECM, 'log')
    def test_check_for_excess_critical(self, mock_log, mock_send_email):
        ECM.check_for_excess(80, 90, 95, 'Disk C:')
        mock_log.assert_called_with('critical', 'Disk C:', 90, 80, 95)  
        mock_send_email.assert_called()   
        
    def test_check_last_executed_false(self): 
        last_time = time.time()
        time.sleep(1)
        self.assertFalse(ECM.check_last_executed(last_time, 5))
        
    def test_check_last_executed_true(self): 
        last_time = time.time()
        time.sleep(2)
        self.assertTrue(ECM.check_last_executed(last_time, 1))
    
    @mock.patch.object(MG, 'is_float')    
    def check_is_float(self, mock):
        self.assertTrue(MG.is_float(12))
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)