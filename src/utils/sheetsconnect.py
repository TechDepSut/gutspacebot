from . import sh, time_voc


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


# async def bookingCheck(time, vk_id):
# wks = sh.worksheet_by_title("VK_ID")
# rec_col = await get_rec(time, wks)
#
# if vk_id in rec_col:
# return True
#
# wks.update_value(f"{time_voc.get(time)}{len(rec_col)+2}", vk_id)
#
# return False


async def person_add(time, name):
    wks = sh.worksheet_by_title("Занятость")
    rec_col = await get_rec(time, wks)
    wks.update_value(f"{time_voc.get(time)}{len(rec_col)+2}", name)
