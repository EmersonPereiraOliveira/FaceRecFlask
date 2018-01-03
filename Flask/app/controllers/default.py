from app import app
from flask import Flask, render_template, Response
#Discocery where is the root path of modules
from app.controllers.camera import VideoCamera
from app.controllers.capture import Capture
from app.controllers.generator import Generator

from app.models.forms import LoginForm


# The 'render_template, search in path templates automatically by default
# Can be more on route
@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

# Receive variable <name>
@app.route('/test', defaults={"name": None})
@app.route('/test/<name>')
def show_name(name):
    return render_template('test.html', name=name)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


def gen(camera):
    while True:
        frame = camera.get_encoded_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Video streaming generator function
def gen2():
    cap = Capture()
    while True:
        frame = cap.capture()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/face_capture')
def face_capture():
    return Response(gen2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/show_capture")
def show_capture():
    return render_template('capture.html')


@app.route('/video_feed')
def video_feed():
    #Retorna o que o gerador (função gen()) está gerando
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

#Video streaming generator function





if __name__ == '__main__':
    app.run(debug=True)

