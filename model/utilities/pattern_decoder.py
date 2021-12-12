import re


def pattern_decoder(file):
    """ Decoder of pattern files, rle format """
    rle_code = ""
    pattern_width = None
    pattern_height = None
    for line in file:
        # Ignore comments
        if not line.startswith("#"):
            # Find line with dimensions of the pattern
            if line.startswith("x"):
                # find all numbers in line and cast those to int
                numbers = [int(x) for x in re.findall(r'\d+', line)]
                # save online the pattern_width and height, the first two numbers in the line
                pattern_width, pattern_height = numbers[:2]
            else:
                # Other lines are part of the rle code
                rle_code += line

    # Split all items in the rle code
    items = re.findall(r"\d*b|\d*o|\d*\$", rle_code)
    decodex: set[tuple] = set()
    x, y = 0, 0

    # Decode rle string
    for sect in items:
        # Extract the numbers of items
        number = int(re.search("\d+", sect).group(0)) if re.search("\d+", sect) else 1
        # Apply rle rules for decoding
        if "b" in sect:
            x += number
        elif "o" in sect:
            for _ in range(number):
                decodex.add((x, y))
                x += 1
        elif "$" in sect:
            x = 0
            y += number
    return pattern_width, pattern_height, decodex
