# 🏫 Online Learning Platform – Django REST API

This project is a backend for an **Online Learning Platform** built with **Django REST Framework** and **JWT authentication**.  
It supports **user management (students, instructors, admins)**, **courses & lessons**, and **student enrollments with progress tracking**.

---

## 🚀 Setup & Run Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/online-learning-platform.git
cd online-learning-platform
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server
```bash
python manage.py runserver
```

Server runs at 👉 `http://127.0.0.1:8000/`

---

## 🗄️ Database Schema

### **Users (`users_user`)**
| Field       | Type         | Notes                          |
|-------------|-------------|--------------------------------|
| id          | PK           |                                |
| username    | CharField    | unique                         |
| password    | CharField    | hashed                         |
| role        | CharField    | `student` / `instructor` / `admin` |

### **Courses (`courses_course`)**
| Field       | Type         | Notes                |
|-------------|-------------|----------------------|
| id          | PK           |                      |
| title       | CharField    |                      |
| description | TextField    |                      |
| instructor  | FK → User    | role = instructor    |
| price       | Decimal      |                      |
| is_published| Boolean      |                      |

### **Lessons (`courses_lesson`)**
| Field     | Type         | Notes                |
|-----------|-------------|----------------------|
| id        | PK           |                      |
| title     | CharField    |                      |
| content   | TextField    |                      |
| video     | FileField    | optional              |
| course    | FK → Course  |                      |

### **Enrollments (`enrollments_enrollment`)**
| Field       | Type         | Notes                |
|-------------|-------------|----------------------|
| id          | PK           |                      |
| student     | FK → User    | role = student        |
| course      | FK → Course  |                      |
| enrolled_at | DateTime     | auto_now_add          |
| is_active   | Boolean      |                      |
| progress    | Float        | % progress           |

### **Lesson Progress (`enrollments_lessonprogress`)**
| Field     | Type         | Notes                          |
|-----------|-------------|--------------------------------|
| id        | PK           |                                |
| enrollment| FK → Enrollment |                              |
| lesson    | FK → Lesson  |                                |
| watched   | Boolean      |                                |
| watched_at| DateTime     | auto timestamp if watched = True |

---

## 📌 API Documentation

### 🔐 Authentication
- **POST** `/api/auth/token/` → Login (get JWT tokens)
  ```json
  { "username": "xyz", "password": "pass123" }
  ```
- **POST** `/api/auth/token/refresh/`

---

### 👤 Users
- **POST** `/api/users/register/` → Register new user  
- **GET** `/api/users/` → List users (admin only)

---

### 📚 Courses & Lessons
- **GET** `/api/courses/` → List courses  
- **POST** `/api/courses/` → Create course (instructor only)  
- **GET** `/api/courses/{id}/` → Course details  
- **PUT** `/api/courses/{id}/` → Update course  
- **DELETE** `/api/courses/{id}/` → Delete course  

- **GET** `/api/courses/lessons/` → List lessons  
- **POST** `/api/courses/lessons/` → Create lesson (instructor only)  
- **PUT** `/api/courses/lessons/{id}/` → Update lesson  
- **DELETE** `/api/courses/lessons/{id}/` → Delete lesson  

---

### 🎓 Enrollments
- **POST** `/api/enrollments/courses/{course_id}/enroll/` → Enroll student in course  
  ✔️ Example Response:
  ```json
  {
    "id": 1,
    "student": "alice",
    "course": {
      "id": 1,
      "title": "Django for Beginners",
      "description": "Learn Django step by step",
      "instructor": "instructor1"
    },
    "progress": 0.0
  }
  ```

- **GET** `/api/enrollments/my_courses/` → List my enrollments  
- **GET** `/api/enrollments/{id}/my_progress/` → Check progress in one course  
- **POST** `/api/enrollments/{id}/progress/` → Update progress manually  
  Request:
  ```json
  { "progress": 50 }
  ```

---

### 📖 Lesson Progress
- **POST** `/api/enrollments/lesson-progress/` → Mark lesson watched  
  Request:
  ```json
  {
    "enrollment": 1,
    "lesson": 2,
    "watched": true
  }
  ```

  Response:
  ```json
  {
    "id": 1,
    "enrollment": 1,
    "lesson": 2,
    "watched": true,
    "watched_at": "2025-09-05T08:30:00Z"
  }
  ```

---

## ✅ Testing in Postman
1. Login → get token  
2. Set `Authorization: Bearer <access_token>`  
3. Call user, course, enrollment APIs in sequence  
4. Check progress tracking  


## PROJECT-DEMO ##
<img width="1378" height="762" alt="1" src="https://github.com/user-attachments/assets/fde8e31f-bbf7-48e3-a85d-2bd4ff6c889d" />
<img width="1374" height="642" alt="2" src="https://github.com/user-attachments/assets/98fcae73-c594-4c7b-925a-b54ce6c4e58e" />
<img width="1393" height="819" alt="3" src="https://github.com/user-attachments/assets/843bd419-1b8d-43ff-b4f4-b5288cbced1f" />
<img width="1373" height="658" alt="4" src="https://github.com/user-attachments/assets/04a65be8-1216-476c-9150-b4bc59f12329" />
<img width="1379" height="620" alt="5" src="https://github.com/user-attachments/assets/4b4332f6-a5b6-4b36-98d9-a11706bc025d" />
<img width="1387" height="522" alt="6" src="https://github.com/user-attachments/assets/ebf529fe-1a93-44d7-89ff-c8b9d40d560a" />
<img width="1381" height="673" alt="7" src="https://github.com/user-attachments/assets/2eaabecf-fffe-406f-8cb4-ff8480f26094" />
<img width="1372" height="652" alt="8" src="https://github.com/user-attachments/assets/0a3d38b2-111a-4e37-826b-89db26a565ca" />
<img width="1391" height="483" alt="9" src="https://github.com/user-attachments/assets/0278f673-3d56-4868-b636-0e9b78a67fb8" />
<img width="1386" height="889" alt="10" src="https://github.com/user-attachments/assets/61db0260-43fe-42fb-ada8-a1ffc88080b9" />
<img width="1385" height="563" alt="11" src="https://github.com/user-attachments/assets/09381421-cc5e-4180-9356-4e3fb23fc95b" />
<img width="1388" height="898" alt="12" src="https://github.com/user-attachments/assets/be9419e2-79ca-4084-8983-b343a7ee70f8" />
<img width="1394" height="888" alt="13" src="https://github.com/user-attachments/assets/824c511b-c31f-45ad-9e57-3a0ccad0b49b" />
<img width="1438" height="902" alt="14" src="https://github.com/user-attachments/assets/1f4df72b-1e98-4e4e-bbf7-763363e8bdd5" />

