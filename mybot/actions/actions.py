# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
# from rasa_sdk.events import EventType
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
# import pandas as pd

# import sys
# import io
#
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# from rasa.utils.io import utf8_file
#
# training_data_file = "data/nlu.md"
# training_data = utf8_file(training_data_file)

# from rasa.core.domain import Domain
#
# domain_file = "domain.yml"
# domain = Domain.load(domain_file, utf8=True)



#######################################
################# Xem điểm Anh văn đầu vào

class action_ask_point(Action):

    def name(self) -> Text:
        return "action_ask_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # df = pd.read_csv("db/points_old.csv")
        student_code = next(tracker.get_latest_entity_values("student_code"), None)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="cda_chatbot"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM tblMarks WHERE student_code = '" + student_code + "'")

        myresult = mycursor.fetchall()
        df =  None
        for x in myresult:
            df = x
            print(x)
            break
        # df = df[df["student_code"]==student_code]
        if not (df is None):  # len(df)>0:
            if float(str(df[1])) < 45:
                dispatcher.utter_message(text="Điểm của sinh viên có mã " + student_code + " là: " + str(
                    df[1]) + " điểm. Sinh viên không được miễn anh văn căn bản. Xin cảm ơn!")
            elif float(str(df[1])) < 55:
                dispatcher.utter_message(text="Điểm của sinh viên có mã " + student_code + " là: " + str(
                    df[1]) + " điểm. Sinh viên được miễn học phần anh văn căn bản 1. Xin cảm ơn!")
            elif float(str(df[1])) < 65:
                dispatcher.utter_message(text="Điểm của sinh viên có mã " + student_code + " là: " + str(
                    df[1]) + " điểm. Sinh viên được miễn học phần anh văn căn bản 1 và 2. Xin cảm ơn!")
            elif float(str(df[1])) < 80:
                dispatcher.utter_message(text="Điểm của sinh viên có mã " + student_code + " là: " + str(
                    df[1]) + " điểm. Sinh viên được miễn cả 3 học phần anh văn căn bản. Xin cảm ơn!")
        else:
            dispatcher.utter_message(text="Không tìm thấy mã sinh viên. Vui lòng thử lại!")

        return []



#######################################
################# Cung cấp họ tên để góp ý
class action_give_comment_name(Action):

    def name(self) -> Text:
        return "action_give_comment_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Vui lòng cung cấp nội dung góp ý: ")
        return [SlotSet(key="comment_name", value=tracker.latest_message["entities"][0]["value"])]



#######################################
################# Góp ý
class action_give_comment_content(Action):

    def name(self) -> Text:
        return "action_give_comment_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Xin cảm ơn bạn đã góp ý!")

        comment_name = tracker.get_slot('comment_name')
        # comment_content = tracker.latest_message["text"]
        comment_content = next(tracker.get_latest_entity_values("comment_content"), None)
        print(comment_name, comment_content)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="cda_chatbot"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO tblComments (comment_date, comment_name, comment_content) VALUES (NOW(),%s, %s)"
        val = (comment_name, comment_content)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "Thanh Cong.")

        return []



#######################################
################# Xem lại góp ý
class action_ask_comment_replay(Action):

    def name(self) -> Text:
        return "action_ask_comment_replay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # df = pd.read_csv("db/points_old.csv")
        student_name = next(tracker.get_latest_entity_values("student_name"), None)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="cda_chatbot"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM tblComments WHERE comment_name = '" + student_name + "'")

        myresult = mycursor.fetchall()
        df =  None
        for x in myresult:
            df = x
            print(x)
            break
        # df = df[df["student_code"]==student_code]
        if not (df is None):#len(df)>0:
            dispatcher.utter_message(text="Góp ý của bạn đối với dịch vụ là " + str(df[2]) + ". Xin cảm ơn!")
        else:
            dispatcher.utter_message(text="Không tìm thấy tên của bạn trong dữ liệu góp ý. Vui lòng kiểm tra lại họ tên vừa nhập.")

        return []



#######################################
################# Hỏi ngành chuyên sâu
class action_ask_majors(Action):

    def name(self) -> Text:
        return "action_ask_majors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # df = pd.read_csv("db/majors.csv")
        majors_name = next(tracker.get_latest_entity_values("majors_code"), None)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="cda_chatbot"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM tblmajors WHERE Name_majors = '" + majors_name + "'")

        myresult = mycursor.fetchall()
        df = None
        for x in myresult:
            df = x
            print(x)
            break
        if not (df is None):#len(df)>0:
            dispatcher.utter_message(text="Ngành " + majors_name + " có nha bạn với các tổ hợp xét tuyển như: " + str(df[3]))
        else:
            dispatcher.utter_message(text="Không tìm thấy ngành. Bạn vui lòng kiểm tra lại (lưu ý: tên ngành phải đầy đủ)!")

        return [SlotSet("name", majors_name)]

class action_ask_majors_point(Action):

    def name(self) -> Text:
        return "action_ask_majors_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        majors_name = tracker.get_slot("name")
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="cda_chatbot"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM tblmajors WHERE Name_majors = '" + majors_name + "'")

        myresult = mycursor.fetchall()
        df = None
        for x in myresult:
            df = x
            print(x)
            break

        # df = df[df["majors_code"]==majors_code]
        # dp = df["point"]
        if not (df is None):#len(df)>0 and len(dp)>0:
            dispatcher.utter_message(text="Ngành " + majors_name + " năm trước điểm học bạ là " + str(df[4])
                                          + " điểm và điểm xét tuyển là "+ str(df[5]) +" điểm. Xin cảm ơn!")
        else:
            dispatcher.utter_message(text="Ngành này vừa mở năm nay. Nên không có điểm năm trước. Xin cảm ơn!")

        return []