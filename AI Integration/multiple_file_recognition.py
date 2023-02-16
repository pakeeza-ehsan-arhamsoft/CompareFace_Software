from compreface_sdk.compreface import CompreFace
from compreface_sdk.compreface.service.recognition_service import RecognitionService
from compreface_sdk.compreface.collections import FaceCollection
from compreface_sdk.compreface.collections.face_collections import Subjects
import psycopg2
import sys, os



class CompareFaceLocal:
    def __init__(self):
        DOMAIN: str = 'http://localhost'
        PORT: str = '8000'
        API_KEY: str = '38a6dd81-45d9-41a5-8301-7dc60bedbf4c'

        options={
            "limit": 3,
            "det_prob_threshold": 0.7,
            "prediction_count": 5,
            "face_plugins": "calculator,age,gender,landmarks",
            "status": "False"
        }

        self.compre_face: CompreFace = CompreFace(DOMAIN, PORT, options=options)
        print(self.compre_face)

        self.recognition: RecognitionService = self.compre_face.init_face_recognition(API_KEY)

        self.face_collection: FaceCollection = self.recognition.get_face_collection()

        self.subjects: Subjects = self.recognition.get_subjects()

        try:
            self.conn = psycopg2.connect(database="compareface",
                                    host="localhost",
                                    user="postgres",
                                    password="123",
                                    port="5432")

            self.cur = self.conn.cursor()
        except Exception as e:
            print(e.args[0])


    def create_table(self):
        try:
            self.cur.execute("""
                    CREATE TABLE User_Data (image_id varchar PRIMARY KEY NOT NULL, image_subject varchar,
                    case_number varchar, ps varchar, examiner_name varchar, examiner_bp_number varchar);
                """)

            self.conn.commit()

        except Exception as e:
            print(e.args[0])



    def top_three_value(self, result):
        scores = [(item["subject"], item["similarity"]) for item in result]
        scores = list(set(scores))
        scores.sort(reverse=True)
        return scores[:3]


    def add_data_db(self, img_id, subject, case_nmber, ps_nmber, examiner_name, examiner_nmber):
        try:
            self.cur.execute("""INSERT INTO user_data (image_id, image_subject, case_number, ps, examiner_name, examiner_bp_number)
                             VALUES (%s, %s, %s, %s, %s, %s)""",
                            (img_id, subject, case_nmber, ps_nmber, examiner_name, examiner_nmber))
            self.conn.commit()

            self.conn.close()
            print("data successfully added to database")
            self.cur.close()

        except Exception as e:
            print(e.args[0])


    def add_img(self, img_path, subject, case_nmber, ps_nmber, examiner_name, examiner_nmber):
        image_path: str = img_path
        subject: str = subject

        obj1 = self.face_collection.add(image_path=image_path, subject=subject)
        image_id, image_subject = obj1["image_id"], obj1["subject"]
        self.add_data_db(image_id, image_subject, case_nmber, ps_nmber, examiner_name, examiner_nmber)


    def recognize_img(self, img_path):
        response = []
        result = self.recognition.recognize(image_path=img_path)
        top_result = self.top_three_value(result["result"][0]["subjects"])
        self.cur.execute("""
            SELECT * from user_data
        """)
        rows = self.cur.fetchall()
        for data in rows:
            res = [(data, res[1]) for res in top_result if res[0] == data[1]]

            response.extend(res)

        return response


if __name__ == '__main__':
    method_call = sys.argv
    if method_call[1] == "2":
        compare = CompareFaceLocal()

        # Create Table
        compare.create_table()
    elif method_call[1] == "3":
        # Add Image to DB
        compare = CompareFaceLocal()

        img = "dataset/sammy/d1.jpeg"
        subject = input("Subject: ")
        case_number = input("Case Number: ")
        ps_number = input("PS Number: ")
        examiner_name = input("Examiner Name: ")
        examiner_number = input("Examiner Number: ")

        compare.add_img(img, subject, case_number, ps_number, examiner_name, examiner_number)

    elif method_call[1] == "1":
        folder_file = os.listdir("FaceAI Media")

        compare = CompareFaceLocal()
        for img in folder_file:
            print(img, " :- \n", compare.recognize_img(f"FaceAI Media/{img}"))
