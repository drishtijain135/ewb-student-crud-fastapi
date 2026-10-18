
from app.database import get_connection


def create_student(student_data: dict):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO students (
                name, date_of_birth, email, phone,
                course, address, enrollment_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_data["name"],
                student_data["date_of_birth"],
                student_data.get("email"),
                student_data.get("phone"),
                student_data.get("course"),
                student_data.get("address"),
                student_data.get("enrollment_date"),
            ),
        )

        connection.commit()

        student = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return dict(student)

    finally:
        connection.close()


def get_all_students():
    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_student_by_id(student_id: int):
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()

def update_student(student_id: int, student_data: dict):
    connection = get_connection()

    try:
        existing_student = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if existing_student is None:
            return None

        connection.execute(
            """
            UPDATE students
            SET name = ?,
                date_of_birth = ?,
                email = ?,
                phone = ?,
                course = ?,
                address = ?,
                enrollment_date = ?
            WHERE id = ?
            """,
            (
                student_data["name"],
                student_data["date_of_birth"],
                student_data.get("email"),
                student_data.get("phone"),
                student_data.get("course"),
                student_data.get("address"),
                student_data.get("enrollment_date"),
                student_id,
            ),
        )

        connection.commit()

        updated_student = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        return dict(updated_student)

    finally:
        connection.close()
