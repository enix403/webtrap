def get_indent(line: str):
    return len(line[:-len(line.lstrip())])

def pullback(content: str):
    lines = content.splitlines()

    min_indent = -1

    for line in lines:
        if len(line.strip()) > 0:
            min_indent = get_indent(line)
            break

    # print(min_indent)
    if min_indent == -1:
        return content

    for i in range(len(lines)):
        remove_indent = min(
            get_indent(lines[i]),
            min_indent
        )

        lines[i] = lines[i][remove_indent:]

    return '\n'.join(lines).strip('\n') + '\n'

val = (f"""
    hello
        export default {'dawdwa'};
d
        """)

print(pullback(val))