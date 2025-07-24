from datetime import datetime
from logs.listener import Listener

class EmployeeTransactionLogger(Listener):
    def update(self, payload):
        employee = payload.get("employee")
        if employee is None:
            return  # skip if no employee found

        if not hasattr(employee, "transactions"):
            employee.transactions = []

        employee.transactions.append({
            "type": payload.get("event_type", "unknown"),
            "description": payload.get("description", "No description"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
