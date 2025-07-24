from src.menu.app import App
from src.employee.queries import EmployeeInMemoryStore
from src.store.store import store

def main():
    # choose employee storing strategy
    s = EmployeeInMemoryStore(store)

    app = App(s)
    app.run()



if __name__ == "__main__":
    main()
