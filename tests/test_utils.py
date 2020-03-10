from cobra.utils.utils import first_usage, get_object_from_list_by_name
from cobra.utils.constants import Paths


class TestUtils:
    def test_not_first_usage(self, tmp_path, monkeypatch):
        cobra_home_dir = tmp_path / ".cobra"
        cobra_home_dir.mkdir()
        monkeypatch.setattr(Paths, "COBRA_FOLDER", cobra_home_dir)
        assert not first_usage()

    def test_first_usage(self, tmp_path, monkeypatch):
        cobra_home_dir = tmp_path / ".cobra"
        monkeypatch.setattr(Paths, "COBRA_FOLDER", cobra_home_dir)
        assert first_usage()
