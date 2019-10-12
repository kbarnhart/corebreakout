"""
Assorted image / mask / label / region manipulation functions.
"""
import numpy as np

###++++++++++++++++++++++++++++++###
### Region + Layout Manipulation ###
###++++++++++++++++++++++++++++++###

# Could add 'b2t' and 'r2l', although those are very unusual
ORIENTATIONS = ['t2b', 'l2r']


def rotate_vertical(region_img, orientation):
    """Rotated (cropped) `region_img` array to vertical, given the depth `orientation`."""
    assert orientation in ORIENTATIONS, f'orientation {orientation} must be one of {ORIENTATIONS}'

    if orientation is 't2b':
        return region_img
    elif orientation is 'l2r':
        return np.rot90(region_img, k=-1)
    else:
        raise ValueError(f'bad `orientation`: {orientation}')


def sort_regions(regions, order):
    """Sort skimage `regions` (core columns), given the column `order`."""
    assert order in ORIENTATIONS, f'order {order} must be one of {ORIENTATIONS}'

    idx = 0 if order is 't2b' else 1
    regions.sort(key=lambda x: x.bbox[idx])

    return regions


def maximum_extent(regions, crop_axis):
    """Find min/max of combined skimage `regions`, along `crop_axis`."""
    low_idx = 0 if crop_axis == 1 else 1
    high_idx = 2 if crop_axis == 1 else 3

    low = min(r.bbox[low_idx] for r in regions)
    high = max(r.bbox[high_idx] for r in regions)

    return (low, high)


def v_overlapping(r0, r1):
    """Check if skimage regions `r0` & `r1` are *vertically* overlapping."""
    return (r0.bbox[0] < r1.bbox[2] and r0.bbox[2] > r1.bbox[0])


def h_overlapping(r0, r1):
    """Check if skimage regions `r0` & `r1` are *horizontally* overlapping."""
    return (r0.bbox[1] < r1.bbox[3] and r0.bbox[3] > r1.bbox[1])


def crop_region(img, labels, region, axis=0, endpts=(815, 6775)):
    """Adjust region bbox and return cropped region * mask.

    Parameters
    ----------
    img : array
        The image to crop
    labels : array
        Mask of integer labels, same height and width as `img`
    region : skimage.RegionProperties instance
        Region object corresponding to column to crop around
    axis : int, optional
        Which axis to change `endpts` along, default=0 (y-coordinates)
    endpts : tuple(int)
        Least extreme endpoint coordinates allowed along `axis`

    Returns
    -------
    region : array
        Masked image region, cropped in (adjusted) bounding box
    """
    r0, c0, r1, c1 = region.bbox

    if axis is 0:
        c0, c1 = min(c0, endpts[0]), max(c1, endpts[1])
    elif axis is 1:
        r0, r1 = min(r0, endpts[0]), max(r1, endpts[1])

    region_img = img * np.expand_dims(labels==region.label, -1)

    return region_img[r0:r1,c0:c1,:]


###++++++++++++++++++++++++###
### Preds + masks + labels ###
###++++++++++++++++++++++++###

def masks_to_labels(masks):
    """Convert boolean (H,W,N) `masks` array to integer (H,W) in range(0,N+1)."""
    labels = np.zeros(masks.shape[0:-1], dtype=np.int)

    for i in range(masks.shape[-1]):
        labels += (i+1) * masks[:,:,i].astype(int)

    return labels


def squeeze_labels(labels):
    """Set labels to range(0, objects+1)"""
    label_ids = np.unique([r.label for r in measure.regionprops(labels)])

    for new_label, label_id in zip(range(1, label_ids.size), label_ids[1:]):
        labels[labels==label_id] == new_label

    return labels


def vstack_images(imgA, imgB):
    """Vstack `imgA` and `imgB`, after RHS zero-padding the narrower if necessary."""
    dimA, dimB = imgA.ndim, imgB.ndim
    assert dimA == dimB, f'Cannot vstack images of different dimensions: {(dimA, dimB)}'
    assert dimA in [2, 3], f'Images must be 2D or 3D, not {dimA}D'

    dw = imgA.shape[1] - imgB.shape[1]

    if dw == 0:
        return np.concatenate([imgA, imgB])
    elif dimA == 2:
        pads = ((0,0), (0, abs(dw)))
    else:
        pads = ((0,0), (0, abs(dw)), (0,0))

    if dw < 0:
        paddedA = np.pad(imgA, pads, 'constant')
        return np.concatenate([paddedA, imgB])
    else:
        paddedB = np.pad(imgB, pads, 'constant')
        return np.concatenate([imgA, paddedB])
