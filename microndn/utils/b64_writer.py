from base64 import b64encode
from math import ceil

# universal b64 writer    
def write_base64_file(file_name, content):
    max_width = 70
    with open(file_name, 'w') as b64_file:
        b64_file_str = b64encode(bytes(content)).decode("utf-8")
        for i in range(0, ceil(len(b64_file_str) / max_width)):
            line = b64_file_str[i * max_width : (i + 1) * max_width] + '\n'
            b64_file.write(line)
