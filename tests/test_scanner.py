import io
import json
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from media_organizer.cli import (
    build_apply_payload,
    collect_google_photos_matches,
    collect_google_photos_received,
    collect_google_photos_summary,
    collect_google_photos_sidecar_gaps,
    collect_mtime_summary_groups,
    collect_suspicious_report_entries,
    inspect_google_photos_folder,
    main,
    resolve_preview_root,
    verify_source_matches_report,
)
from media_organizer.config import Roots
from media_organizer.scanner import build_file_record, build_scan_report, infer_date, plan_destination


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

    def test_build_file_record_routes_project_images_under_projects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            target = videos / "PleasantHarmony" / "logo.png"
            target.parent.mkdir(parents=True)
            pictures.mkdir()
            videos.mkdir(exist_ok=True)
            target.write_bytes(b"image-bytes")

            record = build_file_record(target, root_type="videos", root_path=videos, hash_media=False)

            self.assertEqual(record.category, "image")
            self.assertEqual(record.proposed_relative_destination, "Projects/PleasantHarmony/logo.png")

    def test_build_file_record_routes_root_cs50w_videos_under_projects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            target = videos / "cs50w-project1.mp4"
            pictures.mkdir()
            videos.mkdir(exist_ok=True)
            target.write_bytes(b"video-bytes")

            record = build_file_record(target, root_type="videos", root_path=videos, hash_media=False)

            self.assertEqual(record.category, "video")
            self.assertEqual(record.proposed_relative_destination, "Projects/cs50w/cs50w-project1.mp4")

    def test_build_file_record_routes_project_unknown_files_under_projects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            target = videos / "PleasantHarmony" / "session.kdenlive"
            target.parent.mkdir(parents=True)
            pictures.mkdir()
            videos.mkdir(exist_ok=True)
            target.write_bytes(b"project-file")

            record = build_file_record(target, root_type="videos", root_path=videos, hash_media=False)

            self.assertEqual(record.category, "unknown")
            self.assertEqual(record.proposed_relative_destination, "Projects/PleasantHarmony/session.kdenlive")

    def test_build_file_record_routes_project_cache_files_to_app_caches(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            target = videos / "PleasantHarmony" / ".wdmc" / "thumb.jpg"
            target.parent.mkdir(parents=True)
            pictures.mkdir()
            videos.mkdir(exist_ok=True)
            target.write_bytes(b"cache-bytes")

            record = build_file_record(target, root_type="videos", root_path=videos, hash_media=False)

            self.assertEqual(record.category, "cache")
            self.assertEqual(record.proposed_relative_destination, "App-Caches/PleasantHarmony/.wdmc/thumb.jpg")

    def test_build_file_record_classifies_photodirector_cache_without_extension_as_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "PhotoDirector" / "3.0" / "gabriel" / "gabriel_cache" / "10_original"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"jpeg-like-cache-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "cache")
            self.assertEqual(
                record.proposed_relative_destination,
                "App-Caches/PhotoDirector/3.0/gabriel/gabriel_cache/10_original",
            )

    def test_build_file_record_classifies_wmv_and_flv_as_video(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            videos = temp_path / "Videos"
            pictures.mkdir()
            videos.mkdir()

            wmv_path = pictures / "2011" / "08" / "03" / "Jahna.wmv"
            wmv_path.parent.mkdir(parents=True)
            wmv_path.write_bytes(b"wmv-bytes")

            flv_path = videos / "legacy" / "capture.flv"
            flv_path.parent.mkdir(parents=True)
            flv_path.write_bytes(b"flv-bytes")

            wmv_record = build_file_record(wmv_path, root_type="pictures", root_path=pictures, hash_media=False)
            flv_record = build_file_record(flv_path, root_type="videos", root_path=videos, hash_media=False)

            self.assertEqual(wmv_record.category, "video")
            self.assertEqual(flv_record.category, "video")

    def test_build_file_record_keeps_destination_for_unknown_files_already_in_structured_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "Reference" / "Documents" / "Scanned Document.pdf"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"pdf-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "unknown")
            self.assertEqual(record.proposed_relative_destination, "Reference/Documents/Scanned Document.pdf")

    def test_plan_destination_uses_meaningful_source_label(self) -> None:
        pictures_root = Path("/library/Pictures")

        dated_tree_path = pictures_root / "2000" / "09" / "20" / "Cliff in Clouds.jpg"
        compact_dated_folder_path = pictures_root / "201003" / "Joy and Ima.JPG"
        album_path = pictures_root / "imports" / "Family Trip" / "IMG_0001.jpg"
        jonel_camera_path = pictures_root / "Pictures from ates camera" / "121_0705" / "IMG_0596.JPG"

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
        self.assertEqual(
            plan_destination(jonel_camera_path, "pictures", "image", "2013-07-04", pictures_root),
            "Shared/Jonel/2013/2013-07-04_Jonel/IMG_0596.JPG",
        )

    def test_plan_destination_routes_jonel_to_shared_library(self) -> None:
        pictures_root = Path("/library/Pictures")
        jonel_path = pictures_root / "Jonel" / "DSC01283.JPG"

        self.assertEqual(
            plan_destination(jonel_path, "pictures", "image", "2015-06-22", pictures_root),
            "Shared/Jonel/2015/2015-06-22_Jonel/DSC01283.JPG",
        )

    def test_plan_destination_routes_samyra_to_shared_library(self) -> None:
        pictures_root = Path("/library/Pictures")
        samyra_path = pictures_root / "Samyras 16" / "IMG_1178.JPG"

        self.assertEqual(
            plan_destination(samyra_path, "pictures", "image", "2014-09-05", pictures_root),
            "Shared/Samyra/2014/2014-09-05_Samyra/IMG_1178.JPG",
        )

    def test_plan_destination_routes_ceu_to_shared_library(self) -> None:
        pictures_root = Path("/library/Pictures")
        ceu_path = pictures_root / "ceu" / "grad1.jpg"

        self.assertEqual(
            plan_destination(ceu_path, "pictures", "image", "2016-05-10", pictures_root),
            "Shared/CEU/2016/2016-05-10_CEU/grad1.jpg",
        )

    def test_build_file_record_routes_ceu_to_undated_shared_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "ceu" / "grad1.jpg"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"image-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "image")
            self.assertEqual(record.proposed_relative_destination, "Shared/CEU/Undated/grad1.jpg")

    def test_plan_destination_routes_tito_osias_to_shared_library(self) -> None:
        pictures_root = Path("/library/Pictures")
        tito_osias_path = pictures_root / "Tito Osias" / "IMG_0001.JPG"

        self.assertEqual(
            plan_destination(tito_osias_path, "pictures", "image", "2012-08-14", pictures_root),
            "Shared/Tito-Osias/2012/2012-08-14_Tito-Osias/IMG_0001.JPG",
        )

    def test_build_file_record_routes_nanay80_items_to_shared_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "nanay80" / "436363125_806662541380645_2610630878209441441_n.jpg"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"image-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(
                record.proposed_relative_destination,
                "Shared/nanayCora80th/436363125_806662541380645_2610630878209441441_n.jpg",
            )

    def test_build_file_record_routes_nanay80_unknown_files_to_shared_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "nanay80" / "d1.pdf"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"pdf-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "unknown")
            self.assertEqual(record.proposed_relative_destination, "Shared/nanayCora80th/d1.pdf")

    def test_build_file_record_routes_reference_folders_outside_dated_library(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            pictures.mkdir(exist_ok=True)

            samples = {
                "Pexels": "pexels-cottonbro-5876759.jpg",
                "Screenshots": "Screenshot (1).png",
                "Wallpapers": "NayTay.png",
                "googleEarth": "joy house.png",
            }

            for folder, filename in samples.items():
                target = pictures / folder / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"image-bytes")

                record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

                self.assertEqual(record.category, "image")
                self.assertEqual(
                    record.proposed_relative_destination,
                    "Reference/{0}/{1}".format(folder, filename),
                )

    def test_build_file_record_routes_morepics_to_legacy_scans_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "morePics" / "Lola 081099 Front.jpg"
            target.parent.mkdir(parents=True)
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"image-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "image")
            self.assertEqual(
                record.proposed_relative_destination,
                "Reference/Legacy-Scans/morePics/Lola 081099 Front.jpg",
            )

    def test_build_file_record_routes_loose_scanned_joy_png_to_legacy_scans_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pictures = temp_path / "Pictures"
            target = pictures / "joy.png"
            pictures.mkdir(exist_ok=True)
            target.write_bytes(b"image-bytes")

            record = build_file_record(target, root_type="pictures", root_path=pictures, hash_media=False)

            self.assertEqual(record.category, "image")
            self.assertEqual(
                record.proposed_relative_destination,
                "Reference/Legacy-Scans/loose-root/joy.png",
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

    def test_infer_date_uses_date_prefixed_folder_names(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "Photos" / "2008" / "2008-04-20--18.53.11" / "DSCF1286.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1640995200)

        self.assertEqual(inferred_date, "2008-04-20")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_named_year_bucket_folders(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "google-takeout" / "Takeout" / "Google Photos" / "Photos from 2014" / "MOVIE.m4v"

        inferred_date, date_source = infer_date(path, pictures_root, 1775001600)

        self.assertEqual(inferred_date, "2014-01-01")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_year_and_month_name_folders(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "Photos" / "2007" / "Jun" / "DSCF0720.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1194048000)

        self.assertEqual(inferred_date, "2007-06-01")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_ates_camera_folder_dates_for_2013(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "Pictures from ates camera" / "121_0705" / "IMG_0596.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1372982400)

        self.assertEqual(inferred_date, "2013-07-05")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_ates_camera_folder_dates_for_2014(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "Pictures from ates camera" / "200_0523" / "IMG_0440.JPG"

        inferred_date, date_source = infer_date(path, pictures_root, 1400803200)

        self.assertEqual(inferred_date, "2014-05-23")
        self.assertEqual(date_source, "path")

    def test_infer_date_uses_year_prefix_for_numeric_sequence_filenames(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "morePics" / "200600001.jpg"

        inferred_date, date_source = infer_date(path, pictures_root, 1165622400)

        self.assertEqual(inferred_date, "2006-01-01")
        self.assertEqual(date_source, "filename")

    def test_infer_date_uses_exif_metadata_for_images(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "IMG_0001.jpg"

        class FakeImage:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def getexif(self):
                return {36867: "2014:09:05 05:44:58"}

        with patch("media_organizer.scanner.Image.open", return_value=FakeImage()):
            inferred_date, date_source = infer_date(path, pictures_root, 0)

        self.assertEqual(inferred_date, "2014-09-05")
        self.assertEqual(date_source, "metadata")

    def test_infer_date_uses_embedded_video_metadata(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "MVI_0739.MOV"
        probe_output = json.dumps(
            {
                "format": {"tags": {"creation_time": "2014-06-28T16:17:15.000000Z"}},
                "streams": [{"tags": {"handler_name": "VideoHandler"}}],
            }
        )

        with patch(
            "media_organizer.scanner.subprocess.run",
            return_value=subprocess.CompletedProcess(args=["ffprobe"], returncode=0, stdout=probe_output),
        ):
            inferred_date, date_source = infer_date(path, pictures_root, 0)

        self.assertEqual(inferred_date, "2014-06-28")
        self.assertEqual(date_source, "metadata")

    def test_infer_date_uses_quicktime_creationdate_metadata_for_videos(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "MVI_0739.MOV"
        probe_output = json.dumps(
            {
                "format": {"tags": {"com.apple.quicktime.creationdate": "2014-06-28T11:17:15-0500"}},
                "streams": [],
            }
        )

        with patch(
            "media_organizer.scanner.subprocess.run",
            return_value=subprocess.CompletedProcess(args=["ffprobe"], returncode=0, stdout=probe_output),
        ):
            inferred_date, date_source = infer_date(path, pictures_root, 0)

        self.assertEqual(inferred_date, "2014-06-28")
        self.assertEqual(date_source, "metadata")

    def test_infer_date_falls_back_when_video_metadata_probe_fails(self) -> None:
        pictures_root = Path("/library/Pictures")
        path = pictures_root / "summer2014" / "MVI_0739.MOV"
        modified_ts = 1403950634

        with patch(
            "media_organizer.scanner.subprocess.run",
            side_effect=subprocess.CalledProcessError(returncode=1, cmd=["ffprobe"]),
        ):
            inferred_date, date_source = infer_date(path, pictures_root, modified_ts)

        self.assertEqual(inferred_date, "2014-06-28")
        self.assertEqual(date_source, "mtime")

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

    def test_collect_mtime_summary_groups_groups_by_folder_and_pattern(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/Jonel/DSC01283.JPG",
                    "category": "image",
                    "date_source": "mtime",
                },
                {
                    "path": "/library/Pictures/Jonel/DSC01284.JPG",
                    "category": "image",
                    "date_source": "mtime",
                },
                {
                    "path": "/library/Pictures/Jonel/IMG_0001.JPG",
                    "category": "image",
                    "date_source": "mtime",
                },
                {
                    "path": "/library/Pictures/Jonel/notes.txt",
                    "category": "unknown",
                    "date_source": "mtime",
                },
                {
                    "path": "/library/Pictures/Trips/DSC05555.JPG",
                    "category": "image",
                    "date_source": "path",
                },
            ]
        }

        groups = collect_mtime_summary_groups(report_data)

        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["folder"], "/library/Pictures/Jonel")
        self.assertEqual(groups[0]["pattern"], "DSC<digits>.JPG")
        self.assertEqual(groups[0]["count"], 2)
        self.assertEqual(groups[0]["sample"], "DSC01283.JPG")

    def test_collect_mtime_summary_groups_ignores_direct_shared_overrides(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/nanay80/436363125_806662541380645_2610630878209441441_n.jpg",
                    "category": "image",
                    "date_source": "mtime",
                    "proposed_relative_destination": "Shared/nanayCora80th/436363125_806662541380645_2610630878209441441_n.jpg",
                }
            ]
        }

        self.assertEqual(collect_mtime_summary_groups(report_data), [])

    def test_collect_mtime_summary_groups_ignores_reference_overrides(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/Screenshots/Screenshot (1).png",
                    "category": "image",
                    "date_source": "mtime",
                    "proposed_relative_destination": "Reference/Screenshots/Screenshot (1).png",
                }
            ]
        }

        self.assertEqual(collect_mtime_summary_groups(report_data), [])

    def test_collect_mtime_summary_groups_ignores_ceu_undated_override(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Pictures/ceu/grad1.jpg",
                    "category": "image",
                    "date_source": "mtime",
                    "proposed_relative_destination": "Shared/CEU/Undated/grad1.jpg",
                }
            ]
        }

        self.assertEqual(collect_mtime_summary_groups(report_data), [])

    def test_collect_mtime_summary_groups_ignores_project_overrides(self) -> None:
        report_data = {
            "files": [
                {
                    "path": "/library/Videos/cs50w-project1.mp4",
                    "category": "video",
                    "date_source": "mtime",
                    "proposed_relative_destination": "Projects/cs50w/cs50w-project1.mp4",
                }
            ]
        }

        self.assertEqual(collect_mtime_summary_groups(report_data), [])

    def test_mtime_summary_command_prints_grouped_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "files": [
    {
      "path": "/library/Pictures/Jonel/DSC01283.JPG",
      "category": "image",
      "date_source": "mtime"
    },
    {
      "path": "/library/Pictures/Jonel/DSC01284.JPG",
      "category": "image",
      "date_source": "mtime"
    },
    {
      "path": "/library/Pictures/Jonel/IMG_0001.JPG",
      "category": "image",
      "date_source": "mtime"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["mtime-summary", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 2 grouped mtime patterns across 3 files", output.getvalue())
            self.assertIn("folder=/library/Pictures/Jonel | pattern=DSC<digits>.JPG", output.getvalue())

    def test_collect_google_photos_summary_groups_takeout_folders(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/received_1.jpeg",
                    "category": "image",
                    "date_source": "path",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
                    "category": "image",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1.jpg.supplemental-metadata.json",
                    "category": "sidecar",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Jonel 26/20210419_165459.jpg",
                    "category": "image",
                    "date_source": "filename",
                },
            ],
        }

        summaries = collect_google_photos_summary(report_data)

        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries[0]["folder"], "Photos from 2021")
        self.assertEqual(summaries[0]["media"], 2)
        self.assertEqual(summaries[0]["sidecars"], 1)
        self.assertEqual(summaries[0]["edited"], 1)
        self.assertEqual(summaries[0]["received"], 1)
        self.assertEqual(summaries[0]["path"], 1)
        self.assertEqual(summaries[0]["filename"], 1)

    def test_google_photos_summary_command_prints_folder_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/received_1.jpeg",
      "category": "image",
      "date_source": "path"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
      "category": "image",
      "date_source": "filename"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1.jpg.supplemental-metadata.json",
      "category": "sidecar",
      "date_source": "filename"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["google-photos-summary", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 Google Photos folders", output.getvalue())
            self.assertIn("Photos from 2021 | media=2 sidecars=1 edited=1 received=1", output.getvalue())

    def test_inspect_google_photos_folder_groups_edited_pairs_and_sidecars(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1-edited.jpg",
                    "category": "image",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg",
                    "category": "image",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg.supplemental-metada.json",
                    "category": "sidecar",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/received_2.jpeg",
                    "category": "image",
                    "date_source": "path",
                },
            ],
        }

        summary = inspect_google_photos_folder(report_data, "Photos from 2014")

        self.assertIsNotNone(summary)
        self.assertEqual(summary["media"], 3)
        self.assertEqual(summary["sidecars"], 1)
        self.assertEqual(summary["edited"], 1)
        self.assertEqual(summary["received"], 1)
        self.assertEqual(summary["groups"][0]["kind"], "edited-pair")
        self.assertEqual(summary["groups"][0]["name"], "IMG_1.jpg")

    def test_google_photos_folder_command_prints_group_details(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1-edited.jpg",
      "category": "image",
      "date_source": "filename"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg",
      "category": "image",
      "date_source": "filename"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg.supplemental-metada.json",
      "category": "sidecar",
      "date_source": "filename"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "google-photos-folder",
                        "--report",
                        str(report_path),
                        "--folder",
                        "Photos from 2014",
                        "--limit",
                        "5",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Photos from 2014 | media=2 sidecars=1 edited=1", output.getvalue())
            self.assertIn("edited-pair | count=2 sidecars=1 name=IMG_1.jpg", output.getvalue())

    def test_collect_google_photos_received_groups_by_folder(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/received_1.jpeg",
                    "category": "image",
                    "date_source": "path",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/received_1.jpeg.supplemental-met.json",
                    "category": "sidecar",
                    "date_source": "path",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Jonel 26/received_2.jpeg",
                    "category": "image",
                    "date_source": "mtime",
                },
            ],
        }

        items = collect_google_photos_received(report_data)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["folder"], "Photos from 2021")
        self.assertEqual(items[0]["sidecars"], 1)
        self.assertEqual(items[1]["folder"], "Jonel 26")

    def test_collect_google_photos_sidecar_gaps_finds_unmatched_sidecars(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg.supplemental-metada.json",
                    "category": "sidecar",
                    "date_source": "filename",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_2.jpg",
                    "category": "image",
                    "date_source": "filename",
                },
            ],
        }

        items = collect_google_photos_sidecar_gaps(report_data)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["folder"], "Photos from 2014")
        self.assertEqual(items[0]["name"], "IMG_1.jpg")

    def test_collect_google_photos_matches_compares_against_rest_of_library(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
                    "category": "image",
                    "inferred_date": "2021-04-19",
                },
                {
                    "path": "/library/Pictures/imports/Album/IMG_1.jpg",
                    "category": "image",
                    "inferred_date": "2021-04-19",
                },
            ],
        }

        items = collect_google_photos_matches(report_data)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"], "IMG_1.jpg")
        self.assertEqual(items[0]["date"], "2021-04-19")

    def test_collect_google_photos_matches_can_filter_by_date_and_rest_folder(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
                    "category": "image",
                    "inferred_date": "2021-04-19",
                },
                {
                    "path": "/library/Pictures/imports/Album/IMG_1.jpg",
                    "category": "image",
                    "inferred_date": "2021-04-19",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2020/IMG_2-edited.jpg",
                    "category": "image",
                    "inferred_date": "2020-01-01",
                },
                {
                    "path": "/library/Pictures/elsewhere/IMG_2.jpg",
                    "category": "image",
                    "inferred_date": "2020-01-01",
                },
            ],
        }

        items = collect_google_photos_matches(
            report_data,
            dates=["2021-04-19"],
            rest_folder_contains="/library/Pictures/imports",
        )

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"], "IMG_1.jpg")

    def test_google_photos_received_command_prints_folder_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/received_1.jpeg",
      "category": "image",
      "date_source": "path"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["google-photos-received", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 Google Photos folders with received_* items", output.getvalue())
            self.assertIn("Photos from 2021 | media=1 sidecars=0", output.getvalue())

    def test_google_photos_sidecar_gaps_command_prints_gap_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2014/IMG_1.jpg.supplemental-metada.json",
      "category": "sidecar",
      "date_source": "filename"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["google-photos-sidecar-gaps", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 sidecar-only Google Photos groups", output.getvalue())
            self.assertIn("Photos from 2014 | sidecars=1 name=IMG_1.jpg", output.getvalue())

    def test_google_photos_compare_command_prints_match_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    },
    {
      "path": "/library/Pictures/imports/Album/IMG_1.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["google-photos-compare", "--report", str(report_path), "--limit", "5"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 Google Photos match groups", output.getvalue())
            self.assertIn("2021-04-19 | IMG_1.jpg | google=1 rest=1", output.getvalue())

    def test_google_photos_compare_command_accepts_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    },
    {
      "path": "/library/Pictures/imports/Album/IMG_1.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2020/IMG_2-edited.jpg",
      "category": "image",
      "inferred_date": "2020-01-01"
    },
    {
      "path": "/library/Pictures/elsewhere/IMG_2.jpg",
      "category": "image",
      "inferred_date": "2020-01-01"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "google-photos-compare",
                        "--report",
                        str(report_path),
                        "--date",
                        "2021-04-19",
                        "--rest-folder-contains",
                        "/library/Pictures/imports",
                        "--limit",
                        "5",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Found 1 Google Photos match groups", output.getvalue())
            self.assertIn("2021-04-19 | IMG_1.jpg | google=1 rest=1", output.getvalue())

    def test_google_photos_compare_command_can_write_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            output_path = temp_path / "matches.json"
            report_path.write_text(
                """
{
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    },
    {
      "path": "/library/Pictures/imports/Album/IMG_1.jpg",
      "category": "image",
      "inferred_date": "2021-04-19"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "google-photos-compare",
                        "--report",
                        str(report_path),
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Wrote 1 Google Photos match groups", output.getvalue())

            written = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(written["match_count"], 1)
            self.assertEqual(written["matches"][0]["name"], "IMG_1.jpg")

    def test_final_review_package_command_writes_bundle_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            output_dir = temp_path / "review"
            report_path.write_text(
                """
{
  "summary": {
    "total_files": 2,
    "images": 1,
    "videos": 0,
    "sidecars": 1,
    "caches": 0,
    "unknown": 0
  },
  "roots": {
    "pictures": "/library/Pictures",
    "videos": "/library/Videos"
  },
  "files": [
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1-edited.jpg",
      "category": "image",
      "inferred_date": "2021-04-19",
      "date_source": "filename",
      "proposed_relative_destination": "Library/2021/2021-04-19_Photos-from-2021/IMG_1-edited.jpg"
    },
    {
      "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1.jpg.supplemental-metada.json",
      "category": "sidecar",
      "inferred_date": "2021-04-19",
      "date_source": "filename",
      "proposed_relative_destination": "Exports/google-takeout/Takeout/Google Photos/Photos from 2021/IMG_1.jpg.supplemental-metada.json"
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "final-review-package",
                        "--report",
                        str(report_path),
                        "--output-dir",
                        str(output_dir),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Wrote final review package", output.getvalue())
            self.assertTrue((output_dir / "README.md").exists())
            self.assertTrue((output_dir / "google-photos-summary.json").exists())
            self.assertTrue((output_dir / "google-photos-2014-review.json").exists())

    def test_build_apply_payload_skips_conservative_categories_by_default(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/imports/IMG_20200101_0001.jpg",
                    "category": "image",
                    "date_source": "filename",
                    "size_bytes": 5,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2020/2020-01-01_imports/IMG_20200101_0001.jpg",
                },
                {
                    "path": "/library/Pictures/imports/IMG_20200101_0001.jpg.json",
                    "category": "sidecar",
                    "date_source": "filename",
                    "size_bytes": 2,
                    "modified_at": "2020-01-01T00:00:00",
                    "sidecar_for": "/library/Pictures/imports/IMG_20200101_0001.jpg",
                    "proposed_relative_destination": "Exports/imports/IMG_20200101_0001.jpg.json",
                },
                {
                    "path": "/library/Pictures/mtime/IMG_1.jpg",
                    "category": "image",
                    "date_source": "mtime",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2020/2020-01-01_mtime/IMG_1.jpg",
                },
                {
                    "path": "/library/Pictures/dup/IMG_2.jpg",
                    "category": "image",
                    "date_source": "filename",
                    "duplicate_group": "dup-0001",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2020/2020-01-01_dup/IMG_2.jpg",
                },
                {
                    "path": "/library/Pictures/.wdmc/thumb.jpg",
                    "category": "cache",
                    "date_source": "filename",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "App-Caches/.wdmc/thumb.jpg",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/received_1.jpeg",
                    "category": "image",
                    "date_source": "path",
                    "size_bytes": 1,
                    "modified_at": "2024-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2024/2024-01-01_Photos-from-2024/received_1.jpeg",
                },
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/IMG_3.jpg.supplemental-met.json",
                    "category": "sidecar",
                    "date_source": "path",
                    "size_bytes": 1,
                    "modified_at": "2024-01-01T00:00:00",
                    "proposed_relative_destination": "Exports/google-takeout/Takeout/Google Photos/Photos from 2024/IMG_3.jpg.supplemental-met.json",
                },
                {
                    "path": "/library/Videos/PleasantHarmony/Hymns/hymns.m4v",
                    "category": "project_video",
                    "date_source": "filename",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Projects/PleasantHarmony/Hymns/hymns.m4v",
                },
            ],
        }

        payload = build_apply_payload(report_data, Path("/tmp/report.json"), Path("/dest"))

        self.assertEqual(len(payload["operations"]), 2)
        self.assertEqual(
            [item["source"] for item in payload["operations"]],
            [
                "/library/Pictures/imports/IMG_20200101_0001.jpg",
                "/library/Pictures/imports/IMG_20200101_0001.jpg.json",
            ],
        )
        skipped = {item["path"]: item["reason"] for item in payload["skipped"]}
        self.assertEqual(skipped["/library/Pictures/mtime/IMG_1.jpg"], "mtime-date")
        self.assertEqual(skipped["/library/Pictures/dup/IMG_2.jpg"], "duplicate-group")
        self.assertEqual(skipped["/library/Pictures/.wdmc/thumb.jpg"], "cache")
        self.assertEqual(
            skipped["/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/received_1.jpeg"],
            "google-takeout",
        )
        self.assertEqual(
            skipped["/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/IMG_3.jpg.supplemental-met.json"],
            "google-takeout",
        )
        self.assertEqual(
            skipped["/library/Videos/PleasantHarmony/Hymns/hymns.m4v"],
            "pleasantharmony",
        )

    def test_build_apply_payload_skips_sidecar_when_target_is_excluded(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/mtime/IMG_1.jpg",
                    "category": "image",
                    "date_source": "mtime",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2020/2020-01-01_mtime/IMG_1.jpg",
                },
                {
                    "path": "/library/Pictures/mtime/IMG_1.jpg.json",
                    "category": "sidecar",
                    "date_source": "filename",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "sidecar_for": "/library/Pictures/mtime/IMG_1.jpg",
                    "proposed_relative_destination": "Exports/mtime/IMG_1.jpg.json",
                },
            ],
        }

        payload = build_apply_payload(report_data, Path("/tmp/report.json"), Path("/dest"))

        self.assertEqual(payload["operations"], [])
        skipped = {item["path"]: item["reason"] for item in payload["skipped"]}
        self.assertEqual(skipped["/library/Pictures/mtime/IMG_1.jpg"], "mtime-date")
        self.assertEqual(skipped["/library/Pictures/mtime/IMG_1.jpg.json"], "sidecar-target-not-selected")

    def test_verify_source_matches_report_rejects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "sample.jpg"
            source.write_bytes(b"abc")
            operation = {
                "source": str(source),
                "destination": str(Path(temp_dir) / "dest" / "sample.jpg"),
                "size_bytes": 4,
                "modified_at": datetime.fromtimestamp(source.stat().st_mtime).isoformat(),
            }

            with self.assertRaises(ValueError):
                verify_source_matches_report(source, operation)

    def test_verify_source_matches_report_accepts_zero_byte_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "empty.jpg"
            source.write_bytes(b"")
            operation = {
                "source": str(source),
                "destination": str(Path(temp_dir) / "dest" / "empty.jpg"),
                "size_bytes": 0,
                "modified_at": datetime.fromtimestamp(source.stat().st_mtime).isoformat(),
            }

            verify_source_matches_report(source, operation)

    def test_apply_command_dry_run_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report_path = temp_path / "scan.json"
            manifest_path = temp_path / "manifest.json"
            report_path.write_text(
                json.dumps(
                    {
                        "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
                        "files": [
                            {
                                "path": "/library/Pictures/imports/IMG_20200101_0001.jpg",
                                "category": "image",
                                "date_source": "filename",
                                "size_bytes": 5,
                                "modified_at": "2020-01-01T00:00:00",
                                "proposed_relative_destination": "Library/2020/2020-01-01_imports/IMG_20200101_0001.jpg",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "apply",
                        "--report",
                        str(report_path),
                        "--dest-root",
                        str(temp_path / "dest"),
                        "--manifest",
                        str(manifest_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Built 1 apply operations and skipped 0 files", output.getvalue())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["operation_count"], 1)

    def test_build_apply_payload_can_include_caches_explicitly(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/.wdmc/thumb.jpg",
                    "category": "cache",
                    "date_source": "filename",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "App-Caches/.wdmc/thumb.jpg",
                }
            ],
        }

        payload = build_apply_payload(
            report_data,
            Path("/tmp/report.json"),
            Path("/dest"),
            include_caches=True,
        )

        self.assertEqual(len(payload["operations"]), 1)
        self.assertEqual(payload["operations"][0]["source"], "/library/Pictures/.wdmc/thumb.jpg")

    def test_build_apply_payload_can_include_google_takeout_explicitly(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/IMG_1.jpg",
                    "category": "image",
                    "date_source": "path",
                    "size_bytes": 1,
                    "modified_at": "2024-01-01T00:00:00",
                    "proposed_relative_destination": "Library/2024/2024-01-01_Photos-from-2024/IMG_1.jpg",
                }
            ],
        }

        payload = build_apply_payload(
            report_data,
            Path("/tmp/report.json"),
            Path("/dest"),
            include_google_takeout=True,
        )

        self.assertEqual(len(payload["operations"]), 1)
        self.assertEqual(
            payload["operations"][0]["source"],
            "/library/Pictures/google-takeout/Takeout/Google Photos/Photos from 2024/IMG_1.jpg",
        )

    def test_build_apply_payload_can_include_pleasantharmony_explicitly(self) -> None:
        report_data = {
            "roots": {"pictures": "/library/Pictures", "videos": "/library/Videos"},
            "files": [
                {
                    "path": "/library/Videos/PleasantHarmony/Hymns/hymns.m4v",
                    "category": "project_video",
                    "date_source": "filename",
                    "size_bytes": 1,
                    "modified_at": "2020-01-01T00:00:00",
                    "proposed_relative_destination": "Projects/PleasantHarmony/Hymns/hymns.m4v",
                }
            ],
        }

        payload = build_apply_payload(
            report_data,
            Path("/tmp/report.json"),
            Path("/dest"),
            include_pleasantharmony=True,
        )

        self.assertEqual(len(payload["operations"]), 1)
        self.assertEqual(
            payload["operations"][0]["source"],
            "/library/Videos/PleasantHarmony/Hymns/hymns.m4v",
        )


if __name__ == "__main__":
    unittest.main()
