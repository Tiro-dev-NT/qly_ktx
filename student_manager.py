import data_manager as dm
from models import Student


def get_student_by_id(student_id: str) -> Student | None:
    dm._ensure_data_loaded()
    for student in dm.ALL_STUDENTS:
        if student.student_id == student_id:
            return student
    return None


def get_all_students() -> list[Student]:
    dm._ensure_data_loaded()
    return dm.ALL_STUDENTS


def get_students_by_class(class_name: str) -> list[Student]:
    dm._ensure_data_loaded()
    return [student for student in dm.ALL_STUDENTS if student.class_name == class_name]


def add_student(student_id, full_name, class_name, phone, email, policy_type) -> bool:
    if get_student_by_id(student_id) is not None:
        return False

    student_new = Student(
        student_id      = student_id,
        full_name       = full_name,
        class_name      = class_name,
        phone           = phone,
        email           = email,
        policy_type     = policy_type,
        enrollment_date = dm.get_today_str()  # lấy ngày hôm nay
    )
    dm.ALL_STUDENTS.append(student_new)
    dm.save_students(dm.ALL_STUDENTS)
    return True


def update_student(student_id: str, **kwargs) -> bool:
    student = get_student_by_id(student_id)
    if student is None:
        return False

    for key, value in kwargs.items():
        if hasattr(student, key):
            setattr(student, key, value)

    dm.save_students(dm.ALL_STUDENTS)
    return True


def delete_student(student_id: str) -> bool:
    student = get_student_by_id(student_id)
    if student is None:
        return False

    dm.ALL_STUDENTS.remove(student)
    dm.save_students(dm.ALL_STUDENTS)
    return True


def has_active_contract(student_id: str) -> bool:
    dm._ensure_data_loaded()
    for contract in dm.ALL_CONTRACTS:
        if contract.student_id == student_id and contract.is_active():
            return True
    return False