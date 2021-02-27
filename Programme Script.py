import time
import os
import picamera
import schedule
from datetime import datetime

def mkdir(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
        
def cam_capture(iso):
    print(iso)
    now = datetime.now() 
    capture_date = now.strftime("%d-%m-%Y")
    capture_time = now.strftime("%H-%M")
    mkdir(capture_date)
    mkdir(capture_date + "/"+ capture_time)
    
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.framerate = 30
        camera.iso = iso
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        #camera.exposure_speed = int(camera.exposure_speed * 1.5)
        speed = int(camera.exposure_speed)
        camera.shutter_speed = speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        delta = int(camera.shutter_speed * 0.1); # shutter speed increment step
        
        for i in range(-9,1):
            # create folder based on exposure lvl
            exposure_folder = capture_date + "/"+ capture_time + "/%02f" % (i*0.1)
            mkdir(exposure_folder)
            
            # retrieve current date and time again
            now = datetime.now() 
            date_time = now.strftime("%d-%m-%Y, %H-%M-%S-%f")
            camera.shutter_speed = speed + delta * i
            print('%02f' % (i*0.1))
            print('exposure time: %d' % camera.shutter_speed)
            print(date_time)
            if(camera.shutter_speed<0):
                break
            filename = (date_time + "-%02f.bmp") % (i*0.1)
            
            print("filename:" + filename)
            camera.capture(exposure_folder + "/" + filename)
            
        # Finally, take several photos with the fixed settings
        # camera.capture_sequence(['image%02d.jpg' % i for i
        
cam_capture(100)
# schedule.every().day.at("12:00").do(cam_capture, 100)
# schedule.every().day.at("13:00").do(cam_capture, 100)
# schedule.every().day.at("14:00").do(cam_capture, 100)
# schedule.every().day.at("18:00").do(cam_capture, 200)
# schedule.every().day.at("18:30").do(cam_capture, 200)
# 
# while True:
#     schedule.run_pending()
#     time.sleep(10)
# 

