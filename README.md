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
