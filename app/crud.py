
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
