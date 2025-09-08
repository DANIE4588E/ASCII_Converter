from Utils import ASCIIConverter
import cv2

converter = ASCIIConverter(font_path="Fonts/CONSOLA.TTF", font_size=50)

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break

            ascii_frame = converter.process_and_convert_frame(frame, True, 10)

            cv2.imshow('Video', ascii_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

