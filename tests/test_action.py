import unittest

from jvmguard.security.action import ActionRequest


class ActionRequestTests(unittest.TestCase):
    def test_to_dict_contains_expected_fields(self):
        action = ActionRequest(
            agent="test-agent",
            tool="get_system_info",
            arguments={},
            user_goal="inspect system",
        )

        data = action.to_dict()

        self.assertEqual(data["agent"], "test-agent")
        self.assertEqual(data["tool"], "get_system_info")
        self.assertEqual(data["user_goal"], "inspect system")
        self.assertEqual(data["source"], "user")
        self.assertEqual(data["trust_level"], "trusted")
        self.assertTrue(data["timestamp"])


if __name__ == "__main__":
    unittest.main()
