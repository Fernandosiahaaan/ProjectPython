# Image Detection of Cookies Maturity 

## Description

This Repo describe about to embed a script python to `Raspberry` get a analyst of maturity cookies based on color or image. The color detection using HSV standart and the image detection using the YoloV3 detection.

## Presetup 

- install the requirements of module
    ```
    cd Camera-Detection-Cookies
    pip install -r requirements.txt 
    ```

- Download Models of Cookies Image Detection in this [URL](https://drive.google.com/file/d/1Ow20L-KNVrUGfal7pWSUOk6jcIgaTVVV/view?usp=sharing). and copy the models to folder `/Camera-Detection-Cookies/models/`


## Start The Project

- Run program python 
    ```
    cd Camera-Detection-Cookies
    python main.py 
    ```
- Check result of detection in folder `/Camera-Detection-Cookies/images/`

- If you want to set the Job based on Cronjob or Auto Startup in Linux, you can use crontab or Service in folder `/lib/system/systemd/camera-detection.service`. For more Detail you can check in open source documentation.