import time
def myName_with_delay(name = None):
    if not name:
        time.sleep(5)
        print("Hello Saksham")
    else:
        print(f"Hello otta {name}")

myName_with_delay()

