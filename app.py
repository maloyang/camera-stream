# ref1: https://my.oschina.net/u/4883419/blog/4832014
# ref2: https://ithelp.ithome.com.tw/articles/10230509

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# for ip camera
#camera = cv2.VideoCapture('rtsp://admin:VIRYFYCODE@192.168.8.101:554/h264/ch1/main/av_stream') #螢石
# mp4
#camera = cv2.VideoCapture('test.mp4')
# web-cam: 0=first cam
#camera = cv2.VideoCapture(0)

camera = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # use yield to return this time image
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_start')
def video_start():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


## for my application: just one image : NG
def get_snapshot1():
    video1 = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
    
    success, frame = video1.read()
    img_str = ''
    if not success:
        pass
    else:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
    
        img_str = (b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video1.release()

    return img_str

@app.route('/snapshot1')
def snapshot1():
    return Response(get_snapshot1(), mimetype='image/jpg')

## for my application: just one image : OK
@app.route('/snapshot2')
def snapshot2():
    video1 = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
    
    success, img = video1.read()
    for i in range(40):
        success, img = video1.read()
        if success:
            #print(i)
            cv2.imwrite("image.jpg", img)
    
    ret, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()

    return Response(frame, mimetype='image/jpg')

## for my application: just one image : OK
sn3 = 1
@app.route('/snapshot3')
def snapshot3():
    global sn3
    sn3+=1
    video1 = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
    
    success, img = video1.read()
    for i in range(100*sn3):
        success, img = video1.read()
        if success:
            #print(i)
            cv2.imwrite("image3.jpg", img)
    
    ret, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()

    return Response(frame, mimetype='image/jpg')

## get : OK
@app.route('/snapshot4')
def snapshot4():
    video1 = cv2.VideoCapture('rtsp://admin:VIRYFYCODE@192.168.8.101:554/h264/ch1/main/av_stream') #螢石
    
    success, img = video1.read()
    if success:
        cv2.imwrite("image4.jpg", img)
    
    ret, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()

    return Response(frame, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)