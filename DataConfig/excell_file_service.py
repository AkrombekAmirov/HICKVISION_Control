from DatabaseService.core import DatabaseService1, User
from DataConfig.file_path import get_file_path
from openpyxl import load_workbook, Workbook
from LoggingService import LoggerService
import asyncio

db = DatabaseService1(logger=LoggerService())


async def read_excel():
    file_path = await get_file_path("students.xlsx")
    workbook = load_workbook(file_path)
    sheet = workbook.active
    rows = list(sheet.iter_rows(min_row=2, values_only=True))
    try:
        for row in rows:
            print(row, end="\n")
            print(row[0])
            await db.add(
                User(username=str(row[1]), password=str(row[2]), external_id=str(row[0]), full_name=str(row[4]) or 'None',
                     gender='Erkak',
                     faculty_id=int(row[6]) or 0, turniket_id=str(row[7]) or 'None', begin_time=(row[8]), end_time=(row[9]),
                     image_url='https://hemis.tdpu.uz/static//pi/b/4/b46a147cd59b84df2eafb2aceee64724.jpg',
                     created_at=row[11], student_id=str(row[12]), file_path=str(row[13]),
                     group_id=row[14] or 0, group_name=str(row[15]), speciality_id='None', speciality_name=str(row[17])
                     ))
            # break
    # (38, 1 355241102426, 2 'AD4373857', 3 None, 4 'PARDAYEVA MADINA MUSURMON QIZI', 5 'Ayol', 6 1, 7 20250001, 8 datetime.datetime(2025, 9, 6, 16, 15, 34, 78000), 9
    # 9 datetime.datetime(2029, 9, 5, 16, 15, 34, 78000), 10 'https://hemis.tdpu.uz/static/crop/2/6/320_320_90_2675932958.jpg', 11 datetime.datetime(2025, 9, 6, 16, 15, 34, 83000),
    # 12 355241102426, 13 'students\\355241102426_PARDAYEVA_MADINA_MUSURMON_QIZI_20250001.json', 14 1954, 15 'M uz 101 kechki 2025', 16 '8caf66ec-98a3-4f65-8582-0cf6ce38aa05', 17 'Matematika')
    except Exception as ex:
        print(ex)
    finally:
        workbook.close()


if __name__ == "__main__":
    asyncio.run(read_excel())
