#Product requirements document

---

##School Management System

###Author
Danylo Zakharchenko

###Purpose
The application is supposed to help teacher manage students’ information. As well the system is not a E-Diary or any other e-marking system.

###Use cases
Teachers use the system when working online and ought to manage students’ information remotely and independently

###Requirements
Backend: Python Django

Frontend: Django Templates, Bootstrap

Roles: Teacher/Administration

Entries: Classes/Students/Schools/Notes

###Functionality
Admin(not Django one) can register school 

To register teacher is need to provide unique school id(UUID maybe)

Teacher or Admin should be able to create class and populate it with students manually or by uploading excel file with determined structure.

Teacher can write note about a student

Maybe teacher can download a pdf file with user info

##Model Description

###School
 
- id
- name

###Class

 - id
 - name - max 4 chars (e.g. 11-A )
 - school

###Student
 - id
 - name
 - surname
 - class
 - photo (Optional)
 - email (Optional)
 - phone (Optional)

###Note
 - id
 - student
 - title
 - message

###Teacher/Administration
Is subclasses of the AbstractUser
