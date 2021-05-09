# import os
# import glob
#
# import cv2
#
#
# class FaceDetect:
#
#     def __init__(self, upload_path):
#         self.err_msg = None
#         self.upload_path = upload_path
#         self.img = self.load_img()
#         self.face_xml = cv2.CascadeClassifier(r'static/ocv_face_detect.xml')
#
#     def load_img(self):
#         try:
#             img = cv2.imread(self.upload_path)
#         except FileNotFoundError:
#             img = None
#             self.err_msg = "图片读取失败，请重新上传！"
#
#         return img
#
#     def show_img(self, img=None):
#         s_img = self.img if img is None else img
#
#         cv2.imshow('show', s_img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#     # def resize(self, size="200*200"):
#     #     try:
#     #         size = size.split("*")
#     #         w = size[0]
#     #         h = size[1]
#     #     except IndexError:
#     #         w = 200
#     #         h = 200
#     #         self.err_msg = "重置大小参数有误，使用默认参数！"
#     #
#     #     resized = cv2.resize(self.img, (int(w), int(h)), interpolation=cv2.INTER_CUBIC)
#     #     cv2.imwrite(self.upload_path, resized)
#     #
#     #     return resized
#
#     def detect(self):
#
#         self.remove_old_face()
#
#         gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
#         face_areas = self.face_xml.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3, flags=0)
#
#         if len(face_areas) == 1:
#             try:
#                 (x, y, w, h) = face_areas[0]
#                 face = self.img[y: y + h, x: x + w]
#                 # face = self.resize(face)
#                 save_path = self.save_img(face)
#
#             except IndexError:
#                 save_path = None
#                 self.err_msg = '截取人脸失败，请重新拍摄'
#
#         else:
#             save_path = ''
#             self.err_msg = '未检测到人脸或图片中存在多张人脸，请重新上传！'
#
#         return save_path
#
#     def save_img(self, img):
#         filepath, filename = os.path.split(self.upload_path)
#         filename_tup = filename.rpartition('.')
#         save_path = f'{filepath}/{filename_tup[0]}_face.{filename_tup[2]}'.replace("\\", "/")
#         cv2.imwrite(save_path, img)
#
#         return save_path
#
#     def remove_old_face(self):
#         filepath, filename = os.path.split(self.upload_path)
#         filename_tup = filename.rpartition('.')
#         old_faces = glob.glob(f'{filepath}/{filename_tup[0]}_face.[jp][pn]g'.replace("\\", "/"))
#         if len(old_faces) >= 1:
#             os.remove(old_faces[0])
#
#
# if __name__ == '__main__':
#     detector = FaceDetect(r'F:\GitSpace\flaskServer\static\upload\wechat\t1.jpg')
#     print(detector.detect())
