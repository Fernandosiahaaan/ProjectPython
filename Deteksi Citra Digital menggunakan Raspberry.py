import cv2
import numpy as np


def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


detect = []
detect1 = []
detect2 = []

cap = cv2.VideoCapture(0)
largura_min = 80
altura_min = 80
offset = 6
pos_linha = 300
delay = 10

detect = []
carros = 0
level_1 = 0
level_2 = 0

# Kunci API
myAPI = '7WGQ07PKRINCC1E6'
# URL API cloud milik Thingspeak.com

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
# baseURL1 = 'https://thingspeak.com/channels/1357366/status/recent'
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
waktu = time.asctime(time.localtime(time.time()))
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        suhu = data.split(",")[0]
        kelembaban = data.split(",")[1]
        print("suhu =", suhu)
        print("kelembaban =", kelembaban)
        #         x = ser.readline().decode('utf-8').rstrip()
        #         print(x, "(celcius) adalah temperatur saat ini.")

        # kirim data thi \ngspeak:
        conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s' % (suhu, kelembaban))
        # putuskan koneksi
        conn.close()

        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red color
        low_red = np.array([15, 0, 0])
        high_red = np.array([20, 255, 255])

        low_red1 = np.array([21, 0, 0])
        high_red1 = np.array([23, 255, 255])

        low_red2 = np.array([26, 40, 40])
        high_red2 = np.array([29, 255, 255])
        mask = cv2.inRange(hsv, low_red, high_red)
        mask1 = cv2.inRange(hsv, low_red1, high_red1)
        mask2 = cv2.inRange(hsv, low_red2, high_red2)

        (contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color_bbox2 = (0, 255, 0)
        status1 = "belum matang"
        status2 = "matang"
        #         data = urllib2.urlencode({'api_key':myAPI, 'status' : status1})
        #         data1 = urllib2.urlencode({'api_key':myAPI, 'status' : status2})

        for (i, c) in enumerate(contours):
            rect = cv2.boundingRect(c)
            linex, liney, linew, lineh = rect
            area = linew * lineh
            validar_contorno = (linew >= largura_min) and (lineh >= altura_min)
            if not validar_contorno:
                continue
            if area > 0:
                kotak = cv2.rectangle(frame, (linex, liney), (linex + linew, liney + lineh), color_bbox2, 1)
                centro = pega_centro(linex, liney, linew, lineh)
                detect.append(centro)
                cv2.circle(frame, centro, 4, color_bbox2, -1)
                cv2.putText(frame, 'kematangan level 1 ', (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.putText(frame, "level 1", (linex, liney), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 0), 2)
                cv2.imwrite("level1.jpg", frame)
        #                 conn = urllib3.request.urlopen(baseURL1 + data = data)

        (contours2, hierarchy) = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color_bbox2 = (0, 255, 0)

        for (i, c) in enumerate(contours2):
            rect = cv2.boundingRect(c)
            linex1, liney1, linew1, lineh1 = rect
            area1 = linew1 * lineh1
            validar_contorno = (linew1 >= largura_min) and (lineh1 >= altura_min)
            if not validar_contorno:
                continue
            if area1 > 0:
                kotak = cv2.rectangle(frame, (linex1, liney1), (linex1 + linew1, liney1 + lineh1), color_bbox2, 1)
                centro = pega_centro(linex1, liney1, linew1, lineh1)
                detect1.append(centro)
                cv2.circle(frame, centro, 4, color_bbox2, -1)
                cv2.putText(frame, 'kematangan level 2', (2, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.putText(frame, "level 2", (linex1, liney1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 0), 2)
                cv2.imwrite("level2.jpg", frame)
        #                 conn = urllib3.request.urlopen(baseURL1 + data = data)

        (contours3, hierarchy) = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color_bbox2 = (0, 255, 0)

        for (i, c) in enumerate(contours3):
            rect = cv2.boundingRect(c)
            linex2, liney2, linew2, lineh2 = rect
            area2 = linew2 * lineh2
            validar_contorno = (linew2 >= largura_min) and (lineh2 >= altura_min)
            if not validar_contorno:
                continue
            if area2 > 0:
                kotak1 = cv2.rectangle(frame, (linex2, liney2), (linex2 + linew2, liney2 + lineh2), color_bbox2, 1)
                centro = pega_centro(linex2, liney2, linew2, lineh2)
                detect.append(centro)
                cv2.circle(frame, centro, 4, color_bbox2, -1)
                cv2.putText(frame, 'Kematangan level 3 ', (2, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.putText(frame, "level 3", (linex2, liney2), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 0), 2)
                cv2.putText(frame, 'Motor servo dimatikan', (2, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)
                cv2.imwrite("level3.jpg", frame)
                ser.write(b'9')
                #                 conn = urllib3.request.urlopen(baseURL1 + data = data1)
                break

        rows, cols, channels = frame.shape
        Mainframe = np.zeros((frame.shape[0], frame.shape[1] + frame.shape[1], 3), np.uint8)
        Mainframe[0:rows, 0:cols] = frame

        cv2.imshow("Frame", frame)
        # cv2.imshow("mask", mask)
        # cv2.imshow("Red", red)

        key = cv2.waitKey(1)
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

