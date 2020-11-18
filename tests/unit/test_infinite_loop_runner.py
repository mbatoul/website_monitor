from website_monitor.loop_runner import LoopRunner

class TestLooperRunner:
  def test_enum(self):
    assert LoopRunner.RUNNING == 1