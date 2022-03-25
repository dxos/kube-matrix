import re

# convert hex string to pixel
def convert(str):
    # https://docs.python.org/2/library/re.html#match-objects
    match = re.search(r'^([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})$', str);

    if match:
        r = match.group(1)
        g = match.group(2)
        b = match.group(3)
        w = match.group(4)
        return [int('0x'+r, 0), int('0x'+g, 0), int('0x'+b, 0), int('0x'+w, 0)]
    else:
        return [0, 0, 0, 0]

# convert ascii art to array of hex tuples.
def ascii(str, colors = ['55555555']):
    str = str.replace('|', '') # Optionally terminate each line with | to prevent removing trailing spaces
    str = str.replace('\n', '')

    pixels = []
    for c in str:
        if c == ' ':
            pixel = (0, 0, 0, 0)
        else:
            try:
                # If number then attempt to index array of colors.
                i = int(c)
                pixel = convert(colors[i])
            except:
                pixel = convert(colors[0])

        pixels.append(pixel)

    return pixels

# bitmap is string that contains 121 (11x11) comma delimitered strings of the form 'RRGGBBWW'
def hex(bitmap = ''):
    values = []
    if bitmap:
        values = bitmap.split(',')

    pixels = []
    for y in range(0, 11):
        for x in range(0, 11):
            i = y * 11 + x
            if (i <= len(values) - 1):
                # https://docs.python.org/2/library/re.html#match-objects
                match = re.search(r'^([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})$', values[i]);

                if match:
                    r = match.group(1)
                    g = match.group(2)
                    b = match.group(3)
                    w = match.group(4)
                    pixels.append([int('0x'+r, 0), int('0x'+g, 0), int('0x'+b, 0), int('0x'+w, 0)])
                    continue

            pixels.append([int(0), int(0), int(0), int(0)])

    return pixels
