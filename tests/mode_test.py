from sourcelib.mode import Mode, DefaultMode

class TestMode:
    def test_create_mode(self):
        default_mode = Mode.create('default')
        assert default_mode is Mode.create('default')
        assert isinstance(default_mode, DefaultMode)