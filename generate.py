#!/usr/bin/env python3
"""Generate a one-page A4 bilingual Apple ICP exemption declaration PDF."""
from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


FONT_REG = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
FONT_BLD = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")

CSS = """
@page {
  size: A4;
  margin: 18mm 18mm 18mm 18mm;
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  background: #fff;
  color: #000;
  font-family: "Noto Sans CJK SC", "Noto Sans CJK SC Regular", sans-serif;
  font-size: 16px;
  line-height: 1.38;
  font-weight: 400;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.nowrap { white-space: nowrap; }
h1 {
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin: 0 0 2px 0;
  letter-spacing: 0;
}
h2 {
  font-size: 20px;
  font-weight: 700;
  text-align: center;
  margin: 0 0 22px 0;
}
.to { margin: 0 0 16px 0; }
.to p { margin: 0; line-height: 1.45; }
.meta {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 18px 0;
}
.meta td {
  padding: 3.5px 0;
  vertical-align: baseline;
  font-size: 18px;
  line-height: 1.35;
}
.meta td.k {
  width: 62%;
  white-space: nowrap;
  padding-right: 8px;
}
.meta td.v { width: 38%; }
p.body {
  margin: 0 0 10px 0;
  text-align: justify;
  text-justify: inter-ideograph;
}
.sig { margin-top: 28px; }
.sig-row {
  display: flex;
  align-items: center;
  min-height: 16mm;
  margin: 0 0 14px 0;
}
.sig-row .label { white-space: nowrap; }
.sig-img {
  height: 15mm;
  width: auto;
  margin-left: 8px;
  display: block;
}
.sig p { margin: 0 0 10px 0; }
"""


def e(text: str) -> str:
    return html.escape(text, quote=True)


def format_date(value: str) -> str:
    d = datetime.strptime(value, "%Y-%m-%d").date()
    months = (
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    )
    return f"{d.year} 年 {d.month} 月 {d.day} 日 ({months[d.month - 1]} {d.day}, {d.year})"


def default_printed_name(name_cn: str, name_en: str) -> str:
    parts = name_en.replace("-", " ").split()
    pinyin = " ".join(p.upper() for p in parts if p)
    return f"{name_cn} ({pinyin})" if pinyin else name_cn


def versioned_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    n = 2
    while True:
        candidate = path.with_name(f"{stem}_v{n}{suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def chrome_bin() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chrome/Chromium is required for HTML-to-PDF (google-chrome or chromium).")


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome_bin(),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--disable-extensions",
        "--no-first-run",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def pdf_preview(pdf_path: Path) -> Path:
    png = pdf_path.with_suffix(".png")
    if shutil.which("pdftoppm"):
        dest = pdf_path.with_name(pdf_path.stem)
        subprocess.run(
            ["pdftoppm", "-png", "-singlefile", "-r", "144", str(pdf_path), str(dest)],
            check=True,
            capture_output=True,
            text=True,
        )
        return png
    print("warning: pdftoppm not found, skipped PNG preview", file=sys.stderr)
    return png


def write_html(
    path: Path,
    *,
    case_id: str,
    team_id: str,
    legal_name_cn: str,
    legal_name_en: str,
    printed_name: str,
    app_name: str,
    app_name_display: str,
    bundle_id: str,
    apple_id: str,
    cn_request: str,
    cn_purpose: str,
    cn_close: str,
    en_request: str,
    en_purpose: str,
    en_close: str,
    date_text: str,
    signature: Path | None,
) -> None:
    if case_id:
        to_cn = f"致：Apple 开发者支持（案例编号 {e(case_id)}）"
        to_en = f"To: Apple Developer Support (Case ID: {e(case_id)})"
    else:
        to_cn = "致：Apple 开发者支持"
        to_en = "To: Apple Developer Support"

    if signature:
        sig_html = (
            f'<img class="sig-img" src="{signature.resolve().as_uri()}" alt="Signature">'
        )
    else:
        sig_html = ""

    apple_row = (
        f'    <tr><td class="k">App ID (Apple ID)：</td><td class="v">{e(apple_id)}</td></tr>\n'
        if apple_id else ""
    )
    if not apple_id:
        apple_row = ""
    title = f"{app_name} ICP 备案豁免申请声明"
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{e(title)}</title>
<style>
{CSS}
</style>
</head>
<body>
  <h1>ICP 备案豁免申请声明</h1>
  <h2>ICP Filing Exemption Declaration</h2>
  <div class="to">
    <p>{to_cn}</p>
    <p>{to_en}</p>
  </div>
  <table class="meta">
    <tr><td class="k">团队 ID / Team ID：</td><td class="v">{e(team_id)}</td></tr>
    <tr><td class="k">账户持有人法定姓名 / Account Holder Legal Name：</td><td class="v">{e(legal_name_cn)} ({e(legal_name_en)})</td></tr>
    <tr><td class="k">App 名称 / App Name：</td><td class="v">{e(app_name_display)}</td></tr>
{apple_row}    <tr><td class="k">Bundle ID：</td><td class="v">{e(bundle_id)}</td></tr>
  </table>
  <p class="body">{e(cn_request)}</p>
  <p class="body">{e(cn_purpose)}</p>
  <p class="body">{e(cn_close)}</p>
  <p class="body">{e(en_request)} {e(en_purpose)}</p>
  <p class="body">{e(en_close)}</p>
  <div class="sig">
    <div class="sig-row">
      <span class="label">账户持有人签名 / Signature：</span>
      {sig_html}
    </div>
    <p>正楷法定姓名 / Printed Legal Name：{e(printed_name)}</p>
    <p>日期 / Date：{e(date_text)}</p>
  </div>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")


def prepare_signature(src: Path, dest: Path) -> Path:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is required to prepare a signature image.") from exc

    image = _open_image(src).convert("RGBA")
    rgb = image.convert("RGB")
    # Light paper and faint ruling: high luminance, low saturation.
    pixels = list(image.getdata())
    rgb_pixels = list(rgb.getdata())
    out = []
    for (r, g, b, a), (rr, gg, bb) in zip(pixels, rgb_pixels):
        luma = 0.2126 * rr + 0.7152 * gg + 0.0722 * bb
        mx, mn = max(rr, gg, bb), min(rr, gg, bb)
        sat = 0 if mx == 0 else (mx - mn) / mx
        if luma >= 210 and sat <= 0.18:
            out.append((r, g, b, 0))
        elif luma >= 185 and sat <= 0.12:
            out.append((r, g, b, 0))
        else:
            out.append((r, g, b, a))
    image.putdata(out)

    bbox = image.getbbox()
    if not bbox:
        raise SystemExit(f"Signature image is empty after background removal: {src}")
    pad = 16
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(image.width, bbox[2] + pad)
    bottom = min(image.height, bbox[3] + pad)
    image = image.crop((left, top, right, bottom))
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "PNG")
    return dest


def _open_image(src: Path):
    from PIL import Image

    suffix = src.suffix.lower()
    if suffix in {".heic", ".heif"}:
        try:
            from pillow_heif import register_heif_opener

            register_heif_opener()
        except ImportError:
            converted = src.with_suffix(".converted.png")
            if shutil.which("heif-convert"):
                subprocess.run(["heif-convert", str(src), str(converted)], check=True)
                return Image.open(converted)
            raise SystemExit(
                "Cannot read HEIC: install pillow-heif or heif-convert."
            )
    return Image.open(src)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prepare-signature", nargs=2, metavar=("IN", "OUT"),
                   help="Convert a signature image (HEIC/PNG) to a transparent PNG and exit.")
    p.add_argument("--case-id", default="", help="Apple Developer Support case ID, if any.")
    p.add_argument("--team-id", help="Apple Developer Team ID.")
    p.add_argument("--legal-name-cn", help="Account holder legal name in Chinese.")
    p.add_argument("--legal-name-en", help="Account holder legal name in English.")
    p.add_argument("--printed-name", help="Printed legal name; default is 中文名 (ENGLISH).")
    p.add_argument("--app-name", help="App name used in the body, e.g. MyApp.")
    p.add_argument("--app-name-display", help="Name shown in the field block; defaults to --app-name.")
    p.add_argument("--bundle-id", help="Main app Bundle ID.")
    p.add_argument("--apple-id", default="", help="Numeric App Store Apple ID (App ID Apple asks for).")
    p.add_argument("--cn-purpose", help="Chinese paragraph describing the app and exemption basis.")
    p.add_argument("--en-purpose", help="English paragraph describing the app and exemption basis.")
    p.add_argument("--cn-request", help="Override the standard Chinese request sentence.")
    p.add_argument("--en-request", help="Override the standard English request sentence.")
    p.add_argument("--cn-close", help="Override the standard Chinese legal acknowledgement.")
    p.add_argument("--en-close", help="Override the standard English legal acknowledgement.")
    p.add_argument("--date", default=date.today().isoformat(), help="Letter date, YYYY-MM-DD.")
    p.add_argument("--signature", help="Prepared transparent signature PNG. Omit for unsigned only.")
    p.add_argument("--out-dir", type=Path, default=Path("/workspace/deliverables/icp"))
    p.add_argument("--basename", help='Output stem, e.g. "MyApp_ICP豁免声明".')
    p.add_argument("--work-dir", type=Path, help="Directory for intermediate HTML. Defaults to out-dir/build.")
    return p


def require_generate_args(args: argparse.Namespace) -> None:
    missing = [
        name for name in (
            "team_id", "legal_name_cn", "legal_name_en", "app_name",
            "bundle_id", "cn_purpose", "en_purpose",
        )
        if not getattr(args, name)
    ]
    if missing:
        raise SystemExit("Missing required arguments: " + ", ".join("--" + n.replace("_", "-") for n in missing))


def main() -> None:
    args = build_parser().parse_args()
    if args.prepare_signature:
        src, dest = Path(args.prepare_signature[0]), Path(args.prepare_signature[1])
        out = prepare_signature(src, dest)
        print(out)
        return

    require_generate_args(args)
    app_name_display = args.app_name_display or args.app_name
    printed_name = args.printed_name or default_printed_name(args.legal_name_cn, args.legal_name_en)
    basename = args.basename or f"{args.app_name}_ICP豁免声明"
    out_dir: Path = args.out_dir
    work_dir: Path = args.work_dir or (out_dir / "build")
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    cn_request = args.cn_request or (
        f"本人{args.legal_name_cn}，作为上述 Apple 开发者账户的持有人，"
        f"特此申请就上述独立 App「{args.app_name}」获得 ICP 备案要求的例外豁免。"
    )
    en_request = args.en_request or (
        f'I, {args.legal_name_en}, the Account Holder of the Apple Developer account above, '
        f'hereby request an exception to the ICP filing requirement for the standalone app "{args.app_name}" '
        + (f"(App ID: {args.apple_id}; Bundle ID: {args.bundle_id})." if args.apple_id else f"(Bundle ID: {args.bundle_id}).")
    )
    cn_close = args.cn_close or (
        "本人已了解中华人民共和国关于互联网信息服务及 ICP 备案的相关法律法规，"
        "并确认上述内容真实、准确。如出现任何虚假陈述，本人同意承担全部法律责任。"
    )
    en_close = args.en_close or (
        "I understand the relevant laws and regulations of the People's Republic of China "
        "regarding internet information services and ICP filing, and I confirm that the statements "
        "above are true and accurate. I agree to bear all legal responsibility in the event of any false statement."
    )
    date_text = format_date(args.date)
    common = dict(
        case_id=args.case_id,
        team_id=args.team_id,
        legal_name_cn=args.legal_name_cn,
        legal_name_en=args.legal_name_en,
        printed_name=printed_name,
        app_name=args.app_name,
        app_name_display=app_name_display,
        bundle_id=args.bundle_id,
        apple_id=args.apple_id,
        cn_request=cn_request,
        cn_purpose=args.cn_purpose,
        cn_close=cn_close,
        en_request=en_request,
        en_purpose=args.en_purpose,
        en_close=en_close,
        date_text=date_text,
    )

    unsigned_pdf = versioned_path(out_dir / f"{basename}_待签名.pdf")
    unsigned_html = work_dir / f"{unsigned_pdf.stem}.html"
    write_html(unsigned_html, signature=None, **common)
    html_to_pdf(unsigned_html, unsigned_pdf)
    pdf_preview(unsigned_pdf)
    print(unsigned_pdf)

    if args.signature:
        signature = Path(args.signature)
        if not signature.exists():
            raise SystemExit(f"Signature file not found: {signature}")
        signed_pdf = versioned_path(out_dir / f"{basename}_已签名.pdf")
        signed_html = work_dir / f"{signed_pdf.stem}.html"
        write_html(signed_html, signature=signature, **common)
        html_to_pdf(signed_html, signed_pdf)
        pdf_preview(signed_pdf)
        print(signed_pdf)


if __name__ == "__main__":
    main()
