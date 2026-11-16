---
name: ICP 豁免声明
description: >-
  Use when the user wants to apply for an Apple App Store China ICP filing
  exemption, generate or revise a bilingual exemption declaration PDF, or draft
  the follow-up reply after uploading it.
---
# Apple ICP exemption declaration

Generate a one-page bilingual (Chinese + English) ICP filing exemption letter for a standalone iOS app, and/or help with the Developer Support request. Use `generate.py` in this skill's directory for the PDF layout.

## Privacy and scope

This is a shared template. Do not put personal facts in this directory or its files: no real legal names, Team IDs, App IDs, case IDs, bundle IDs, personal paths, contact details, or signature images. Resolve those per run from the user, verified app facts, and private memory. Use placeholders in examples. Do not hardcode a previous app's facts.

The letter is a legal statement; never invent network, server, or privacy claims. An approval is only that case's outcome, not a guarantee for other apps or future requests.

## Gather facts

Collect for this app:

- Its own Developer Support case ID, if one exists.
- Team ID and account holder's legal name in Chinese and English; printed legal name is typically `中文名 (PINYIN IN CAPITALS)`.
- App Store display name, numeric App ID (Apple ID), and Bundle ID. A Bundle ID alone is not a substitute for the numeric App ID. Apple has returned letters missing it; include it whenever available.
- Date in the user's timezone.
- Accurate app purpose, networking behavior, and data collection facts.

Do not infer a Chinese legal name from pinyin. Reuse a verified name from the user's earlier documents or ask.

For a new app or changed facts, verify the Bundle ID against the main Xcode target's `PRODUCT_BUNDLE_IDENTIFIER` (ignore test targets). Resolve conflicting main-target IDs. Verify networking and privacy wording against the README, source, and Info.plist, including ATS, Bonjour/local-network permissions, URL schemes, and third-party SDKs. Follow the applicable repository-access skills; do not clone a repository just for this task.

For a continuation of the same application, reuse previously verified, user-accepted wording if there is no indication the app facts changed. Re-verify if information is missing, changed, or inconsistent. Do not repeatedly scan source merely to change the case number or date.

Common traps:

- Local HTTP, LAN, and P2P transfer are network activity: do not claim such an app makes no network requests.
- Fetching iCloud or Photo Library originals may use the network even without an app backend.
- Analytics, crash reporters, and login SDKs may involve network activity or data collection.

If proposed wording contradicts verified behavior, tell the user and resolve it before generating a signed letter. Do not silently sign materially changed claims the user has not accepted.

## Request and case handling

The working route is an Apple Developer Support request followed by a signed letter and secure upload.

If this app has no case:

1. Prepare the request through [Apple Developer Support](https://developer.apple.com/contact/topic/SC1103/subtopic/30023/solution/CONTACT.EML.GEN/details). If unavailable, use [Contact Apple Developer](https://developer.apple.com/contact/).
2. Draft in the requested language, including Team ID, legal name, app name, numeric App ID when available, Bundle ID, and an exemption reason matching the letter. Preparing text does not authorize submitting a form.
3. The App ID field expects the numeric Apple ID, not the Bundle ID or an account email. Fill other fields according to the actual form; do not assume a field is unrelated from its label alone.

Default to one app per case and one letter per app. Reuse the existing case for the same app instead of opening a duplicate. Another app needs its own request and case number; do not copy another app's case ID. Combine apps only if Apple explicitly authorizes that arrangement, then provide a separate letter for each.

Apple typically sends a secure document-upload link separately. Use the link from the actual support correspondence, not an invented or reconstructed URL. After uploading, reply to the case email.

When drafting a reply:

- If the user requests copy only, provide the text in chat and do not send it. For an actual send request, follow the applicable message drafting and approval rules.
- Say the document has been uploaded only when confirmed by the user or a verified upload result. Otherwise clearly label the draft as intended to be sent after upload.
- Include app name, numeric App ID, case reference, a short confirmation of the document's contents, and an offer to provide further information. Use the requested language and the actual support contact's name if known.

## Required letter contents

- Team ID and account holder's legal name.
- App Store name, numeric App ID (Apple ID), and Bundle ID.
- Request for an ICP filing exception for this standalone app.
- Confirmation that the account holder understands the relevant PRC laws and regulations and accepts all legal responsibility for false statements.
- Signature, printed legal name, and date.

## Layout and wording

Match a supplied reference letter when possible; otherwise use the helper's single-page A4 layout with Noto Sans CJK SC, centered bilingual title, addressee and case ID, identifying fields, Chinese and English bodies, signature line, printed name, and date.

Titles: `ICP 备案豁免申请声明` / `ICP Filing Exemption Declaration`.

Standard framing (substitute gathered facts; retain the legal acknowledgement):

- Chinese request: `本人{name}，作为上述 Apple 开发者账户的持有人，特此申请就上述独立 App「{app}」获得 ICP 备案要求的例外豁免。`
- English request: `I, {name_en}, the Account Holder of the Apple Developer account above, hereby request an exception to the ICP filing requirement for the standalone app "{app}" (App ID: {apple_id}; Bundle ID: {bundle}).`
- Chinese close: `本人已了解中华人民共和国关于互联网信息服务及 ICP 备案的相关法律法规，并确认上述内容真实、准确。如出现任何虚假陈述，本人同意承担全部法律责任。`
- English close: `I understand the relevant laws and regulations of the People's Republic of China regarding internet information services and ICP filing, and I confirm that the statements above are true and accurate. I agree to bear all legal responsibility in the event of any false statement.`

Write matching Chinese and English purpose paragraphs from verified facts. If a numeric App ID genuinely does not yet exist, omit that part rather than inventing one; add it as soon as available. Tighten spacing if needed to fit one page; never remove required statements to fit.

## Generate

```bash
python3 generate.py \
  --case-id CASE_ID \
  --team-id TEAM_ID \
  --legal-name-cn NAME \
  --legal-name-en "Name En" \
  --app-name APP \
  --app-name-display "APP（English）" \
  --apple-id NUMERIC_APPLE_ID \
  --bundle-id BUNDLE_ID \
  --cn-purpose "该 App 为…" \
  --en-purpose "The app is…" \
  --date YYYY-MM-DD \
  --out-dir /workspace/deliverables/icp \
  --basename "APP_ICP豁免声明"
```

Always pass `--apple-id` when known: the helper includes it in both the identifying fields and the default English request. Always retain the unsigned PDF. Add `--signature /path/to/signature.png` only with authorization for this letter.

The helper versions filenames instead of overwriting and produces PNG previews. If Chrome printing is unavailable, use an equivalent that preserves A4 layout and fonts.

## Signature

Apply a signature only when the account holder explicitly asks to sign the letter concerned. A saved default image is not permission to sign unrequested or future legal documents. Never draw, trace, or invent a signature.

Resolve the image in this order:

1. A new image or path supplied for this letter.
2. The saved default location in private memory, copying from the user's computer if needed.
3. Ask for an image or path if neither is available.

Keep the default location in private memory, never in the skill. Keep the image outside the skill directory. If the user explicitly replaces the default, update private memory; a one-off image does not replace it. Clarify only when replacement intent is ambiguous.

Use `--prepare-signature IN OUT` for HEIC/PNG preprocessing: convert to transparent PNG, remove paper background and faint ruling, and crop whitespace without altering the signature strokes. Place it on the signature line at about 15 mm tall. Verify that there is no white box or overlapping text.

## Verify and deliver

1. Check PDF page count, extracted text, and PNG preview: one A4 page; correct app, case, numeric App ID, Team ID, names, date, legal statements, and signature when authorized.
2. Send the PDF and preview in chat. Quote Chinese and English purpose paragraphs only when new or changed; for unchanged accepted wording, briefly confirm reuse.
3. If a preferred output folder is authorized, copy files there without overwriting. A failure to copy must not block chat delivery; report the actual result.
4. Remind the user to upload through Apple's secure link and then reply to the case email. Do not imply generation or copying completed the upload.
