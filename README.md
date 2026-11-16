# ICP filing exemption declaration

`generate.py` lays out a one-page A4 PDF for one standalone iOS app. The letter is bilingual. Its titles are `ICP 备案豁免申请声明` and `ICP Filing Exemption Declaration`. This repository also contains the Cursor agent skill in `SKILL.md`. The script lays out only the facts you pass in. The script does not submit the request to Apple.

## Install the skill

Keep `generate.py` in the same directory as `SKILL.md`. Cursor loads `SKILL.md` from a skill directory. Clone this repository there for a user-level skill:

```bash
git clone https://github.com/0summer0/icp-exemption-skill.git ~/.cursor/skills/icp-exemption
```

For one project, use `.cursor/skills/icp-exemption/` and keep the two files side by side.

Ask the agent to draft or generate an ICP filing exemption declaration for one app. The skill collects that app's facts and runs `generate.py` from the skill directory. Draft text is not a submitted form. Confirm the send or the upload yourself before it goes out.

Do not commit real names, Team IDs, numeric App IDs, case IDs, bundle IDs, contact details, personal paths, or signature images to this repository.

## Generate a letter

Install the dependencies below before you generate a PDF. Every value in the sample is a placeholder. Replace each value with this application's facts. At run time, write `--cn-purpose` in Chinese. The sample strings in this README stay in English.

```bash
python3 generate.py \
  --case-id CASE_ID \
  --team-id TEAM_ID \
  --legal-name-cn NAME \
  --legal-name-en "Name En" \
  --app-name APP \
  --app-name-display "APP (English)" \
  --apple-id NUMERIC_APPLE_ID \
  --bundle-id BUNDLE_ID \
  --cn-purpose "CHINESE_PURPOSE" \
  --en-purpose "The app is a placeholder." \
  --date YYYY-MM-DD \
  --out-dir OUT_DIR \
  --basename "APP_ICP豁免声明"
```

If you omit `--out-dir`, the script writes to `/workspace/deliverables/icp`. Pass an `OUT_DIR` outside this repository.

The script always keeps the unsigned PDF. That file is `{basename}_待签名.pdf`. If that name exists, the script tries `_v2`, then `_v3`, and stops at the first free name.

Add a signature only when the account holder explicitly asks to sign this letter. Keep the image outside the skill directory. Do not commit the image.

```bash
python3 generate.py --prepare-signature IN_IMAGE OUT.png
```

`--prepare-signature` writes a transparent PNG and then exits. It removes the paper background and faint ruling, crops the surrounding whitespace, and leaves the signature strokes unchanged. Run the generate command again with `--signature OUT.png` to write `{basename}_已签名.pdf`.

## Dependencies

PDF generation needs Python 3 and a browser.

The main path uses only the Python standard library: `argparse`, `html`, `shutil`, `subprocess`, `sys`, `datetime`, and `pathlib`.

Put Chrome or Chromium on `PATH` under one of these names: `google-chrome`, `google-chrome-stable`, `chromium`, or `chromium-browser`. The script prints the HTML to PDF in headless mode.

The CSS requests `Noto Sans CJK SC`, then `Noto Sans CJK SC Regular`, then `sans-serif`. Install `Noto Sans CJK SC` so the browser can use that family. `generate.py` sets `FONT_REG` and `FONT_BLD` to Noto file paths and never reads them. A missing font does not stop the script. Chinese text then uses the fallback font.

These tools are optional:

- `pdftoppm` from Poppler writes the PNG preview. If `pdftoppm` is missing, the script prints a warning to standard error and continues.
- Pillow is required only for `--prepare-signature`.
- `pillow-heif`, or the `heif-convert` command, is required only when the source image is HEIC or HEIF.

## Use one case per app

Use one Apple Developer Support case for one app, and one letter for that app. A different app needs its own request and its own case ID. Do not copy another app's case ID. Put more than one app in a case only when Apple explicitly allows that arrangement. Still write a separate letter for each app.

`--apple-id` is the numeric Apple ID from the App Store. That number is the App ID the form asks for. A bundle ID does not replace the numeric Apple ID. Pass `--apple-id` when you know the number. The script writes the ID in the field block and in the default English request. If the numeric App ID does not exist yet, omit the flag. Do not invent a number. Add the flag as soon as the ID exists.

## Keep signatures private

Pass the legal name, the case identifiers, and the signature image at run time. Keep them outside this repository and outside the skill directory. A saved default signature image is not permission to sign an unrequested letter or a later letter. Do not draw, trace, or invent a signature.

## Treat approval as case-specific

An approval covers that case only. That approval does not extend to another app or to a later request. Creating or copying the PDF does not upload it. Upload through the secure link in the support reply. Then reply to that case email.

The signer is responsible for the legal acknowledgement in the letter. This README and `generate.py` are not legal advice. Write the purpose, network, and privacy statements from facts you have checked. Do not invent those statements.
