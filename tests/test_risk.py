import unittest

from jvmguard.security.action import ActionRequest
from jvmguard.security.risk import RiskLevel, assess_action


class RiskEngineTests(unittest.TestCase):
    def test_safe_action_is_low_risk(self):
        action = ActionRequest(
            agent="test-agent",
            tool="get_system_info",
            arguments={},
        )
        risk = assess_action(action)
        self.assertEqual(risk.score, 0)
        self.assertEqual(risk.level, RiskLevel.LOW)

    def test_untrusted_source_increases_risk(self):
        action = ActionRequest(
            agent="test-agent",
            tool="get_system_info",
            arguments={},
            trust_level="untrusted",
        )
        risk = assess_action(action)
        self.assertEqual(risk.score, 25)
        self.assertEqual(risk.level, RiskLevel.MEDIUM)

    def test_sensitive_resource_is_detected(self):
        action = ActionRequest(
            agent="test-agent",
            tool="read_file",
            arguments={"path": ".env"},
        )
        risk = assess_action(action)
        self.assertEqual(risk.score, 45)
        self.assertEqual(risk.level, RiskLevel.MEDIUM)

    def test_dangerous_tool_and_sudo_can_reach_critical(self):
        action = ActionRequest(
            agent="test-agent",
            tool="run_command",
            arguments={"command": "sudo whoami"},
        )
        risk = assess_action(action)
        self.assertEqual(risk.score, 80)
        self.assertEqual(risk.level, RiskLevel.CRITICAL)


if __name__ == "__main__":
    unittest.main()
