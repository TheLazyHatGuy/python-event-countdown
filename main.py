import datetime
import os
import sqlite3
import time


def create_db() -> bool:
    try:
        con = sqlite3.connect("main.db")
        c = con.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS event(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                  "title TEXT,"
                  "date TEXT)")

        c.close()
        con.close()
    except sqlite3.Error as e:
        print("Failed to create DB: ", e)
        return False
    else:
        print("DB ready")
        return True


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_events() -> list:
    try:
        con = sqlite3.connect("main.db")
        c = con.cursor()

        c.execute("SELECT title, date FROM event")
        events = c.fetchall()

        c.close()
        con.close()
    except sqlite3.Error as e:
        print("Failed to get from DB: ", e)
        return []
    else:
        return events


def add_event():
    clear()

    name = input("Event Name: ")
    date = input("Date (DD/MM/YYYY HH:MM:SS): ")

    try:
        con = sqlite3.connect("main.db")
        c = con.cursor()

        c.execute("INSERT INTO event(title, date) VALUES (?, ?)", (name, date))
        con.commit()

        c.close()
        con.close()
    except sqlite3.Error as e:
        print("Failed to insert to DB: ", e)
        time.sleep(10)
    else:
        print("Inserted successfully")
        time.sleep(1)


def delete_event():
    clear()

    try:
        con = sqlite3.connect("main.db")
        c = con.cursor()

        c.execute("SELECT id, title, date FROM event")
        events = c.fetchall()

        for event in events:
            print(event)

        print("\n")
        remove = input("Which ID do you want to delete: ")

        c.execute("DELETE FROM event WHERE id = ?", [remove])
        con.commit()

        c.close()
        con.close()
    except sqlite3.Error as e:
        print("Failed to insert to DB: ", e)
        time.sleep(10)
    else:
        print("Deleted successfully")
        time.sleep(1)


def print_events(events, current_time):
    if len(events) > 0:
        for event in events:
            try:
                date = datetime.datetime.strptime(event[1], "%d/%m/%Y %H:%M:%S")
                diff = date - current_time

                minutes, seconds = divmod(diff.seconds, 60)
                hours, minutes = divmod(minutes, 60)

                if diff.days > 0:
                    date_str = str(diff.days) + " Days, " + \
                               str(hours) + " Hours, " + \
                               str(minutes) + " Minutes, " + \
                               str(seconds) + " Seconds"
                elif hours > 0:
                    date_str = str(hours) + " Hours, " + \
                               str(minutes) + " Minutes, " + \
                               str(seconds) + " Seconds"
                elif minutes > 0:
                    date_str = str(minutes) + " Minutes, " + \
                               str(seconds) + " Seconds"
                else:
                    date_str = str(seconds) + " Seconds"
            except ValueError:
                print(B + event[0] + ": " + R + "INVALID DATE: " + W + event[1])
            else:
                print(B + event[0] + ": " + G + event[1] + W + " - " + date_str)
    else:
        print(R + "NO DATA" + W)


if __name__ == '__main__':
    # https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[36m'  # Cyan
    P = '\033[35m'  # purple

    run = create_db()

    while run:
        try:
            data = get_events()
            x = datetime.datetime.now()
            print(R + "Now: " + W + x.strftime("%d/%m/%Y %H:%M:%S"))
            print("\n\n")

            print_events(events=data, current_time=x)

            print("\n\n")
            print(B + "a: " + W + "Add Event")
            print(B + "d: " + W + "Delete Event")
            print(B + "q: " + W + "Quit")
            print("\n")

            user = input("> ")

            if len(user) > 0:
                command = user.lower()[0]
                if command == "q":
                    run = False
                elif command == "a":
                    add_event()
                elif command == "d":
                    delete_event()
                else:
                    print("Invalid command")
                    time.sleep(1)

            clear()
        except KeyboardInterrupt:
            # CTRL + C will kill the program gracefully
            run = False

    print("Bye")
