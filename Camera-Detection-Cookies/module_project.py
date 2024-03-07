from serial import Serial as uart
import cv2


def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


def send_serial_data():
    ser = uart("/dev/ttyACM0", 9600, timeout=1)
    ser.flush()
    if ser.in_waiting > 0:
        data = ser.readline().decode("utf-8").rstrip()
        suhu = data.split(",")[0]
        kelembaban = data.split(",")[1]
        print("suhu =", suhu)
        print("kelembaban =", kelembaban)

        # Send data to thingspeak:
        conn = urllib.request.urlopen(
            baseURL + "&field1=%s&field2=%s" % (suhu, kelembaban)
        )
        conn.close()  # Disconnect connection


def process_contours(
    frame: cv2.typing.MatLike, contours, mask, result_image, level_text
):
    # Standart models of the image
    largura_min = 80
    altura_min = 80
    offset = 6
    pos_linha = 300
    color_bbox2 = (0, 255, 0)

    for i, c in enumerate(contours):
        rect = cv2.boundingRect(c)
        linex, liney, linew, lineh = rect
        area = linew * lineh
        validar_contorno = (linew >= largura_min) and (lineh >= altura_min)
        if not validar_contorno:
            continue
        if area > 0:
            kotak = cv2.rectangle(
                frame,
                (linex, liney),
                (linex + linew, liney + lineh),
                color_bbox2,
                1,
            )
            centro = pega_centro(linex, liney, linew, lineh)
            result_image.append(centro)
            cv2.circle(frame, centro, 4, color_bbox2, -1)
            cv2.putText(
                frame,
                level_text,
                (linex, liney),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),  # green
                2,
            )
            cv2.imwrite(f"{level_text}.jpg", frame)
