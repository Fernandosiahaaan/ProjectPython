import cv2
import numpy as np
import module_project as module

# Array of data images
result_image = []
result_image1 = []
result_image2 = []
class_ids = []
confidences = []

# file models detection image
file_models_training = "models/yolov3_training_last.weights"
file_models_config = "models/yolov3_testing.cfg"
file_models_class = "models/classes.txt"

# Thingspeak API
myAPI = "7WGQ07PKRINCC1E6"  # Kunci API
baseURL = (
    f"https://api.thingspeak.com/update?api_key={myAPI}"  # URL API  Thingspeak.com
)

if __name__ == "__main__":
    # Set Image Detection YoloV3
    net = cv2.dnn.readNet(file_models_training, file_models_config)
    classes = []
    with open(file_models_class, "r") as f:
        classes = f.read().splitlines()

    streaming_camera = cv2.VideoCapture(0)
    while True:
        try:
            module.send_serial_data(baseURL)
        except Exception as failed_read_serial:
            print(
                f"Failed Send Data Sensor to Thingspeak Server; exception = {failed_read_serial}"
            )
        _, frame = streaming_camera.read()

        # detect cookies from model
        index, confidences, class_ids, line_x, line_y, line_w, line_h = (
            module.detect_image_cookies(frame, net)
        )
        # for i in str(rectangle_maturity):
        module.validate_image(
            frame,
            index,
            classes,
            class_ids,
            confidences,
            line_x,
            line_y,
            line_w,
            line_h,
        )

        # Create Frame and Visualization
        rows, cols, channels = frame.shape
        main_frame = np.zeros(
            (frame.shape[0], frame.shape[1] + frame.shape[1], 3), np.uint8
        )
        main_frame[0:rows, 0:cols] = frame

        cv2.imshow("Camera Detection Cookies Level", frame)
        key = cv2.waitKey(1)
        if key == 27:
            streaming_camera.release()
            cv2.destroyAllWindows()
            break
