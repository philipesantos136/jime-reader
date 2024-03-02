from ImageReader import ImageReader
from ImageCropper import ImageCropper
from WindowCapture import WindowCapture
import cv2 as cv
import time
import numpy as np
from PIL import ImageGrab


class AlgorithmRunner:

    @staticmethod
    def run():
        debug = False # Activate print image filters
        window_capture = WindowCapture('Journeys in Middle-Earth')

        time_spend = ''
        text_read = False
        my_list = list()
        crop_top = False

        while True:
            screenshot = ImageGrab.grab()
            screenshot = np.array(screenshot)
            screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)

            image_cropper = ImageCropper()
            found_img, max_loc = image_cropper.find_image(screenshot)

            if found_img is False:
                text_read = False

            if found_img and text_read is False:

                # wait until the whole border appears
                time.sleep(0.15)

                screenshot = ImageGrab.grab()
                screenshot = np.array(screenshot)
                screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

                screenshot, crop_img, crop_top = image_cropper.crop_image(screenshot, max_loc)

                ############### Pre-processing image #################
                if debug:
                    cv.imwrite('result.jpg', crop_img)
                # Aplly gray filter for better OCR
                gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)

                # APllay Blur to reduce noise
                imgGaussian = cv.GaussianBlur(gray,(3,3),9)
                if debug:
                    cv.imwrite('imgGaussian.jpg', imgGaussian)

                imgBilateral = cv.bilateralFilter(imgGaussian, 6,90,90)
                if debug:
                    cv.imwrite('imgBilateral.jpg', imgBilateral)


                imgLaplace = cv.Laplacian(imgGaussian,cv.CV_8U)
                if debug:
                    cv.imwrite('imgLaplace.jpg', imgLaplace)

                # Multiplication to better details
                img = 2 * cv.subtract(imgBilateral,imgLaplace)

                result = cv.add(gray,img)

                thresh = cv.threshold(result, 127, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

                # Morph open to remove noise and invert image
                kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
                opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)
                invert = 255 - opening

                if debug:
                    cv.imwrite('Tesseract.jpg', invert)


                image_reader = ImageReader(invert)

                text = image_reader.read_from_img()

                image_reader.read_sentence_by_sentence(my_list)

                text_read = True

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break