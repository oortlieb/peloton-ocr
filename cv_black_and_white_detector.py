import sys

import cv2
import pytesseract

def inspect(image, name="image"):
    print(image, name)
    cv2.imshow(name, image)
    cv2.waitKey(0)

def parse_word_data_from_string(words_data_string):
    words_data = []

    for word_data_str in words_data_string.split("\n")[1:-1]:
        tokens = word_data_str.strip("\t").split("\t")
        word_data = [int(s) for s in tokens[:11]] + [tokens[-1]]
        words_data.append(word_data)

    return words_data

if __name__ == "__main__":
    # load the input image and grab the image dimensions
    originalImage = cv2.imread(sys.argv[1])
    height, width, _ = originalImage.shape

    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    blackAndWhiteImage = cv2.bitwise_not(blackAndWhiteImage)

    new_width = width * 2
    new_height = height * 2

    blackAndWhiteImage = cv2.resize(blackAndWhiteImage, (new_width, new_height))

    config_options = [
        "--psm 11"
    ]

    words_data = parse_word_data_from_string(pytesseract.image_to_data(blackAndWhiteImage, config=" ".join(config_options), output_type=pytesseract.Output.STRING))

    image = cv2.cvtColor(blackAndWhiteImage, cv2.COLOR_GRAY2RGB)

    for word in words_data:
        (level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text) = word
        if conf == -1: continue
        image = cv2.rectangle(image, (left, top), (left + width, top + height), (255, 0, 0), 1)
        image = cv2.putText(image, text, (left, top - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 0, 0))

    cv2.imwrite("out_{}_{}.png".format(new_width, new_height), image)
