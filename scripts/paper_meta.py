#!/usr/bin/env python3
"""Deterministic map of a paper PDF: metadata hints and where things are.

Usage:
    python3 -I paper_meta.py paper.pdf                 # human-readable map
    python3 -I paper_meta.py paper.pdf --json          # same as JSON
    python3 -I paper_meta.py paper.pdf --find "ablation|seed"   # grep with page numbers
    python3 -I paper_meta.py paper.pdf --page 7        # print one page of text
    python3 -I paper_meta.py paper.pdf --text-out paper.txt     # dump all text (pages separated by \\f)

Text extraction uses `pdftotext` (poppler) if present, else `pypdf`. No reasoning is done
here; it only locates sections, figures, tables, algorithms, equations, ids, and venue hints
so the reviewer knows which pages to read. Captions in two-column layouts may be garbled;
treat the page numbers as reliable and the caption text as a hint.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

VENUE_PAT = re.compile(
    r"(Published as a conference paper at|Proceedings of|Advances in Neural Information|"
    r"\bNeurIPS\b|\bNIPS\b|\bICML\b|\bICLR\b|\bACL\b|\bEMNLP\b|\bNAACL\b|\bCVPR\b|\bICCV\b|"
    r"\bECCV\b|\bAAAI\b|\bIJCAI\b|\bKDD\b|\bWWW\b|\bSIGIR\b|\bCOLM\b|\bCoRL\b|\bAISTATS\b|"
    r"\bUAI\b|\bJMLR\b|\bTMLR\b|Transactions on|Under review|Preprint|Accepted at|"
    r"Workshop|arXiv preprint|Technical Report|Submitted to)",
    re.I,
)
NUM_HEADING_PAT = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+(.+)$")
ROMAN = r"(?:X{0,2}(?:IX|IV|V?I{0,3}))"
ROMAN_HEADING_PAT = re.compile(r"^\s*(" + ROMAN + r")\.\s+([A-Z].+)$")           # IEEE: "IV. STAGE 2: ..."
ROMAN_SUB_PAT = re.compile(r"^\s*([A-H])\.\s+([A-Z][^.]{2,80})$")                   # IEEE: "A. Research Method"
LETTER_HEADING_PAT = re.compile(r"^\s*([A-H](?:\.\d{1,2}){0,2})\.?\s+(.+)$")
BARE_NUM_PAT = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s*$")
BARE_LETTER_PAT = re.compile(r"^\s*([A-H](?:\.\d{1,2}){0,2})\.?\s*$")
NAMED_SECTION_PAT = re.compile(
    r"^\s*(Abstract|Introduction|Background|Preliminaries|Related Work|Method(?:s|ology)?|"
    r"Approach|Experiments?|Experimental (?:Setup|Results)|Results|Analysis|Discussion|"
    r"Limitations|Conclusions?|Broader Impacts?|Ethics Statement|Acknowledg(?:e)?ments?|"
    r"References|Appendix|Appendices|Supplementary Material)\s*$",
    re.I,
)
FIG_PAT = re.compile(r"^\s*(?:Figure|Fig\.?)[\s\u00a0]*(\d+)\s*[.:|]\s*(.*)$")
TAB_PAT = re.compile(r"^\s*Table\s*(\d+)\s*[.:|]\s*(.*)$")
TAB_ROMAN_PAT = re.compile(r"^\s*TABLE\s+(" + ROMAN + r")\s*[.:]?\s*(.*)$")        # IEEE: "TABLE IV" (caption on next line)
ALG_PAT = re.compile(r"^\s*Algorithm\s*(\d+)\s*[.:|]?\s*(.*)$")
THM_PAT = re.compile(r"^\s*((?:Theorem|Lemma|Proposition|Corollary|Definition|Assumption)\s*\d+(?:\.\d+)*)\s*[.:(]?\s*(.*)$")
# Two-column layouts can put a caption mid-line; only trust a colon there ("Table 1: ...").
FIG_INLINE_PAT = re.compile(r"(?:Figure|Fig\.?)[\s\u00a0]*(\d+)\s*[.:]\s+([A-Z].*)$")
TAB_INLINE_PAT = re.compile(r"Table\s*(\d+)\s*:\s*(.*)$")
EQ_PAT = re.compile(r"\((\d{1,3})\)\s*$")
ARXIV_PAT = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?", re.I)
DOI_PAT = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)")
URL_PAT = re.compile(r"https?://(?:github\.com|huggingface\.co|[a-z0-9.-]+\.github\.io)/[^\s)]+", re.I)
CODE_PAT = re.compile(r"(code|models?|data(?:set)?)\s+(?:is|are|will be)?\s*(?:publicly\s+)?available", re.I)


def extract_pages(pdf: Path) -> list[str]:
    if shutil.which("pdftotext"):
        out = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        pages = out.split("\f")
        if pages and not pages[-1].strip():
            pages = pages[:-1]
        return pages
    try:
        import pypdf  # type: ignore
    except ImportError:
        sys.exit("Need `pdftotext` (poppler) on PATH or `pip install pypdf`.")
    reader = pypdf.PdfReader(str(pdf))
    return [(p.extract_text() or "") for p in reader.pages]


def title_like(ln: str) -> bool:
    """A heading: short, starts with a capital, no sentence punctuation at the end."""
    ln = ln.strip()
    words = ln.split()
    alpha_words = [w for w in words if re.fullmatch(r"[A-Za-z][A-Za-z'’-]{2,}", w)]
    return (
        3 <= len(ln) <= 90
        and ln[0].isupper()
        and not ln.endswith((".", ",", ";", ":"))
        and len(words) <= 12
        and (len(alpha_words) >= 2 or (len(words) == 1 and len(ln) >= 6 and ln.isalpha()))
    )


SMALLCAPS_GAP = re.compile(r"(?<![A-Za-z])([A-Z]) (?=[A-Z]{2})")


def normalize_heading(ln: str) -> str:
    """pdftotext renders small-caps headings as 'I NTRODUCTION'; close the gap on all-caps lines."""
    if ln == ln.upper() and any(c.isalpha() for c in ln):
        return SMALLCAPS_GAP.sub(r"\1", ln)
    return ln


def roman_to_int(r: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10}
    total = 0
    for i, c in enumerate(r):
        v = vals[c]
        total += -v if i + 1 < len(r) and vals[r[i + 1]] > v else v
    return total


def next_nonempty(lines: list[str], i: int, max_skip: int = 3) -> tuple[int, str]:
    for j in range(i + 1, min(i + 1 + max_skip, len(lines))):
        if lines[j].strip():
            return j, normalize_heading(lines[j].strip())
    return -1, ""


def build_map(pages: list[str]) -> dict:
    info: dict = {
        "pages": len(pages),
        "words": sum(len(p.split()) for p in pages),
        "front_matter_lines": [],
        "arxiv_id": None,
        "doi": None,
        "venue_hints": [],
        "code_or_data_urls": [],
        "availability_statements": [],
        "sections": [],
        "figures": [],
        "tables": [],
        "algorithms": [],
        "theorems": [],
        "numbered_equations": 0,
        "references_page": None,
        "appendix_page": None,
    }
    first = [ln.strip() for ln in pages[0].splitlines() if ln.strip()] if pages else []
    info["front_matter_lines"] = first[:12]

    seen = {"figures": set(), "tables": set(), "algorithms": set()}
    last_top = 0  # last accepted top-level numeric section, for sequential filtering

    def add_caption(store: str, n: str, cap: str, lines: list[str], i: int, pno: int) -> None:
        if n in seen[store]:
            return
        seen[store].add(n)
        cap = cap.strip()
        if len(cap) < 40:
            _, nxt = next_nonempty(lines, i, 1)
            if nxt and nxt != cap:
                cap = (cap + " " + nxt).strip()
        info[store].append({"n": int(n), "page": pno, "caption": cap[:160]})

    def add_section(pno: int, number: str, title: str, numeric: bool) -> None:
        nonlocal last_top
        if numeric:
            if info["references_page"] is not None and pno > info["references_page"]:
                return  # numbered headings after the bibliography are almost always noise
            top = int(number.split(".")[0])
            is_sub = "." in number
            if is_sub and top != last_top:
                return
            if not is_sub:
                if top != last_top + 1:
                    return
                last_top = top
        elif info["references_page"] is None or pno <= info["references_page"]:
            return  # letter headings (appendices) only count once we are past the references
        label = f"{number} {title}".strip() if number else title
        info["sections"].append({"page": pno, "title": label})
        if numeric is False and number and info["appendix_page"] is None:
            info["appendix_page"] = pno

    for pno, text in enumerate(pages, start=1):
        if info["arxiv_id"] is None:
            m = ARXIV_PAT.search(text)
            if m:
                info["arxiv_id"] = m.group(1) + (m.group(2) or "")
        if info["doi"] is None and pno <= 2:
            m = DOI_PAT.search(text)
            if m:
                info["doi"] = m.group(1).rstrip(".,;")
        for m in URL_PAT.finditer(text):
            u = m.group(0).rstrip(".,;")
            if u not in info["code_or_data_urls"]:
                info["code_or_data_urls"].append(u)
        lines = text.splitlines()
        for i, raw in enumerate(lines):
            ln = normalize_heading(raw.strip())
            if not ln:
                continue
            if pno <= 2 and VENUE_PAT.search(ln) and len(ln) < 160:
                info["venue_hints"].append({"page": pno, "text": ln})
            if CODE_PAT.search(ln) and len(info["availability_statements"]) < 5:
                info["availability_statements"].append({"page": pno, "text": ln[:200]})

            # --- headings ---
            m = ROMAN_HEADING_PAT.match(ln)
            if m and title_like(m.group(2)) and (info["references_page"] is None or pno <= info["references_page"]):
                add_section(pno, str(roman_to_int(m.group(1))), m.group(2).strip(), numeric=True)
                continue
            m = ROMAN_SUB_PAT.match(ln)
            if m and title_like(m.group(2)) and info["references_page"] is None and last_top:
                info["sections"].append({"page": pno, "title": f"{last_top}.{m.group(1)} {m.group(2).strip()}"})
                continue
            m = NAMED_SECTION_PAT.match(ln)
            if m:
                low = ln.lower()
                if info["references_page"] is None and low.startswith("references"):
                    info["references_page"] = pno
                if low.startswith(("appendix", "appendices", "supplementary")) and info["appendix_page"] is None:
                    info["appendix_page"] = pno
                # Skip if the bare-number lookahead already recorded "N <title>" on this page, or if
                # this bare word already appeared (table headers like "Method" repeat on many pages).
                already = any(
                    s_["title"].lower() == low or (s_["page"] == pno and s_["title"].endswith(" " + ln))
                    for s_ in info["sections"]
                )
                if not already:
                    info["sections"].append({"page": pno, "title": ln})
            else:
                m = NUM_HEADING_PAT.match(ln)
                if m and title_like(m.group(2)):
                    add_section(pno, m.group(1), m.group(2).strip(), numeric=True)
                else:
                    m = BARE_NUM_PAT.match(ln)
                    if m:
                        _, nxt = next_nonempty(lines, i)
                        if nxt and title_like(nxt):
                            add_section(pno, m.group(1), nxt, numeric=True)
                    else:
                        m = LETTER_HEADING_PAT.match(ln)
                        if m and title_like(m.group(2)):
                            add_section(pno, m.group(1), m.group(2).strip(), numeric=False)
                        else:
                            m = BARE_LETTER_PAT.match(ln)
                            if m:
                                _, nxt = next_nonempty(lines, i)
                                if nxt and title_like(nxt):
                                    add_section(pno, m.group(1), nxt, numeric=False)

            # --- captions ---
            m = TAB_ROMAN_PAT.match(ln)
            if m:
                _, cap = next_nonempty(lines, i, 1)
                add_caption("tables", str(roman_to_int(m.group(1))), cap or m.group(2), lines, i, pno)
            for pat, inline, store in (
                (FIG_PAT, FIG_INLINE_PAT, "figures"),
                (TAB_PAT, TAB_INLINE_PAT, "tables"),
                (ALG_PAT, None, "algorithms"),
            ):
                m = pat.match(ln) or (inline.search(ln) if inline else None)
                if m:
                    add_caption(store, m.group(1), m.group(2), lines, i, pno)
            m = THM_PAT.match(ln)
            if m and not any(t_["label"] == m.group(1) for t_ in info["theorems"]):
                info["theorems"].append({"label": m.group(1), "page": pno, "text": m.group(2).strip()[:120]})
            if EQ_PAT.search(ln):
                info["numbered_equations"] += 1

    dedup, seen_s = [], set()
    for sec in info["sections"]:
        key = (sec["page"], sec["title"])
        if key not in seen_s:
            seen_s.add(key)
            dedup.append(sec)
    info["sections"] = dedup
    for k in ("figures", "tables", "algorithms"):
        info[k].sort(key=lambda d: d["n"])
    return info


def print_map(info: dict) -> None:
    print(f"pages: {info['pages']}   words: ~{info['words']}   numbered equations: {info['numbered_equations']}")
    print(f"arXiv: {info['arxiv_id'] or '-'}   DOI: {info['doi'] or '-'}")
    print(f"references start: p{info['references_page'] or '?'}   appendix start: p{info['appendix_page'] or '?'}")
    print("\n[front matter, page 1]")
    for ln in info["front_matter_lines"]:
        print("  " + ln)
    if info["venue_hints"]:
        print("\n[venue hints — verify with web search]")
        for h in info["venue_hints"]:
            print(f"  p{h['page']}: {h['text']}")
    if info["code_or_data_urls"] or info["availability_statements"]:
        print("\n[code / data]")
        for u in info["code_or_data_urls"]:
            print("  " + u)
        for s in info["availability_statements"]:
            print(f"  p{s['page']}: {s['text']}")
    print("\n[sections]")
    for s in info["sections"]:
        print(f"  p{s['page']:>3}  {s['title']}")
    for label in ("figures", "tables", "algorithms"):
        if info[label]:
            print(f"\n[{label}]")
            for d in info[label]:
                print(f"  {label[:-1].title()} {d['n']:>2} (p{d['page']}): {d['caption']}")
    if info["theorems"]:
        print("\n[theorems / lemmas]")
        for d in info["theorems"]:
            print(f"  {d['label']} (p{d['page']}): {d['text']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--find", metavar="REGEX", help="print matching lines with page numbers (case-insensitive)")
    ap.add_argument("--page", type=int, metavar="N", help="print the text of page N (1-based)")
    ap.add_argument("--text-out", type=Path, metavar="FILE", help="write full extracted text to FILE")
    args = ap.parse_args()

    if not args.pdf.exists():
        sys.exit(f"not found: {args.pdf}")
    pages = extract_pages(args.pdf)
    if args.text_out:
        args.text_out.write_text("\f".join(pages), encoding="utf-8")
        print(f"wrote {args.text_out} ({len(pages)} pages)")
    if args.page:
        if not 1 <= args.page <= len(pages):
            sys.exit(f"page out of range (1..{len(pages)})")
        print(pages[args.page - 1])
        return
    if args.find:
        pat = re.compile(args.find, re.I)
        for pno, text in enumerate(pages, start=1):
            for ln in text.splitlines():
                if pat.search(ln):
                    print(f"p{pno}: {ln.strip()[:220]}")
        return
    info = build_map(pages)
    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print_map(info)


if __name__ == "__main__":
    main()
