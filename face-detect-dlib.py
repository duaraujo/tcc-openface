
# import the necessary packages
from imutils import face_utils
import dlib
import cv2
 
# Vamos inicializar um detector de faces (HOG) para então
# fazer a predição dos pontos da nossa face.
#p é o diretorio do nosso modelo já treinado, no caso, ele está no mesmo diretorio
# que esse script
#p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
#predictor = dlib.shape_predictor(p)
win = dlib.image_window()
cap = cv2.VideoCapture(1)
 
while True:
    # Obtendo nossa imagem através da webCam e transformando-a preto e branco.
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Detectando as faces em preto e branco.
    rects = detector(gray, 0)
    
    for i, face_rect in enumerate(rects):
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))   
    #win.add_overlay(rects)
    #win.set_image(detector)
    # Mostre a imagem com os pontos de interesse.
        cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()