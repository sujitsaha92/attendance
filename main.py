from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate(r"C:\project\yugabyte\attendanceapp-df540-firebase-adminsdk-ku4oi-20a0e8ae76.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://attendanceapp-df540-default-rtdb.firebaseio.com/'
})

# Get a reference to the database service
db = db.reference()

# Load the Kivy file
Builder.load_string('''
<AttendanceLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    
    Label:
        text: 'Name:'
    TextInput:
        id: name_input
        multiline: False
        
    Label:
        text: 'Roll Number:'
    TextInput:
        id: roll_number_input
        multiline: False
        
    Button:
        text: 'Present'
        on_press: root.mark_attendance('present')
    Button:
        text: 'Absent'
        on_press: root.mark_attendance('absent')
''')

# Define the main layout
class AttendanceLayout(BoxLayout):
    def mark_attendance(self, status):
        # Get the current date and time
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")
        
        # Get the name and roll number from the text inputs
        name = self.ids.name_input.text
        roll_number = self.ids.roll_number_input.text
        
        # Create a new attendance record in Firebase
        attendance_ref = db.child('attendance').push()
        attendance_ref.set({
            'name': name,
            'roll_number': roll_number,
            'status': status,
            'date_time': date_time
        })
        
        # Clear the text inputs
        self.ids.name_input.text = ''
        self.ids.roll_number_input.text = ''

# Define the main app
class AttendanceApp(App):
    def build(self):
        return AttendanceLayout()

if __name__ == '__main__':
    AttendanceApp().run()
