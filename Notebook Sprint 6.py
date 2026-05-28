import re, json, sys

src_path = sys.argv[1] if len(sys.argv) > 1 else "notebook.ipynb"
dst_path = sys.argv[2] if len(sys.argv) > 2 else "notebook_fixed.ipynb"

text = open(src_path, "r", encoding="utf-8", errors="replace").read()

def find_matching_bracket(s, start_idx, open_char='[', close_char=']'):
    depth = 0
    in_str = False
    esc = False
    for i in range(start_idx, len(s)):
        c = s[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == open_char:
                depth += 1
            elif c == close_char:
                depth -= 1
                if depth == 0:
                    return i
    return None

cells = []
pos = 0
cell_type_re = re.compile(r'"cell_type"\s*:\s*"(code|markdown|raw)"', re.IGNORECASE)

while True:
    m = cell_type_re.search(text, pos)
    if not m:
        break

