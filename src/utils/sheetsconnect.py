from . import sh, time_voc
from .bookingtime import get_name


async def get_rec(time, wks):
    all_records = wks.get_all_records()
    rec_col = []
    for i in all_records:
        rec_col.append(i[time])

    try:
        while True:
            rec_col.remove("")
    except ValueError:
        pass

    return rec_col

async def sheetBookingDelete(vk_id, time):
    name = await get_name(vk_id)
    wks = sh.worksheet_by_title("Занятость")
    all_records = wks.get_all_records()

    rec_col = []
    for i in all_records:
        rec_col.append(i[time])

    wks.update_value(f"{time_voc.get(time)}{rec_col.index(name)+2}", "")


async def person_add(time, vk_id):
    name = await get_name(vk_id)
    wks = sh.worksheet_by_title("Занятость")
    rec_col = await get_rec(time, wks)
    wks.update_value(f"{time_voc.get(time)}{len(rec_col)+2}", name)
