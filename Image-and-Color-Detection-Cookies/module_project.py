from serial import Serial as uart
import cv2
from urllib import request as req
from numpy import argmax
from numpy import random


def pega_centro(x, y, w, h):
    """
    read center of rectangel
    @return cx and cy coordinates
    """
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


def send_serial_data(URL):
    """
    send data suhu and kelembaban from serial to thingspeak API server
    @URL url of Thingspeak API server
    """
    ser = uart("/dev/ttyACM0", 9600, timeout=1)
    ser.flush()
    if ser.in_waiting > 0:
        data = ser.readline().decode("utf-8").rstrip()
        suhu = data.split(",")[0]
        kelembaban = data.split(",")[1]
        print("suhu =", suhu)
        print("kelembaban =", kelembaban)

        # Send data to thingspeak:
        conn = req.urlopen(URL + "&field1=%s&field2=%s" % (suhu, kelembaban))
        conn.close()  # Disconnect connection


def process_contours(
    frame: cv2.typing.MatLike, contours, mask, result_image, level_text
):
    """
    Process detection of model color
    @frame frame of livesteam
    @contours array of leveling standart
    @result_image array of image detection
    @level_text name of file or identification
    """
    # Standart models of the image
    largura_min = 80
    altura_min = 80
    offset = 6
    pos_linha = 300
    color_bbox2 = (0, 255, 0)

    for i, c in enumerate(contours):
        rect = cv2.boundingRect(c)
        line_x, line_y, line_w, line_h = rect
        area = line_w * line_h
        validar_contorno = (line_w >= largura_min) and (line_h >= altura_min)
        if not validar_contorno:
            continue
        if area > 0:
            kotak = cv2.rectangle(
                frame,
                (line_x, line_y),
                (line_x + line_w, line_y + line_h),
                color_bbox2,
                1,
            )
            centro = pega_centro(line_x, line_y, line_w, line_h)
            result_image.append(centro)
            cv2.circle(frame, centro, 4, color_bbox2, -1)
            cv2.putText(
                frame,
                level_text,
                (line_x, line_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),  # green
                2,
            )
            cv2.imwrite(f"images/{level_text}.jpg", frame)
            # return kotak, line_x, line_y, line_w, line_h


def detect_image_cookies(frame: cv2.typing.MatLike, net):
    height, width, _ = frame.shape

    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False
    )
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []
    x = 0
    y = 0
    w = 0
    h = 0

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    return (
        cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4),
        confidences,
        class_ids,
        x,
        y,
        w,
        h,
    )


def validate_image(
    frame,
    index,
    classes,
    class_ids,
    confidences,
    line_x,
    line_y,
    line_w,
    line_h,
    filenames="images/cookies.jpg",
    font=cv2.FONT_HERSHEY_PLAIN,
    colors=random.uniform(0, 255, size=(100, 3)),
):
    if len(index) > 0:
        for i in index.flatten():
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(
                frame,
                (line_x, line_y),
                (line_x + line_w, line_y + line_h),
                color,
                2,
            )
            cv2.putText(
                frame,
                label + " " + confidence,
                (line_x, line_y + 20),
                font,
                2,
                (255, 255, 255),
                2,
            )
            cv2.imwrite(filenames, frame)
