from PIL import Image


def pixeldiff(last_ss, this_ss):
    last_ss = Image.open(f"screenshots/{last_ss}")
    this_ss = Image.open(f"screenshots/{this_ss}")

    width, height = this_ss.size

    last_ss_pixels = list(last_ss.getdata())
    this_ss_pixels = list(this_ss.getdata())

    pixels_changed = 0
    for i in range(20, height, 40):
        for j in range(20, width, 40):
            if last_ss_pixels[width * i + j] != this_ss_pixels[width * i + j]:
                pixels_changed += 1

    return pixels_changed


if __name__ == "__main__":
    import os

    last_ss, this_ss = sorted(os.listdir("screenshots"))[-2:]
    print(pixeldiff(last_ss, this_ss))
