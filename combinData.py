import csv
import os

DATASET_FOLDER = "/home/dante/shareDANTE/KLTN/pythonFile/data"
DATA_ROOMS = ["room_1", "room_2", "room_3"]
DATA_SUBROOMS = [["1", "2", "3", "4"], ["1"], ["1", "2", "3", "4", "5"]]
# all_paths = []
# Label = []
# CSI = []
# for index, room in enumerate(DATA_ROOMS):
#     for subroom in DATA_SUBROOMS[index]:
#         all_paths.append(os.path.join(DATASET_FOLDER, room, subroom))
#         for index, path in enumerate(all_paths):
#             a = os.path.join(path, "data.csv")


# # Thư mục gốc chứa các thư mục room_1, room_2, ...
# DATASET_FOLDER = r"D:\Gitdesktop\KLTN\pythonFile\data"

# DATA_ROOMS = ["room_1", "room_2", "room_3"]
# DATA_SUBROOMS = [
#     ["1", "2", "3", "4"],  # Các subroom của room_1
#     ["1"],                 # Các subroom của room_2
#     ["1", "2", "3", "4", "5"]  # Các subroom của room_3
# ]

# Tên file kết quả
OUTPUT_CSV = r"/home/dante/shareDANTE/KLTN/pythonFile/Ndata/data.csv"

with open(OUTPUT_CSV, "w", newline="") as out_file:
    writer = None

    # 1️⃣ Duyệt qua từng room và từng subroom
    for room_idx, room in enumerate(DATA_ROOMS):
        for subroom in DATA_SUBROOMS[room_idx]:
            # Xây dựng đường dẫn đến file data.csv của từng subroom
            csv_path = os.path.join(DATASET_FOLDER, room, subroom, "data.csv")

            # Nếu file data.csv không tồn tại thì bỏ qua
            if not os.path.isfile(csv_path):
                print(f"[WARN] Không tìm thấy: {csv_path}")
                continue

            # 2️⃣ Mở từng file data.csv để đọc
            with open(csv_path, "r", newline="") as in_file:
                reader = csv.reader(in_file)
                writer = csv.writer(out_file)
                for row in reader:
                    # row là một list các giá trị trong data.csv
                    writer.writerow(row)

print("➜ Hoàn tất gộp dữ liệu vào", OUTPUT_CSV)
