import unittest
from functions.is_safe_path import is_safe_path

class TestAgentSecurity(unittest.TestCase):
    def test_safe_path(self):
        # Should be allowed
        self.assertTrue(is_safe_path("/var/log/syslog"))
        
    def test_unsafe_path(self):
        # Should be BLOCKED
        self.assertFalse(is_safe_path("/var/log/../../etc/shadow"))
        self.assertFalse(is_safe_path("/home/user/secret.txt"))

if __name__ == '__main__':
    unittest.main()