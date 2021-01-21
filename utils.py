def parse_cmd(cmd):
    cmd_t = cmd.split(' ')
    cmd_c = []
    for item in cmd_t:
        if item != "":
            cmd_c.append(item)
    return cmd_c


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
