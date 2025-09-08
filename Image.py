from Utils import *

converter = ASCIIConverter(font_path="Fonts/CONSOLA.TTF", font_size=50)

frame = cv2.imread('Images\Donut.tif')
ascii_frame = converter.process_and_convert_frame(frame, False, 2)
cv2.imshow('Image', ascii_frame)

cv2.waitKey(0)
cv2.destroyAllWindows()