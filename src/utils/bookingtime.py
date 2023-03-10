from datetime import datetime
import sqlite3
from . import err


async def timebuttons():
    if datetime.now().minute > 30:
        hour = int(datetime.now().hour) + 1
    else:
        hour = int(datetime.now().hour)

    # hour = 2

    btime = []

    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    if hour in err and hour != 19 and hour != 20:
        return btime

    for i in range(3):
        av = cursor.execute(
            "SELECT * FROM availability WHERE time = ? OR time = ? OR time = ?",
            (hour + i - 1, hour + i, hour + i + 1),
        ).fetchall()

        if (av[0][1] + av[1][1] < 30) & (av[1][1] + av[2][1] < 30):
            btime.append(str(av[1][0]) + ":00")


    if len(btime) == 0:
        return ['Full']

    if hour == 19 or hour == 20:
        try:
            btime.remove("21:00")
            btime.remove("22:00")
        except:
            pass

    conn.commit()
    conn.close()

    return btime


async def bookingDB(txt):
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    av = cursor.execute(
        "SELECT * FROM availability WHERE time = ?", (txt.split(":")[0],)
    ).fetchall()
    cursor.execute(
        "UPDATE availability SET amount = ? WHERE time = ?", (av[0][1] + 1, av[0][0])
    )

    conn.commit()
    conn.close()
