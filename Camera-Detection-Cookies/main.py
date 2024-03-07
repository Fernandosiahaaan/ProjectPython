import cv2
import numpy as np
import module_project as module

# file name of image
filename_level1 = "level_1_of_Maturity"
filename_level2 = "level_2_of_Maturity"
filename_level3 = "level_3_of_Maturity"

# Array of data images
result_image = []
result_image1 = []
result_image2 = []

# Range Max & Min in Level 1
min_level1 = np.array([15, 0, 0])
max_level1 = np.array([20, 255, 255])

# Range Max & Min in Level 2
min_level2 = np.array([21, 0, 0])
max_level2 = np.array([23, 255, 255])

# Range Max & Min in Level 3
min_level3 = np.array([26, 40, 40])
max_level3 = np.array([29, 255, 255])

# Thingspeak API
myAPI = "7WGQ07PKRINCC1E6"  # Kunci API
baseURL = (
    "https://api.thingspeak.com/update?api_key=%s" % myAPI
)  # URL API  Thingspeak.com
level = 1


while True:
    try:
        module.send_serial_data()
    except Exception as failed_read_serial:
        print(
            f"Failed Send Data Sensor to Thingspeak Server; exception = {failed_read_serial}"
        )

    streaming_camera = cv2.VideoCapture(0)
    _, frame = streaming_camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Level 1
    mask_level1 = cv2.inRange(hsv, min_level1, max_level1)
    (contours_level1, hierarchy) = cv2.findContours(
        mask_level1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    module.process_contours(
        frame, contours_level1, mask_level1, result_image, filename_level1
    )

    # Level 2
    mask_level2 = cv2.inRange(hsv, min_level2, max_level2)
    (contours_level2, hierarchy) = cv2.findContours(
        mask_level2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    module.process_contours(
        frame, contours_level2, mask_level2, result_image1, filename_level2
    )

    # Level 3
    mask_level3 = cv2.inRange(hsv, min_level3, max_level3)
    (contours_level3, hierarchy) = cv2.findContours(
        mask_level3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    module.process_contours(
        frame, contours_level2, mask_level3, result_image2, filename_level3
    )

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
