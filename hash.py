import imagehash
from PIL import Image

def av_hash(filename,reference):
    ref = imagehash.average_hash(Image.open(reference))
    hash=imagehash.average_hash(Image.open(filename))
    diff_av=ref-hash
    return diff_av
    
def p_hash(filename,reference):
    ref = imagehash.phash(Image.open(reference))
    hash=imagehash.phash(Image.open(filename))
    diff_p=ref-hash
    return diff_p

def d_hash(filename,reference):
    ref = imagehash.dhash(Image.open(reference))
    hash=imagehash.dhash(Image.open(filename))
    diff_d=ref-hash
    return diff_d    

def w_hash(filename,reference):
    ref = imagehash.whash(Image.open(reference))
    hash=imagehash.whash(Image.open(filename))
    diff_w=ref-hash
    return diff_w  