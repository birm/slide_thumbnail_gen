import openslide, subprocess, csv, sys
from multiprocessing.pool import ThreadPool
# GLOBALS (for now)

## todo make args??
config={'thumbnail_size': 100, 'thread_limit': 20, 'image_type': 'png'}
manifest_path=sys.argv[1] or "manifest.csv"


'''process expects a single image metadata as dictionary'''
def process(img):
    try:
        img = gen_thumbnail(img)
    except BaseException as e:
        img['_status'] = "ERRORED"
    return img


def gen_thumbnail(metadata):
        slide = openslide.OpenSlide(metadata['source'])
        filename = metadata['dest']
        size = config['thumbnail_size'] or 100
        imgtype = config['image_type'] or 'png'
        dest =  filename + "." + imgtype
        print(dest)
        slide.get_thumbnail([size,size]).save(dest, imgtype.upper())

#get manifest
with open(manifest_path, 'r') as f:
    reader = csv.DictReader(f)
    manifest = [row for row in reader]
    thread_limit = config.get('thread_limit', 10)
    # run process on each image
    res = ThreadPool(thread_limit).imap_unordered(process, manifest)
    print([r for r in res])
