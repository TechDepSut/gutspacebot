import sqlite3


async def create_db():
    print("Creating database...")
    conn = sqlite3.connect("booking.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS availability(
        time INTEGER,
        amount INTEGER);
        """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS bookings(
    time TEXT,
    vid, TEXT);
    """
    )

    cursor.execute(
        """INSERT INTO availability(time, amount) VALUES
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (8, 0),
                (9, 0),
                (10, 0),
                (11, 0),
                (12, 0),
                (13, 0),
                (14, 0),
                (15, 0),
                (16, 0),
                (17, 0),
                (18, 0),
                (19, 0),
                (20, 0),
                (21, 0),
                (22, 0),
                (23, 0),
                (0, 0);
                    """
    )

    conn.commit()
    conn.close()
