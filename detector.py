"""検出"""
import urllib
import urllib.request
import cv2
import numpy as np
import config


img1 = cv2.imread(config.PATH["sample"], 0)
sift = cv2.SIFT_create()
matcher = cv2.FlannBasedMatcher()
des1 = sift.detectAndCompute(img1, None)[1]


def detect(img) -> bool:
    count = 0
    try:
        des2 = sift.detectAndCompute(img, None)[1]
        matches = matcher.knnMatch(des1, des2, k=2)
        for m, n in matches:
            if m.distance < n.distance*0.6:
                count += 1
    except cv2.error:
        return False
    return count > 6


def main(img_url: str) -> bool:
    """main"""
    try:
        with urllib.request.urlopen(img_url) as file:
            data = file.read()
            img = np.frombuffer(data, dtype=np.uint8)
            img = cv2.imdecode(img, 0)
            return detect(img)

    except urllib.error.URLError:
        return False


if __name__ == '__main__':
    pass
