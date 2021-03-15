def parse_cmd(cmd):
    cmd_res = []
    cmd_part = ""
    s1 = False
    s2 = False
    prev = ''
    for c in cmd:
        if c == ' ' or c == '\t' or c == '\n':
            if s1 or s2:
                cmd_part = cmd_part + c
            else:
                if cmd_part != "":
                    cmd_res.append(cmd_part)
                    cmd_part = ""
            continue
        cmd_part = cmd_part + c
        if c == "'":
            if prev != '\\':
                s1 = not s1
        if c == '"':
            if prev != '\\':
                s2 = not s2
        prev = c

    if cmd_part != "":
        cmd_res.append(cmd_part)
    
    return cmd_res


def parse_ipv4(addr):
    addr = addr.lstrip(' ').rstrip(' ')
    addr_list = addr.split(':')
    if len(addr_list) != 2:
        return False
    ip, port = addr_list
    if port.isdigit() is False:
        return False
    port = int(port)
    if port < 0 or port > 65535:
        return False
    ip_stack = ip.split('.')
    if len(ip_stack) != 4:
        return False
    for item in ip_stack:
        if item.isdigit() is False:
            return False
        item = int(item)
        if item < 0 or item > 255:
            return False
    return True
