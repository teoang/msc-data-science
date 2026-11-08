"""Copy every definition, proposition, theorem, corollary and algorithm
box of the Notes into build/cheatsheet-boxes.tex, under the chapter and
section they belong to. The Cheatsheet inputs that file, so it always
follows the Notes and keeps their box numbers.

Run from source/: python3 make_cheatsheet.py
"""
import re
from pathlib import Path

NOTES = Path("Fundamentals_of_Statistical_Learning_Notes.tex")
OUT = Path("build/cheatsheet-boxes.tex")

BOX = r"framed(?:defn|prop|thm|cor|algo)"
TOKEN = re.compile(
    r"\\chapter\{(?P<chapter>[^}]*)\}"
    r"|\\section\{(?P<section>[^}]*)\}"
    rf"|(?P<box>\\begin\{{(?P<env>{BOX})\}}.*?\\end\{{(?P=env)\}})",
    re.S,
)


def clean(box):
    # Links to sections or boxes left out of the cheatsheet would dangle,
    # so keep only their text.
    return re.sub(r"\\hyperref\[[^\]]*\]\{([^}]*)\}", r"\1", box)


def main():
    text = NOTES.read_text()
    body = text.split(r"\begin{document}", 1)[1]
    out, section, section_done = [], None, False
    for m in TOKEN.finditer(body):
        if m.group("chapter") is not None:
            out.append(f"\n\\notesheading{{{m.group('chapter')}}}\n")
            section, section_done = None, False
        elif m.group("section") is not None:
            section, section_done = m.group("section"), False
        else:
            if section and not section_done:
                out.append(f"\n\\notessection{{{section}}}\n")
                section_done = True
            out.append("\n" + clean(m.group("box")) + "\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("".join(out))


if __name__ == "__main__":
    main()
