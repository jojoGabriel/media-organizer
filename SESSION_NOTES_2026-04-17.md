# Session Notes - 2026-04-17

## Where the project stands

This session resumed from the previously documented non-Takeout duplicate
baseline at:

- `reports/scan-hash-v38.json`

While preparing the next reviewed batch, the live library was found to be ahead
of that saved baseline. A fresh hashed scan was required before continuing.

## What changed during the session

### Re-baseline to live library state

The reviewed `2007-10-27` import-folder duplicate batch was extracted from
`scan-hash-v38.json` and documented in:

- `reports/non-takeout-review-2007-10-27.md`
- `reports/quarantine_non_takeout_2007_10_27.sh`

When the script was attempted, the duplicate-side files were already absent
from `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/` and present in
the home-level quarantine tree. A fresh hashed scan was then written to:

- `reports/scan-hash-v39.json`

Compared with `reports/scan-hash-v38.json`:

- total files: `46875 -> 46834` (`-41`)
- total bytes: `136831618495 -> 136777761159` (`-53857336`)
- images: `12920 -> 12879` (`-41`)
- duplicate groups: `70 -> 29` (`-41`)
- duplicate files: `143 -> 61` (`-82`)

This confirmed the saved notes had fallen behind the actual library state.

### Cleanup applied this session

After re-baselining, the next clean remaining batch in `scan-hash-v39.json`
was:

- `3` groups:
  `/home/gabriel/Pictures/2009/10/27`
  against
  `/home/gabriel/Pictures/Photos/2009/10/27`

Artifacts written for that pass:

- `reports/non-takeout-review-2009-10-27.md`
- `reports/quarantine_non_takeout_2009_10_27.sh`

The duplicate-side files from `/home/gabriel/Pictures/Photos/2009/10/27/`
were quarantined, keeping the canonical copies under
`/home/gabriel/Pictures/2009/10/27/`.

The next reviewed low-risk batch from `scan-hash-v40.json` was:

- `2` groups:
  `/home/gabriel/Pictures/Photos/2007/08/16`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-08-16.md`
- `reports/quarantine_non_takeout_2007_08_16.sh`

The duplicate-side files from
`/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/`
were quarantined, keeping the canonical copies under
`/home/gabriel/Pictures/Photos/2007/08/16/`.

The next reviewed low-risk batch from `scan-hash-v41.json` was:

- `2` groups:
  `/home/gabriel/Pictures/2007/09/25`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-09-25.md`
- `reports/quarantine_non_takeout_2007_09_25.sh`

The duplicate-side files from
`/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/`
were quarantined, keeping the canonical copies under
`/home/gabriel/Pictures/2007/09/25/`.

The next reviewed low-risk batch from `scan-hash-v42.json` was:

- `2` groups:
  `/home/gabriel/Pictures/2007/09/16`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-09-16.md`
- `reports/quarantine_non_takeout_2007_09_16.sh`

The duplicate-side files from
`/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/`
were quarantined, keeping the canonical copies under
`/home/gabriel/Pictures/2007/09/16/`.

The next reviewed low-risk batch from `scan-hash-v43.json` was:

- `2` groups:
  `/home/gabriel/Pictures/Photos/2007/08/30`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-08-30.md`
- `reports/quarantine_non_takeout_2007_08_30.sh`

The duplicate-side files from
`/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/`
were quarantined, keeping the canonical copies under
`/home/gabriel/Pictures/Photos/2007/08/30/`.

The next reviewed low-risk batch from `scan-hash-v44.json` was:

- `1` group:
  `/home/gabriel/Pictures/2008/09/03`
  against
  `/home/gabriel/Pictures/Photos/2008/09/03`

Artifacts written for that pass:

- `reports/non-takeout-review-2008-09-03.md`
- `reports/quarantine_non_takeout_2008_09_03.sh`

The duplicate-side file from `/home/gabriel/Pictures/Photos/2008/09/03/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/2008/09/03/`.

The next reviewed low-risk batch from `scan-hash-v45.json` was:

- `1` group:
  `/home/gabriel/Pictures/2007/10/16`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-10-16.md`
- `reports/quarantine_non_takeout_2007_10_16.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/2007/10/16/`.

The next reviewed low-risk batch from `scan-hash-v46.json` was:

- `1` group:
  `/home/gabriel/Pictures/2007/09/17`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-09-17.md`
- `reports/quarantine_non_takeout_2007_09_17.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/2007/09/17/`.

The next reviewed low-risk batch from `scan-hash-v47.json` was:

- `1` group:
  `/home/gabriel/Pictures/Photos/2007/08/12`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-08-15--19.02.45`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-08-12.md`
- `reports/quarantine_non_takeout_2007_08_12.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-08-15--19.02.45/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/Photos/2007/08/12/`.

The next reviewed low-risk batch from `scan-hash-v48.json` was:

- `1` group:
  `/home/gabriel/Pictures/Photos/2007/08/23`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-08-23.md`
- `reports/quarantine_non_takeout_2007_08_23.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/Photos/2007/08/23/`.

The next reviewed low-risk batch from `scan-hash-v49.json` was:

- `1` group:
  `/home/gabriel/Pictures/Photos/2007/09/04`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-09-04.md`
- `reports/quarantine_non_takeout_2007_09_04.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/Photos/2007/09/04/`.

The next reviewed low-risk batch from `scan-hash-v50.json` was:

- `1` group:
  `/home/gabriel/Pictures/Photos/2007/09/01`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-09-01.md`
- `reports/quarantine_non_takeout_2007_09_01.sh`

Both copies in that pair inferred to `2007-08-31` from metadata even though
one source folder was named `2007/09/01`; the reviewed keep/quarantine choice
still followed the same canonical-folder-versus-timestamped-import pattern.

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/Photos/2007/09/01/`.

The next reviewed low-risk batch from `scan-hash-v51.json` was:

- `1` group:
  `/home/gabriel/Pictures/Photos/2007/08/21`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-08-21.md`
- `reports/quarantine_non_takeout_2007_08_21.sh`

Both copies in that pair inferred to `2007-08-20` from metadata even though
one source folder was named `2007/08/21`; the reviewed keep/quarantine choice
still followed the same canonical-folder-versus-timestamped-import pattern.

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/Photos/2007/08/21/`.

The next reviewed low-risk batch from `scan-hash-v52.json` was:

- `1` group:
  `/home/gabriel/Pictures/2007/11/02`
  against
  `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`

Artifacts written for that pass:

- `reports/non-takeout-review-2007-11-02.md`
- `reports/quarantine_non_takeout_2007_11_02.sh`

The duplicate-side file from
`/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/`
was quarantined, keeping the canonical copy under
`/home/gabriel/Pictures/2007/11/02/`.

The next reviewed special-case batch from `scan-hash-v53.json` was:

- `1` internal renamed-copy group in:
  `/home/gabriel/Pictures/Photos/2009/10/02`

Artifacts written for that pass:

- `reports/non-takeout-review-2009-10-02-internal.md`
- `reports/quarantine_non_takeout_2009_10_02_internal.sh`

The unsuffixed base filename `dscf6043.jpg` was kept, and the suffixed exact
duplicates `dscf6043-1.jpg` and `dscf6043-2.jpg` were quarantined.

The next reviewed special-case batch from `scan-hash-v54.json` was:

- `1` internal renamed-copy group in:
  `/home/gabriel/Pictures/Photos/2009/09/13`

Artifacts written for that pass:

- `reports/non-takeout-review-2009-09-13-internal.md`
- `reports/quarantine_non_takeout_2009_09_13_internal.sh`

The unsuffixed base filename `dscf6018.jpg` was kept, and the suffixed exact
duplicates `dscf6018-1.jpg` and `dscf6018-2.jpg` were quarantined.

The next reviewed special-case batch from `scan-hash-v55.json` was:

- `1` internal modified-name group in:
  `/home/gabriel/Pictures/Photos/2010/05/09`

Artifacts written for that pass:

- `reports/non-takeout-review-2010-05-09-internal.md`
- `reports/quarantine_non_takeout_2010_05_09_internal.sh`

The unsuffixed base filename `dscf6236.jpg` was kept, and the exact duplicate
named `dscf6236 (Modified in GIMP Image Editor).jpg` was quarantined.

The next reviewed special-case batch from `scan-hash-v56.json` was:

- `1` internal modified-name group in:
  `/home/gabriel/Pictures/2011/03/07`

Artifacts written for that pass:

- `reports/non-takeout-review-2011-03-07-internal.md`
- `reports/quarantine_non_takeout_2011_03_07_internal.sh`

The unsuffixed base filename `DSCF6596.JPG` was kept, and the exact duplicate
named `DSCF6596_modified.JPG` was quarantined.

The next reviewed special-case batch from `scan-hash-v57.json` was:

- `1` folder-copy style pair:
  `/home/gabriel/Pictures/NayTay.png`
  against
  `/home/gabriel/Pictures/Wallpapers/NayTay.png`

Artifacts written for that pass:

- `reports/non-takeout-review-naytay-wallpaper.md`
- `reports/quarantine_non_takeout_naytay_wallpaper.sh`

The `Wallpapers` copy was kept as the clearer semantic home, and the root-level
duplicate was quarantined.

The next reviewed special-case batch from `scan-hash-v58.json` was:

- `1` folder-copy style pair in the merged `Jonel` / `Pictures from ates camera`
  context:
  `/home/gabriel/Pictures/Pictures from ates camera/199_0510`
  against
  `/home/gabriel/Pictures/Pictures from ates camera/199_0510 - Copy`

Artifacts written for that pass:

- `reports/non-takeout-review-jonel-ates-camera-copy.md`
- `reports/quarantine_non_takeout_jonel_ates_camera_copy.sh`

The non-copy folder version was kept, and the explicit ` - Copy` folder
duplicate was quarantined.

The next reviewed special-case batch from `scan-hash-v59.json` was:

- `1` three-file `mackinac` group centered on:
  `20190705_105025.jpg`

Artifacts written for that pass:

- `reports/non-takeout-review-mackinac-20190705-105025.md`
- `reports/quarantine_non_takeout_mackinac_20190705_105025.sh`

Per the chosen rule, the unsuffixed filename
`/home/gabriel/Pictures/mackinac/20190705_105025.jpg`
was treated as canonical, and both suffixed `(...)(1)` copies were
quarantined.

The final reviewed batch from `scan-hash-v60.json` was:

- `2` cross-folder canonical-path collision pairs:
  - `/home/gabriel/Pictures/2002/09/30/fl000001.jpg`
    against
    `/home/gabriel/Pictures/Photos/2009/01/28/fl000001.jpg`
  - `/home/gabriel/Pictures/2008/04/18/DSCF1458.JPG`
    against
    `/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1458.JPG`

Artifacts written for that pass:

- `reports/non-takeout-review-final-two-canonical-dated.md`
- `reports/quarantine_non_takeout_final_two_canonical_dated.sh`

Per the chosen rule, the dated canonical folders were preferred and the
`Photos/...` counterparts were quarantined.

## Scan progression

- `scan-hash-v38.json -> scan-hash-v39.json`
  after re-baselining to the current live library:
  total files `46875 -> 46834` (`-41`),
  images `12920 -> 12879` (`-41`),
  duplicate groups `70 -> 29` (`-41`),
  duplicate files `143 -> 61` (`-82`)
- `scan-hash-v39.json -> scan-hash-v40.json`
  after the explicit `2009-10-27` quarantine pass:
  total files `46834 -> 46831` (`-3`),
  total bytes `136777761159 -> 136773670185` (`-4090974`),
  images `12879 -> 12876` (`-3`),
  duplicate groups `29 -> 26` (`-3`),
  duplicate files `61 -> 55` (`-6`)
- `scan-hash-v40.json -> scan-hash-v41.json`
  after the explicit `2007-08-16` quarantine pass:
  total files `46831 -> 46829` (`-2`),
  total bytes `136773670185 -> 136770983646` (`-2686539`),
  images `12876 -> 12874` (`-2`),
  duplicate groups `26 -> 24` (`-2`),
  duplicate files `55 -> 51` (`-4`)
- `scan-hash-v41.json -> scan-hash-v42.json`
  after the explicit `2007-09-25` quarantine pass:
  total files `46829 -> 46827` (`-2`),
  total bytes `136770983646 -> 136768165147` (`-2818499`),
  images `12874 -> 12872` (`-2`),
  duplicate groups `24 -> 22` (`-2`),
  duplicate files `51 -> 47` (`-4`)
- `scan-hash-v42.json -> scan-hash-v43.json`
  after the explicit `2007-09-16` quarantine pass:
  total files `46827 -> 46825` (`-2`),
  total bytes `136768165147 -> 136765378219` (`-2786928`),
  images `12872 -> 12870` (`-2`),
  duplicate groups `22 -> 20` (`-2`),
  duplicate files `47 -> 43` (`-4`)
- `scan-hash-v43.json -> scan-hash-v44.json`
  after the explicit `2007-08-30` quarantine pass:
  total files `46825 -> 46823` (`-2`),
  total bytes `136765378219 -> 136762755377` (`-2622842`),
  images `12870 -> 12868` (`-2`),
  duplicate groups `20 -> 18` (`-2`),
  duplicate files `43 -> 39` (`-4`)
- `scan-hash-v44.json -> scan-hash-v45.json`
  after the explicit `2008-09-03` quarantine pass:
  total files `46823 -> 46822` (`-1`),
  total bytes `136762755377 -> 136762743757` (`-11620`),
  images `12868 -> 12867` (`-1`),
  duplicate groups `18 -> 17` (`-1`),
  duplicate files `39 -> 37` (`-2`)
- `scan-hash-v45.json -> scan-hash-v46.json`
  after the explicit `2007-10-16` quarantine pass:
  total files `46822 -> 46821` (`-1`),
  total bytes `136762743757 -> 136761341945` (`-1401812`),
  images `12867 -> 12866` (`-1`),
  duplicate groups `17 -> 16` (`-1`),
  duplicate files `37 -> 35` (`-2`)
- `scan-hash-v46.json -> scan-hash-v47.json`
  after the explicit `2007-09-17` quarantine pass:
  total files `46821 -> 46820` (`-1`),
  total bytes `136761341945 -> 136760022946` (`-1318999`),
  images `12866 -> 12865` (`-1`),
  duplicate groups `16 -> 15` (`-1`),
  duplicate files `35 -> 33` (`-2`)
- `scan-hash-v47.json -> scan-hash-v48.json`
  after the explicit `2007-08-12` quarantine pass:
  total files `46820 -> 46819` (`-1`),
  total bytes `136760022946 -> 136758684140` (`-1338806`),
  images `12865 -> 12864` (`-1`),
  duplicate groups `15 -> 14` (`-1`),
  duplicate files `33 -> 31` (`-2`)
- `scan-hash-v48.json -> scan-hash-v49.json`
  after the explicit `2007-08-23` quarantine pass:
  total files `46819 -> 46818` (`-1`),
  total bytes `136758684140 -> 136757352409` (`-1331731`),
  images `12864 -> 12863` (`-1`),
  duplicate groups `14 -> 13` (`-1`),
  duplicate files `31 -> 29` (`-2`)
- `scan-hash-v49.json -> scan-hash-v50.json`
  after the explicit `2007-09-04` quarantine pass:
  total files `46818 -> 46817` (`-1`),
  total bytes `136757352409 -> 136756045424` (`-1306985`),
  images `12863 -> 12862` (`-1`),
  duplicate groups `13 -> 12` (`-1`),
  duplicate files `29 -> 27` (`-2`)
- `scan-hash-v50.json -> scan-hash-v51.json`
  after the explicit `2007-09-01` quarantine pass:
  total files `46817 -> 46816` (`-1`),
  total bytes `136756045424 -> 136754674541` (`-1370883`),
  images `12862 -> 12861` (`-1`),
  duplicate groups `12 -> 11` (`-1`),
  duplicate files `27 -> 25` (`-2`)
- `scan-hash-v51.json -> scan-hash-v52.json`
  after the explicit `2007-08-21` quarantine pass:
  total files `46816 -> 46815` (`-1`),
  total bytes `136754674541 -> 136753303428` (`-1371113`),
  images `12861 -> 12860` (`-1`),
  duplicate groups `11 -> 10` (`-1`),
  duplicate files `25 -> 23` (`-2`)
- `scan-hash-v52.json -> scan-hash-v53.json`
  after the explicit `2007-11-02` quarantine pass:
  total files `46815 -> 46814` (`-1`),
  total bytes `136753303428 -> 136751870371` (`-1433057`),
  images `12860 -> 12859` (`-1`),
  duplicate groups `10 -> 9` (`-1`),
  duplicate files `23 -> 21` (`-2`)
- `scan-hash-v53.json -> scan-hash-v54.json`
  after the `2009-10-02` internal renamed-copy pass:
  total files `46814 -> 46812` (`-2`),
  total bytes `136751870371 -> 136749137321` (`-2733050`),
  images `12859 -> 12857` (`-2`),
  duplicate groups `9 -> 8` (`-1`),
  duplicate files `21 -> 18` (`-3`)
- `scan-hash-v54.json -> scan-hash-v55.json`
  after the `2009-09-13` internal renamed-copy pass:
  total files `46812 -> 46810` (`-2`),
  total bytes `136749137321 -> 136746379783` (`-2757538`),
  images `12857 -> 12855` (`-2`),
  duplicate groups `8 -> 7` (`-1`),
  duplicate files `18 -> 15` (`-3`)
- `scan-hash-v55.json -> scan-hash-v56.json`
  after the `2010-05-09` internal modified-name pass:
  total files `46810 -> 46809` (`-1`),
  total bytes `136746379783 -> 136745087162` (`-1292621`),
  images `12855 -> 12854` (`-1`),
  duplicate groups `7 -> 6` (`-1`),
  duplicate files `15 -> 13` (`-2`)
- `scan-hash-v56.json -> scan-hash-v57.json`
  after the `2011-03-07` internal modified-name pass:
  total files `46809 -> 46808` (`-1`),
  total bytes `136745087162 -> 136743730712` (`-1356450`),
  images `12854 -> 12853` (`-1`),
  duplicate groups `6 -> 5` (`-1`),
  duplicate files `13 -> 11` (`-2`)
- `scan-hash-v57.json -> scan-hash-v58.json`
  after the `NayTay` wallpaper-root dedupe pass:
  total files `46808 -> 46807` (`-1`),
  total bytes `136743730712 -> 136743244494` (`-486218`),
  images `12853 -> 12852` (`-1`),
  duplicate groups `5 -> 4` (`-1`),
  duplicate files `11 -> 9` (`-2`)
- `scan-hash-v58.json -> scan-hash-v59.json`
  after the `Jonel / ates camera` copy-folder dedupe pass:
  total files `46807 -> 46806` (`-1`),
  total bytes `136743244494 -> 136740366096` (`-2878398`),
  images `12852 -> 12851` (`-1`),
  duplicate groups `4 -> 3` (`-1`),
  duplicate files `9 -> 7` (`-2`)
- `scan-hash-v59.json -> scan-hash-v60.json`
  after the `mackinac` unsuffixed-canonical pass:
  total files `46806 -> 46804` (`-2`),
  total bytes `136740366096 -> 136735876576` (`-4489520`),
  images `12851 -> 12849` (`-2`),
  duplicate groups `3 -> 2` (`-1`),
  duplicate files `7 -> 4` (`-3`)
- `scan-hash-v60.json -> scan-hash-v61.json`
  after the final canonical-dated-folder pass:
  total files `46804 -> 46802` (`-2`),
  total bytes `136735876576 -> 136734463352` (`-1413224`),
  images `12849 -> 12847` (`-2`),
  duplicate groups `2 -> 0` (`-2`),
  duplicate files `4 -> 0` (`-4`)

Current scan baseline:

- `reports/scan-hash-v61.json`

## Current remaining duplicate shape

From `scan-hash-v61.json`:

- duplicate groups remaining: `0`
- duplicate files remaining: `0`

Remaining duplicate shape:

- no duplicate groups remain in the hashed scan baseline

## Best next step

Use `reports/scan-hash-v61.json` as the new clean baseline for any future
organizer work. Duplicate cleanup from this hashed scan set is complete.
