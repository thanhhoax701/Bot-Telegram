# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector



################### xem diem anh van

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


########################### góp ý
class action_give_comment_name(Action):

    def name(self) -> Text:
        return "action_give_comment_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Vui lòng cung cấp nội dung góp ý: ")
        return [SlotSet(key="comment_name", value=tracker.latest_message["entities"][0]["value"])]





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


############################## xem lại góp ý
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


