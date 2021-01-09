import numpy as np
from PIL import Image
from bitstring import BitArray
import os
import sys


def check_arguments():
    if len(sys.argv) != 2:
        print('Give one argument - name of the file to be encrypted')
        exit()
    infile = str(sys.argv[1])
    file, e = os.path.splitext(infile)
    return file, e, infile


def rgb_pixels(pixel: (int, int, int)) -> (BitArray, BitArray, BitArray):
    r, g, b = pixel
    return BitArray(f'uintle:8={r}'), BitArray(f'uintle:8={g}'), BitArray(f'uintle:8={b}')


def gen_pixels(infile):
    image = Image.open(infile)
    pixels = np.array(image)
    return image, pixels


def encryption(message: str, path: str, file_name: str) -> Image:
    fbyte = 8
    encoding = 'utf8'
    img, pixels = gen_pixels(path)
    width, height = img.size
    encoded = np.ndarray(pixels.shape, dtype=np.uint8)

    msg_bits = [bin(char)[2:].zfill(fbyte) for char in message.encode(encoding)] + ['0' * fbyte]
    bits_gen = (c for c in ''.join(msg_bits))

    print('Encrypting...')
    empty = False
    before = []
    after = []
    for x in range(height):
        for y in range(width):
            if empty:
                encoded[x, y] = pixels[x, y]

            else:
                rgb_bitarray = rgb_pixels(pixels[x, y])
                before.append([p for p in pixels[x, y]])

                for color in rgb_bitarray:
                    if not empty and (bit := next(bits_gen, None)):
                        color.set(bit == '1', 4)

                    else:
                        empty = True
                        break

                r, g, b = rgb_bitarray
                encoded[x, y] = (r.uintle, g.uintle, b.uintle)
                after.append((r.uintle, g.uintle, b.uintle))

    print('Before: ', before)
    print(' ')
    print('After: ', after)
    sh1 = Image.fromarray(encoded)
    print('Mode: ' + sh1.mode)
    print('Generated image size: {}'.format(sh1.size))
    print(' ')
    sh1.show()
    sh1.save('encrypt-' + file_name + '.bmp')


def decryption(path: str) -> str:
    fbyte = 8
    encoding = 'utf8'
    img, pixels = gen_pixels(path)
    width, height = img.size

    print('Decrypting...')
    print('Mode: ' + img.mode)
    print('Generated image size: {}'.format(img.size))
    secrets = []
    counter = 0
    temp = ''
    for x in range(height):
        for y in range(width):
            rgb_bitarray = rgb_pixels(pixels[x, y])

            for color in rgb_bitarray:
                temp += '1' if color[4] else '0'
                counter += 1

                if counter == fbyte:
                    byte = int(temp, 2)

                    if byte == 0:
                        # print(secrets)
                        return bytes(b for b in secrets).decode(encoding)

                    secrets += [byte]
                    temp = ''
                    counter = 0
    raise IndexError('Index out of range!')


if __name__ == '__main__':
    file, e, infile = check_arguments()
    encryption('To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-= To jest zakodowana wiadomość !@#$%^&*()_+1234567890-=', infile, file)

    new_path = './encrypt-' + file + '.bmp'
    print(decryption(new_path))
