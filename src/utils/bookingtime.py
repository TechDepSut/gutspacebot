from datetime import datetime
import sqlite3
from . import err

async def checkReg(vk_id):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    name = cursor.execute(
        """
        SELECT name FROM users WHERE vid = ?;
        """,
        (vk_id, )
    ).fetchone()

    if name == None:
        return True
    else:
        return False

async def get_name(vk_id):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    name = cursor.execute(
        """
        SELECT name FROM users WHERE vid = ?;
        """,
        (vk_id, )
    ).fetchone()[0]

    conn.commit()
    conn.close()

    return name

async def registration(vk_id, name):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(vid, name)
        VALUES (?, ?);
        """,
        (vk_id, name)
    )

    conn.commit()
    conn.close()

async def timebuttons():
    if datetime.now().minute > 30:
        hour = int(datetime.now().hour) + 1
    else:
        hour = int(datetime.now().hour)

    # hour = 21

    btime = []

    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    if hour in err and hour != 16 and hour != 17:
        return btime

    for i in range(3):
        av = cursor.execute(
            "SELECT * FROM availability WHERE time = ? OR time = ? OR time = ?",
            (hour + i - 1, hour + i, hour + i + 1),
        ).fetchall()

        if (av[0][1] + av[1][1] < 30) and (av[1][1] + av[2][1] < 40):
            btime.append(str(av[1][0]) + ":00")

    if len(btime) == 0:
        return ["Full"]

    if hour == 16 or hour == 17:
        try:
            btime.remove("18:00")
            btime.remove("19:00")
        except:
            pass

    conn.commit()
    conn.close()

    return btime


async def bookingDB(txt, vk_id):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    av = cursor.execute(
        "SELECT * FROM availability WHERE time = ?", (txt.split(":")[0],)
    ).fetchall()
    cursor.execute(
        "UPDATE availability SET amount = ? WHERE time = ?", (av[0][1] + 1, av[0][0])
    )

    cursor.execute("INSERT INTO bookings(time, vid) VALUES(?, ?);", (txt, vk_id))

    conn.commit()
    conn.close()


async def bookingCheck(time, vk_id):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    bk = cursor.execute("SELECT * FROM bookings WHERE vid = ? and time = ?;", (vk_id, time)).fetchone()

    conn.commit()
    conn.close()

    print(time, vk_id)
    print(bk)

    if bk == None:
        return False
    else:
        return True
    
        
async def bookingDelete(vk_id, time):
    conn = conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM bookings WHERE vid = ? and time = ?
        """, 
        (vk_id, time)
    )

    time = int(time.split(':')[0])

    bk = int(cursor.execute("SELECT amount FROM availability WHERE time = ?", (time, )).fetchone()[0])
    cursor.execute("UPDATE availability SET amount = ? WHERE time = ?", (bk-1, time))

    conn.commit()
    conn.close()
