class Room:
    def __init__(self, room_id, room_type, price_per_month, 
                 capacity, current_occupants, status, floor, building):
        self.room_id = room_id
        self.room_type = room_type
        self.price_per_month = price_per_month
        self.capacity = capacity
        self.current_occupants = current_occupants
        self.status = status
        self.floor = floor
        self.building = building

    def __str__(self):
        status = "Còn chỗ" if self.is_available() else "Hết chỗ/Bảo trì"
        return f"Phòng [{self.room_id}] Tòa {self.building} - {self.room_type} giường | {status}"


    def __repr__(self):
        return (f"Room(id='{self.room_id}', building='{self.building}', "
                f"occupants={self.current_occupants}/{self.capacity}, status='{self.status}')")
    def to_dict(self) -> dict:
        #Chuyển thành data json
        return  {
                    "room_id": self.room_id,
                    "room_type": self.room_type,
                    "price_per_month": self.price_per_month,
                    "capacity": self.capacity,
                    "current_occupants": self.current_occupants,
                    "status": self.status,
                    "floor": self.floor,
                    "building": self.building
                }

    def is_available(self) -> bool:
        return self.current_occupants < self.capacity and self.status != "maintenance" #Trả về True nếu còn slot, False nếu hết slot hoặc bảo trì

    def get_vacancy(self) -> int:  # logic: capacity - current_occupants -> Vị trí còn trống
        return self.capacity - self.current_occupants

class Student:
    def __init__(self, student_id, full_name, class_name, 
                 phone, email, policy_type, enrollment_date):
        self.student_id = student_id
        self.full_name = full_name
        self.class_name = class_name
        self.phone = phone
        self.email = email
        self.policy_type = policy_type
        self.enrollment_date = enrollment_date

    def __str__(self):
        return f"[{self.student_id}] {self.full_name} - Lớp: {self.class_name}"

    def __repr__(self):
        return (f"Student(id='{self.student_id}', name='{self.full_name}', "
                f"policy='{self.policy_type}')")

    def to_dict(self) -> dict:
        return  {
                    "student_id": self.student_id,
                    "full_name": self.full_name,
                    "class_name": self.class_name,
                    "phone": self.phone,
                    "email": self.email,
                    "policy_type": self.policy_type,
                    "enrollment_date": self.enrollment_date
                }


class Contract:
    def __init__(self, contract_id, student_id, room_id, 
                 start_date, end_date, status, created_date):
        self.contract_id = contract_id
        self.student_id = student_id
        self.room_id = room_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.created_date = created_date

    def __str__(self):
        return f"Hợp đồng [{self.contract_id}] - MSSV {self.student_id} - Phòng [{self.room_id}] | status: '{self.status}'"

    def __repr__(self):
        return (f"Contract(id='{self.contract_id}', student='{self.student_id}', "
                f"room='{self.room_id}', status='{self.status}', end='{self.end_date}')")

    def to_dict(self) -> dict:
        return {
            "contract_id": self.contract_id,
            "student_id": self.student_id,
            "room_id": self.room_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "created_date": self.created_date
        }

    def is_active(self) -> bool:
        return self.status == "active"

    def is_expired(self) -> bool:
        from datetime import date
        today = date.today()
        end = date.fromisoformat(self.end_date)
        return self.status == "active" and today > end

class ServiceBill:
    def __init__(self, bill_id, contract_id, room_id, month, year,
                 electric_start, electric_end, water_start, water_end,
                 electric_amount, water_amount, total_amount,
                 status, due_date, paid_date):
        self.bill_id = bill_id
        self.contract_id = contract_id
        self.room_id = room_id
        self.month = month
        self.year = year
        self.electric_start = electric_start
        self.electric_end = electric_end
        self.water_start = water_start
        self.water_end = water_end
        self.electric_amount = electric_amount
        self.water_amount = water_amount
        self.total_amount = total_amount
        self.status = status
        self.due_date = due_date
        self.paid_date = paid_date

    def __str__(self):
        return f"[{self.bill_id}] Phòng {self.room_id} - {self.month}/{self.year} | {self.total_amount:,}đ | {self.status}"

    def __repr__(self):
        return (f"ServiceBill(id='{self.bill_id}', room='{self.room_id}', "
            f"{self.month}/{self.year}, total={self.total_amount}, status='{self.status}')")

    def to_dict(self) -> dict:
        return   {
                "bill_id": self.bill_id,
                "contract_id": self.contract_id,
                "room_id": self.room_id,
                "month": self.month,
                "year": self.year,
                "electric_start": self.electric_start,
                "electric_end": self.electric_end,
                "water_start": self.water_start,
                "water_end": self.water_end,
                "electric_amount": self.electric_amount,
                "water_amount": self.water_amount,
                "total_amount": self.total_amount,
                "status": self.status,
                "due_date": self.due_date,
                "paid_date": self.paid_date
                }

    def is_overdue(self) -> bool: #Xem quá hạn hóa đơn chưa
        # logic: unpaid + quá due_date
        from datetime import date
        today = date.today()
        due = date.fromisoformat(self.due_date)
        return self.status == "unpaid" and today > due