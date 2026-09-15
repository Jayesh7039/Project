
# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import os


app = Flask(__name__)
CORS(app)


# ==================================================
# FILE PATHS
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users.json")

DATA_DIR = os.path.join(BASE_DIR, "data")

SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")


# ==================================================
# DEFAULT USERS
# ==================================================

DEFAULT_USERS = {
    "users": [
        {
            "id": 1,
            "name": "Jayesh Mishra",
            "email": "jayesh12@gmail.com",
            "password": "Jayesh@12",
            "role": "student",
            "course": "MCA",
            "active": True
        },
        {
            "id": 2,
            "name": "Swaraj",
            "email": "swaraj12@gmail.com",
            "password": "Swaraj12@gmail.com",
            "role": "student",
            "course": "Computer Science",
            "active": True
        }
    ]
}


# ==================================================
# DEFAULT SUBJECTS
# ==================================================

DEFAULT_SUBJECTS = {
    "subjects": [
        {
            "id": 1,
            "name": "Advanced Java",
            "description": "Classes, JDBC, Servlets and JSP",
            "icon": "☕",
            "progress": 0
        },
        {
            "id": 2,
            "name": "Advanced DBMS",
            "description": "Transactions, indexing and security",
            "icon": "🗄️",
            "progress": 0
        },
        {
            "id": 3,
            "name": "Computer Networks",
            "description": "OSI model, TCP/IP and protocols",
            "icon": "💻",
            "progress": 0
        },
        {
            "id": 4,
            "name": "Artificial Intelligence",
            "description": "Search algorithms and machine learning",
            "icon": "🧠",
            "progress": 0
        }
    ]
}


# ==================================================
# DEFAULT TASKS
# ==================================================

DEFAULT_TASKS = {
    "tasks": [
        {
            "id": 1,
            "user_id": 1,
            "subject_id": 1,
            "title": "Complete Java inheritance",
            "description": "Advanced Java",
            "duration": "30 minutes",
            "due_date": "",
            "priority": "Medium",
            "completed": False
        },
        {
            "id": 2,
            "user_id": 1,
            "subject_id": 2,
            "title": "Revise DBMS transactions",
            "description": "Advanced DBMS",
            "duration": "45 minutes",
            "due_date": "",
            "priority": "High",
            "completed": False
        },
        {
            "id": 3,
            "user_id": 1,
            "subject_id": 3,
            "title": "Watch networking lesson",
            "description": "Computer Networks",
            "duration": "25 minutes",
            "due_date": "",
            "priority": "Low",
            "completed": False
        }
    ]
}


# ==================================================
# DEFAULT PROGRESS
# ==================================================

DEFAULT_PROGRESS = {
    "progress": [
        {
            "user_id": 1,
            "subject_id": 1,
            "percentage": 0
        },
        {
            "user_id": 1,
            "subject_id": 2,
            "percentage": 0
        },
        {
            "user_id": 1,
            "subject_id": 3,
            "percentage": 0
        },
        {
            "user_id": 1,
            "subject_id": 4,
            "percentage": 0
        }
    ]
}


# ==================================================
# JSON FILE FUNCTIONS
# ==================================================

def write_json(file_path, data):
    folder = os.path.dirname(file_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def read_json(file_path, default_data):
    if not os.path.exists(file_path):
        write_json(file_path, default_data)
        return default_data

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            write_json(file_path, default_data)
            return default_data

        return data

    except (json.JSONDecodeError, OSError):
        write_json(file_path, default_data)
        return default_data


def setup_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create users.json if it does not exist.
    # Update the two default accounts if they already exist.
    users_data = read_json(USERS_FILE, DEFAULT_USERS)

    if not isinstance(users_data.get("users"), list):
        users_data["users"] = []

    users = users_data["users"]

    for default_user in DEFAULT_USERS["users"]:
        found = False

        for user in users:
            if user.get("id") == default_user["id"]:
                user.update(default_user)
                found = True
                break

        if not found:
            users.append(default_user.copy())

    users_data["users"] = users
    write_json(USERS_FILE, users_data)

    read_json(SUBJECTS_FILE, DEFAULT_SUBJECTS)
    read_json(TASKS_FILE, DEFAULT_TASKS)
    read_json(PROGRESS_FILE, DEFAULT_PROGRESS)


def public_user_data(user):
    return {
        "id": user.get("id"),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "role": user.get("role", "student"),
        "course": user.get("course", ""),
        "active": user.get("active", True)
    }


def get_user_by_id(user_id):
    users_data = read_json(USERS_FILE, DEFAULT_USERS)

    for user in users_data.get("users", []):
        try:
            if int(user.get("id", 0)) == user_id:
                return user
        except (TypeError, ValueError):
            continue

    return None


# ==================================================
# HOME
# ==================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Study From Home backend is running"
    })


# ==================================================
# LOGIN
# ==================================================

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    users_data = read_json(USERS_FILE, DEFAULT_USERS)
    users = users_data.get("users", [])

    for user in users:
        saved_email = str(
            user.get("email", "")
        ).strip().lower()

        saved_password = str(
            user.get("password", "")
        ).strip()

        if saved_email == email and saved_password == password:
            if user.get("active", True) is False:
                return jsonify({
                    "success": False,
                    "message": "This account is inactive"
                }), 403

            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": public_user_data(user)
            }), 200

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    }), 401


# ==================================================
# REGISTER
# ==================================================

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()
    course = str(data.get("course", "MCA")).strip()

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Name, email and password are required"
        }), 400

    users_data = read_json(USERS_FILE, DEFAULT_USERS)
    users = users_data.get("users", [])

    for user in users:
        saved_email = str(
            user.get("email", "")
        ).strip().lower()

        if saved_email == email:
            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

    new_id = max(
        [
            int(user.get("id", 0))
            for user in users
            if str(user.get("id", "")).isdigit()
        ],
        default=0
    ) + 1

    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "password": password,
        "role": "student",
        "course": course or "MCA",
        "active": True
    }

    users.append(new_user)
    users_data["users"] = users

    write_json(USERS_FILE, users_data)

    return jsonify({
        "success": True,
        "message": "Registration successful",
        "user": public_user_data(new_user)
    }), 201


# ==================================================
# SUBJECTS
# ==================================================

@app.route("/api/subjects", methods=["GET"])
def get_subjects():
    subjects_data = read_json(
        SUBJECTS_FILE,
        DEFAULT_SUBJECTS
    )

    subjects = subjects_data.get("subjects", [])

    return jsonify({
        "success": True,
        "subjects": subjects
    })


@app.route("/api/subjects", methods=["POST"])
def add_subject():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()
    icon = str(data.get("icon", "📚")).strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Subject name is required"
        }), 400

    subjects_data = read_json(
        SUBJECTS_FILE,
        DEFAULT_SUBJECTS
    )

    subjects = subjects_data.get("subjects", [])

    for s in subjects:
        if str(s.get("name", "")).strip().lower() == name.lower():
            return jsonify({
                "success": False,
                "message": "A subject with this name already exists"
            }), 409

    new_id = max(
        [
            int(s.get("id", 0))
            for s in subjects
            if str(s.get("id", "")).isdigit()
        ],
        default=0
    ) + 1

    new_subject = {
        "id": new_id,
        "name": name,
        "description": description or "Study and improve your knowledge.",
        "icon": icon or "📚",
        "progress": 0
    }

    subjects.append(new_subject)
    subjects_data["subjects"] = subjects

    write_json(SUBJECTS_FILE, subjects_data)

    return jsonify({
        "success": True,
        "message": "Subject added successfully",
        "subject": new_subject
    }), 201


@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
def update_subject(subject_id):
    data = request.get_json(silent=True) or {}

    subjects_data = read_json(
        SUBJECTS_FILE,
        DEFAULT_SUBJECTS
    )

    subjects = subjects_data.get("subjects", [])

    for s in subjects:
        if int(s.get("id", 0)) == subject_id:
            if "name" in data:
                s["name"] = str(data["name"]).strip()
            if "description" in data:
                s["description"] = str(data["description"]).strip()
            if "icon" in data:
                s["icon"] = str(data["icon"]).strip()

            write_json(SUBJECTS_FILE, subjects_data)

            return jsonify({
                "success": True,
                "message": "Subject updated successfully",
                "subject": s
            })

    return jsonify({
        "success": False,
        "message": "Subject not found"
    }), 404


# ==================================================
# GET USER TASKS
# ==================================================

@app.route("/api/tasks/<int:user_id>", methods=["GET"])
def get_tasks(user_id):
    tasks_data = read_json(
        TASKS_FILE,
        DEFAULT_TASKS
    )

    tasks = tasks_data.get("tasks", [])

    user_tasks = [
        task for task in tasks
        if int(task.get("user_id", 0)) == user_id
    ]

    return jsonify({
        "success": True,
        "tasks": user_tasks
    })


# ==================================================
# ADD NEW TASK
# ==================================================

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    subject_id = data.get("subject_id")

    title = str(
        data.get("title", "")
    ).strip()

    due_date = str(
        data.get("due_date", "")
    ).strip()

    priority = str(
        data.get("priority", "Medium")
    ).strip()

    if user_id is None or subject_id is None or not title:
        return jsonify({
            "success": False,
            "message": "User, subject and task title are required"
        }), 400

    try:
        user_id = int(user_id)
        subject_id = int(subject_id)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "User ID and subject ID must be numbers"
        }), 400

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    users_data = read_json(
        USERS_FILE,
        DEFAULT_USERS
    )

    users = users_data.get("users", [])

    user_exists = any(
        int(user.get("id", 0)) == user_id
        for user in users
    )

    if not user_exists:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    subjects_data = read_json(
        SUBJECTS_FILE,
        DEFAULT_SUBJECTS
    )

    subjects = subjects_data.get("subjects", [])

    subject_exists = any(
        int(subject.get("id", 0)) == subject_id
        for subject in subjects
    )

    if not subject_exists:
        return jsonify({
            "success": False,
            "message": "Subject not found"
        }), 404

    tasks_data = read_json(
        TASKS_FILE,
        DEFAULT_TASKS
    )

    if not isinstance(tasks_data.get("tasks"), list):
        tasks_data["tasks"] = []

    tasks = tasks_data["tasks"]

    new_id = max(
        [
            int(task.get("id", 0))
            for task in tasks
        ],
        default=0
    ) + 1

    new_task = {
        "id": new_id,
        "user_id": user_id,
        "subject_id": subject_id,
        "title": title,
        "description": "",
        "duration": "",
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }

    tasks.append(new_task)
    tasks_data["tasks"] = tasks

    write_json(TASKS_FILE, tasks_data)
    recalculate_user_progress(user_id)

    return jsonify({
        "success": True,
        "message": "Task added successfully",
        "task": new_task
    }), 201


# ==================================================
# UPDATE TASK STATUS
# ==================================================

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    tasks_data = read_json(
        TASKS_FILE,
        DEFAULT_TASKS
    )

    tasks = tasks_data.get("tasks", [])

    for task in tasks:
        if int(task.get("id", 0)) == task_id:

            if "completed" in data:
                task["completed"] = bool(
                    data["completed"]
                )

            if "title" in data:
                task["title"] = str(
                    data["title"]
                ).strip()

            if "due_date" in data:
                task["due_date"] = str(
                    data["due_date"]
                ).strip()

            if "priority" in data:
                task["priority"] = str(
                    data["priority"]
                ).strip()

            write_json(TASKS_FILE, tasks_data)

            user_id = int(task.get("user_id", 1))
            recalculate_user_progress(user_id)

            return jsonify({
                "success": True,
                "message": "Task updated successfully",
                "task": task
            })

    return jsonify({
        "success": False,
        "message": "Task not found"
    }), 404


# ==================================================
# DYNAMIC PROGRESS RECALCULATION
# ==================================================

def recalculate_user_progress(user_id):
    tasks_data = read_json(TASKS_FILE, DEFAULT_TASKS)
    user_tasks = [
        t for t in tasks_data.get("tasks", [])
        if int(t.get("user_id", 0)) == user_id
    ]

    subjects_data = read_json(SUBJECTS_FILE, DEFAULT_SUBJECTS)
    subjects_list = subjects_data.get("subjects", [])

    progress_data = read_json(PROGRESS_FILE, DEFAULT_PROGRESS)
    if not isinstance(progress_data.get("progress"), list):
        progress_data["progress"] = []

    progress_list = progress_data["progress"]

    subject_tasks = {}
    for task in user_tasks:
        sub_id = int(task.get("subject_id", 0))
        if sub_id == 0:
            desc = str(task.get("description", "")).lower()
            title = str(task.get("title", "")).lower()
            for s in subjects_list:
                s_name = str(s.get("name", "")).lower()
                if s_name and (s_name in desc or s_name in title):
                    sub_id = int(s.get("id", 0))
                    task["subject_id"] = sub_id
                    break

        if sub_id > 0:
            if sub_id not in subject_tasks:
                subject_tasks[sub_id] = {"total": 0, "completed": 0}
            subject_tasks[sub_id]["total"] += 1
            if task.get("completed") is True:
                subject_tasks[sub_id]["completed"] += 1

    for sub_id, counts in subject_tasks.items():
        pct = round((counts["completed"] / counts["total"]) * 100) if counts["total"] > 0 else 0

        found = False
        for item in progress_list:
            if int(item.get("user_id", 0)) == user_id and int(item.get("subject_id", 0)) == sub_id:
                item["percentage"] = pct
                found = True
                break

        if not found:
            progress_list.append({
                "user_id": user_id,
                "subject_id": sub_id,
                "percentage": pct
            })

    progress_data["progress"] = progress_list
    write_json(PROGRESS_FILE, progress_data)
    return progress_list


# ==================================================
# PROGRESS
# ==================================================

@app.route("/api/progress/<int:user_id>", methods=["GET"])
def get_progress(user_id):
    recalculate_user_progress(user_id)

    progress_data = read_json(
        PROGRESS_FILE,
        DEFAULT_PROGRESS
    )

    user_progress = [
        item for item in progress_data.get("progress", [])
        if int(item.get("user_id", 0)) == user_id
    ]

    return jsonify({
        "success": True,
        "progress": user_progress
    })


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/api/dashboard/<int:user_id>", methods=["GET"])
def get_dashboard(user_id):
    recalculate_user_progress(user_id)

    users_data = read_json(
        USERS_FILE,
        DEFAULT_USERS
    )

    subjects_data = read_json(
        SUBJECTS_FILE,
        DEFAULT_SUBJECTS
    )

    tasks_data = read_json(
        TASKS_FILE,
        DEFAULT_TASKS
    )

    progress_data = read_json(
        PROGRESS_FILE,
        DEFAULT_PROGRESS
    )

    user = None

    for item in users_data.get("users", []):
        try:
            if int(item.get("id", 0)) == user_id:
                user = item
                break
        except (TypeError, ValueError):
            continue

    if user is None:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    subjects = subjects_data.get("subjects", [])

    user_progress = [
        item for item in progress_data.get("progress", [])
        if int(item.get("user_id", 0)) == user_id
    ]

    progress_map = {
        int(item.get("subject_id", 0)): item.get(
            "percentage",
            0
        )
        for item in user_progress
    }

    final_subjects = []

    for subject in subjects:
        subject_copy = subject.copy()
        subject_id = int(subject_copy.get("id", 0))

        if subject_id in progress_map:
            subject_copy["progress"] = progress_map[
                subject_id
            ]

        final_subjects.append(subject_copy)

    user_tasks = [
        task for task in tasks_data.get("tasks", [])
        if int(task.get("user_id", 0)) == user_id
    ]

    total_subjects = len(final_subjects)

    completed_tasks = len([
        task for task in user_tasks
        if task.get("completed") is True
    ])

    pending_tasks = len(user_tasks) - completed_tasks

    if total_subjects > 0:
        overall_progress = round(
            sum(
                subject.get("progress", 0)
                for subject in final_subjects
            ) / total_subjects
        )
    else:
        overall_progress = 0

    return jsonify({
        "success": True,
        "data": {
            "user": public_user_data(user),
            "subjects": final_subjects,
            "tasks": user_tasks,
            "statistics": {
                "total_subjects": total_subjects,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "overall_progress": overall_progress
            }
        }
    })


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":
    setup_files()

    print("========================================")
    print("Study From Home backend is running")
    print("Login email: jayesh12@gmail.com")
    print("Login password: Jayesh@12")
    print("Second account: swaraj12@gmail.com")
    print("Dashboard API: /api/dashboard/1")
    print("Add task API: POST /api/tasks")
    print("========================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )