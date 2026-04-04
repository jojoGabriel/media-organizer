import io
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from contextlib import redirect_stdout

from media_organizer.cli import collect_suspicious_report_entries, main, resolve_preview_root
from media_organizer.config import Roots
from media_organizer.scanner import build_scan_report, infer_date, plan_destination


class ScannerTests(unittest.TestCase):
    def test_scan_builds_duplicate_groups_and_sidecar_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            pictures.mkdir()
            videos.mkdir()

            image_a = pictures / "IMG_20200101_0001.jpg"
            image_b = pictures / "copy" / "IMG_20200101_0001.jpg"
            image_b.parent.mkdir()
            sidecar = pictures / "IMG_20200101_0001.jpg.json"

            image_a.write_bytes(b"same-bytes")
            image_b.write_bytes(b"same-bytes")
            sidecar.write_text("{}", encoding="utf-8")

            report = build_scan_report(Roots(pictures=pictures, videos=videos), hash_media=True)

            self.assertEqual(report.summary.images, 2)
            self.assertEqual(report.summary.sidecars, 1)
            self.assertEqual(report.summary.duplicate_groups, 1)

            sidecar_record = next(record for record in report.files if record.path == str(sidecar))
            self.assertEqual(sidecar_record.sidecar_for, str(image_a))

    def test_plan_destination_routes_cache_and_projects(self) -> None:
        pictures_root = Path("/library/Pictures")
        videos_root = Path("/library/Videos")

        cache_path = pictures_root / ".wdmc" / "thumb.jpg"
        project_video_path = videos_root / "PleasantHarmony" / "cut.mp4"

        self.assertEqual(
            plan_destination(cache_path, "pictures", "cache", "2020-01-01", pictures_root),
            "App-Caches/.wdmc/thumb.jpg",
        )
        self.assertEqual(
            plan_destination(project_video_path, "videos", "project_video", "2020-01-01", videos_root),
            "Projects/PleasantHarmony/cut.mp4",
        )

    def test_plan_destination_uses_meaningful_source_label(self) -> None:
        pictures_root = Path("/library/Pictures")

        dated_tree_path = pictures_root / "2000" / "09" / "20" / "Cliff in Clouds.jpg"
        compact_dated_folder_path = pictures_root / "201003" / "Joy and Ima.JPG"
        album_path = pictures_root / "imports" / "Family Trip" / "IMG_0001.jpg"

        self.assertEqual(
            plan_destination(dated_tree_path, "pictures", "image", "2000-09-20", pictures_root),
            "Library/2000/2000-09-20_Pictures/Cliff in Clouds.jpg",
        )
        self.assertEqual(
            plan_destination(compact_dated_folder_path, "pictures", "image", "2010-02-28", pictures_root),
            "Library/2010/2010-02-28_Pictures/Joy and Ima.JPG",
        )
        self.assertEqual(
            plan_destination(album_path, "pictures", "image", "2020-01-01", pictures_root),
            "Library/2020/2020-01-01_Family-Trip/IMG_0001.jpg",
        )

    def test_infer_date_prefers_folder_structure_before_mtime(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "2001" / "10" / "27" / "Bday3.jpg"

        inferred_date, date_source = infer_date(path, pictures_root, 1640995200)

        self.assertEqual(inferred_date, "2001-10-27")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_compact_folder_month_dates(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "201003" / "Joy and Ima.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1267315200)

        self.assertEqual(inferred_date, "2010-03-01")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_compact_folder_day_dates(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "20100613" / "100_0106.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1276214400)

        self.assertEqual(inferred_date, "2010-06-13")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_epoch_timestamp_in_filename(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "FB_IMG_1620441643131.jpg"

        inferred_date, date_source = infer_date(path, pictures_root, 1640995200)

        self.assertEqual(inferred_date, "2021-05-07")
        self.assertEqual(date_source, "filename")

    def test_infer_date_ignores_ancient_placeholder_folder_dates(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "1903" / "12" / "31" / "VIDEO_070.mp4"
        modified_ts = 1191801600

        inferred_date, date_source = infer_date(path, pictures_root, modified_ts)

        self.assertEqual(inferred_date, datetime.fromtimestamp(modified_ts).date().isoformat())
        self.assertEqual(date_source, "mtime")

    def test_preview_command_prints_planned_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            target = pictures / "2000" / "09" / "20" / "IMG_20000920_0001.jpg"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            videos.mkdir()
            target.write_bytes(b"image-bytes")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "preview",
                        "--pictures-root",
                        str(pictures),
                        "--videos-root",
                        str(videos),
                        "--path",
                        str(target),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn(
                "Library/2000/2000-09-20_Pictures/IMG_20000920_0001.jpg",
                output.getvalue(),
            )

    def test_resolve_preview_root_rejects_paths_outside_roots(self) -> None:
        roots = Roots(pictures=Path("/library/Pictures"), videos=Path("/library/Videos"))

        with self.assertRaises(ValueError):
            resolve_preview_root(Path("/elsewhere/file.jpg"), roots)

    def test_suspicious_report_command_prints_flagged_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "files": [
    {
      "path": "/library/Pictures/2000/09/20/Cliff in Clouds.jpg",
      "proposed_relative_destination": "Library/2000/2000-09-20_20/Cliff in Clouds.jpg",
      "inferred_date": "2000-09-20",
      "date_source": "mtime"
    },
    {
      "path": "/library/Pictures/imports/Family Trip/IMG_20200101_0001.jpg",
      "proposed_relative_destination": "Library/2020/2020-01-01_Family-Trip/IMG_20200101_0001.jpg",
      "inferred_date": "2020-01-01",
      "date_source": "filename"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["suspicious-report", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 suspicious planned destinations", output.getvalue())
            self.assertIn("numeric-label,mtime-date", output.getvalue())

    def test_collect_suspicious_report_entries_ignores_clean_rows(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/imports/Family Trip/IMG_20200101_0001.jpg",
                    "proposed_relative_destination": "Library/2020/2020-01-01_Family-Trip/IMG_20200101_0001.jpg",
                    "inferred_date": "2020-01-01",
                    "date_source": "filename",
                }
            ]
        }

        self.assertEqual(collect_suspicious_report_entries(report_data), [])

    def test_collect_suspicious_report_entries_ignores_generic_label_only(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/2000/09/20/Cliff in Clouds.jpg",
                    "proposed_relative_destination": "Library/2000/2000-09-20_Pictures/Cliff in Clouds.jpg",
                    "inferred_date": "2000-09-20",
                    "date_source": "path",
                }
            ]
        }

        self.assertEqual(collect_suspicious_report_entries(report_data), [])


if __name__ == "__main__":
    unittest.main()
