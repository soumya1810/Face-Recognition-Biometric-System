from flask import Flask, request
from flask_mysqldb import MySQL
import cv2, sys, numpy, os 
from glob import glob
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root@123'
app.config['MYSQL_DB'] = 'images_dataset'

mysql = MySQL(app)


@app.route("/", methods=['POST'])
def index():
    data = request.get_json()
    print(request.is_json)
    sub_data = data['studentId']
    numberOfImages = data["NumberOfImagesCapture"]
    datasets = 'datasets'     
    path = os.path.join(datasets, sub_data)
    if not os.path.exists(path): 
        os.makedirs(path) 
    save_id = len(glob(os.path.join(path, "*.*"))) 
    (width, height) = (130, 100) 
    haar_file = '/home/kanika/recognition/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(haar_file) 
    webcam = cv2.VideoCapture(0) 
    count = 1
    while count <= numberOfImages:  
        (_, im) = webcam.read() 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        cur = mysql.connection.cursor() 
        for (x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
            face = gray[y:y + h, x:x + w] 
            face_resize = cv2.resize(face, (width, height)) 
            cv2.imwrite('% s/% s.png' % (path, count), face_resize)
            filename = os.path.join(path, "%s_%d.png" % (sub_data, save_id)) 
            cur.execute("INSERT INTO path_database(id,path) VALUES (%s,%s)", (sub_data + str(count) , filename))
            mysql.connection.commit()        
        count += 1
        cur.close()
        cv2.imshow('OpenCV', im) 
        key = cv2.waitKey(10) 
        if key == 27: 
            break     
    cv2.destroyAllWindows()       
    return "Images Saved"



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4794)
