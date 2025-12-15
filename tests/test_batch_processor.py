import csv
from pathlib import Path

from src.verification.batch_processor import BatchVerificationProcessor


class DummyVerifier:
    def __init__(self, result):
        self._result = result

    def verify(self, ref_image, tmp_image):
        return self._result

    def extract(self, image):
        return {"num_faces": 1}


def make_member_csv(root_dir: Path, group_name="na22"):
    data_dir = root_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / f"{group_name}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hubo_id", "name", "photo_url"])
        writer.writerow(["123", "곽상언", "http://example.com/photo.jpg"])
    return path


def test_process_members_verified_skips_search(tmp_path, monkeypatch, capsys):
    # prepare a fake project root with data CSV
    proj_root = tmp_path / "proj"
    proj_root.mkdir()
    make_member_csv(proj_root, "na22")

    # create reference images dir
    ref_dir = tmp_path / "refs"
    ref_dir.mkdir()
    (ref_dir / "123.JPG").write_text("")

    # instantiate processor and point its project_root to our temp project root
    processor = BatchVerificationProcessor(str(ref_dir))
    processor.project_root = str(proj_root)

    # monkeypatch download to create a tmp image and return its path
    def fake_download(url, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        Path(filename).write_text("fakeimage")
        return filename

    monkeypatch.setattr(processor, "_download_image", fake_download)

    # monkeypatch FaceVerifier used inside to the dummy that returns verified
    monkeypatch.setattr(
        "src.verification.batch_processor.FaceVerifier",
        lambda: DummyVerifier({"verified": True, "similarity": 0.8}),
    )

    # run
    processor.process_members_by_huboid("na22")

    captured = capsys.readouterr()
    assert "Verification result for 123" in captured.out
    assert "Search results" not in captured.out


def test_process_members_failed_verification_triggers_search(
    tmp_path, monkeypatch, capsys
):
    proj_root = tmp_path / "proj"
    proj_root.mkdir()
    make_member_csv(proj_root, "na22")

    ref_dir = tmp_path / "refs"
    ref_dir.mkdir()
    (ref_dir / "123.JPG").write_text("")

    processor = BatchVerificationProcessor(str(ref_dir))
    processor.project_root = str(proj_root)

    def fake_download(url, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        Path(filename).write_text("fakeimage")
        return filename

    monkeypatch.setattr(processor, "_download_image", fake_download)

    # verifier returns not verified
    monkeypatch.setattr(
        "src.verification.batch_processor.FaceVerifier",
        lambda: DummyVerifier({"verified": False}),
    )

    # monkeypatch search results
    monkeypatch.setattr(
        processor, "_search_images", lambda q: ["http://example.com/img1.jpg"]
    )

    processor.process_members_by_huboid("na22")

    captured = capsys.readouterr()
    assert "Verification FAILED for 123" in captured.out
