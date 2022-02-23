import CheckModule
import unittest
from unittest import mock

@mock.patch.object(CheckModule, 'send_email')
@mock.patch.object(CheckModule, 'log')
class TestRuntimeModule(unittest.TestCase):
    
    def test_check_for_excess_info(self, mock_log, mock_send_email):
        CheckModule.check_for_excess(80, 90, 50, "CPU")
        mock_log.assert_called_with(50, "CPU", "info")

    def test_check_for_excess_warning(self, mock_log, mock_send_email):
        CheckModule.check_for_excess(80, 90, 85, "RAM")
        mock_log.assert_called_with(85, "RAM", "warning")

    def test_check_for_excess_critical(self, mock_log, mock_send_email):
        CheckModule.check_for_excess(80, 90, 95, "Disk")
        mock_log.assert_called_with(95, "Disk", "critical")  
        mock_send_email.assert_called()
                
    def test_check_send_email(self, mock_log, mock_send_email):
        CheckModule.check_for_excess(80, 90, 95, "CPU")
        mock_send_email.assert_called()
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)