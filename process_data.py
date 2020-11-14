from PIL import Image
from tqdm.auto import tqdm
import pathlib
import os
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from time import sleep

DATA_ROOT = "/data1/Raw/Reddit/full/EarthPorn"
OUTPUT_ROOT = "/data2/goghgetpaper/imgs/"
BATCH_SIZE = 1000

path = pathlib.Path(DATA_ROOT)
files = list(path.glob('**/*.*'))
print(len(files))


def split_image(file):
    filename = file.stem
    if pathlib.Path(OUTPUT_ROOT, filename + '-0.jpg').exists():
        return

    im = None
    with Image.open(file).convert('RGB') as img:
        im = img.copy()

    width, height = im.size

    cols = width//64
    rows = height//64

    c = 0
    for j in range(rows):
        for i in range(cols):
            out_path = pathlib.Path(
                OUTPUT_ROOT, filename + '-{}.jpg'.format(c))
            if out_path.exists():
                return

            out_path.parent.mkdir(parents=True, exist_ok=True)

            left = i*64
            top = j*64
            right = (i+1)*64
            bottom = (j+1)*64

            temp = im.crop((left, top, right, bottom))

            try:
                temp.save(out_path)
            except Exception as e:
                # print(file, e)
                pass

            c += 1


def break64(file):
    with Image.open(file).convert('RGB') as im:
        width, height = im.size
        images = []

        cols = width//64
        rows = height//64

        for j in range(rows):
            for i in range(cols):
                left = i*64
                top = j*64
                right = (i+1)*64
                bottom = (j+1)*64
                images.append(im.crop((left, top, right, bottom)))
        return images, rows, cols


def getImageSlices(file):
    filename = file.stem
    if pathlib.Path(OUTPUT_ROOT, filename + '-0.jpg').exists():
        return

    imgs, r, c = break64(file)

    for i, im in enumerate(imgs):
        out_path = pathlib.Path(OUTPUT_ROOT, filename + '-{}.jpg'.format(i))
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # q.put([im, out_path])

        try:
            im.save(out_path)
        except Exception as e:
            pass


# def getImage(file):
#     with Image.open(file).convert('RGB') as im:
#         return im.copy()


# for i in tqdm(range(0, len(files), BATCH_SIZE)):
#     processes = []

#     image_batch = []

#     q = mp.Queue()

#     for j in range(i, i+BATCH_SIZE):
#         image_batch.append(getImage(files[j]))

#     for b in range(BATCH_SIZE):
#         p = mp.Process(target=getImageSlices, args=(image_batch[b], q))
#         processes.append(p)
#         p.start()

#     for process in processes:
#         process.join()

#     while not q.empty():
#         im, out_path = q.get()

#         try:
#             im.save(out_path)
#         except Exception as e:
#             pass

with mp.Pool() as p:
    with tqdm(total=len(files)) as pbar:
        for i, _ in enumerate(p.imap_unordered(split_image, files)):
            pbar.update()

# for file in tqdm(files):
#     split_image(file)
