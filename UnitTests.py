import ExceedanceCheckModule as ECM
import MailerService as MS
import unittest
from unittest import mock

@mock.patch.object(MS, 'send_email')
@mock.patch.object(ECM, 'log')
class TestRuntimeModule(unittest.TestCase):
    
    def test_check_for_excess_info(self, mock_log, mock_send_email):
        ECM.check_for_excess(80, 90, 50, 'CPU')
        mock_log.assert_called_with('info', 'CPU', 90, 80, 50)

    def test_check_for_excess_warning(self, mock_log, mock_send_email):
        ECM.check_for_excess(80, 90, 85, 'RAM')
        mock_log.assert_called_with('warning', 'RAM', 90, 80, 85)

    def test_check_for_excess_critical(self, mock_log, mock_send_email):
        ECM.check_for_excess(80, 90, 95, 'Disk C:')
        mock_log.assert_called_with('critical', 'Disk C:', 90, 80, 95)  
        mock_send_email.assert_called()
                
    def test_check_send_email(self, mock_log, mock_send_email):
        ECM.check_for_excess(80, 90, 95, 'CPU')
        mock_send_email.assert_called()
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)