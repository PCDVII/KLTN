import pandas as pd
from sklearn.model_selection import train_test_split

# ---------------------------------------
# 1) Đọc hai file data.csv và label.csv (không có header)
# ---------------------------------------
data_path = "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/data.csv"
label_path = "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/label.csv"

# Vì file không có header, ta dùng header=None
data_df = pd.read_csv(data_path, header=None)
label_df = pd.read_csv(label_path, header=None)

# Đặt tên cột cho label_df (giả sử label.csv có 2 cột: ID và nhãn string)
label_df.columns = ["id", "label", "nan1", "nan2"]

# ---------------------------------------
# 2) Kiểm tra NaN trong data_df
# ---------------------------------------
# Đếm số NaN trong toàn bộ data_df
nan_in_data = data_df.isna().sum().sum()
print(f"Số tổng NaN trong data (data_df): {nan_in_data}")

# Nếu muốn biết có bao nhiêu hàng chứa ít nhất một NaN:
rows_with_nan = data_df.isna().any(axis=1).sum()
print(f"Số dòng có NaN trong data_df: {rows_with_nan}")

# In vài dòng đầu có NaN để bạn kiểm tra (tuỳ chọn)
if rows_with_nan > 0:
    print("Ví dụ các dòng đầu có NaN trong data_df:")
    print(data_df[data_df.isna().any(axis=1)].head())

# ---------------------------------------
# 3) Drop tất cả những hàng trong data_df có NaN,
#    và tương ứng drop cùng index đó trong label_df
# ---------------------------------------
# Tạo mask: True ở những hàng không chứa bất kỳ NaN nào
mask_data_clean = data_df.notna().all(axis=1)

# Lọc data và label, rồi reset index
data_clean = data_df[mask_data_clean].reset_index(drop=True)
label_clean = label_df[mask_data_clean].reset_index(drop=True)

# Sau khi drop, in shape để kiểm tra
print(f"Sau khi loại NaN, shape của data_clean = {data_clean.shape}")
print(f"Sau khi loại NaN, shape của label_clean = {label_clean.shape}")

# ---------------------------------------
# 4) Chuẩn bị X và y cho việc chia tập
#    - X: tất cả các cột data_clean
#    - y: cột 'label' của label_clean
# ---------------------------------------
X = data_clean.copy()
y = label_clean[["label"]].copy()  # DataFrame chỉ chứa cột nhãn

# Kiểm tra lại: đảm bảo y không còn NaN
num_nan_label_after = y["label"].isna().sum()
print(f"Số NaN trong y sau khi drop data có NaN: {num_nan_label_after}")

# ---------------------------------------
# 5) Stratified split → 80% train, 10% val, 10% test
# ---------------------------------------
# 5.1) Tách 80% train, 20% temp
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y["label"]
)

# 5.2) Tách tiếp X_temp/y_temp thành 50% → validation (10% tổng) và 50% → test (10% tổng)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp["label"]
)

# ---------------------------------------
# 6) Ghi ra 6 file CSV riêng (data & label cho mỗi tập)
#    Lưu ý: index=False, header=False để file sạch, không có header và index
# ---------------------------------------
# Train
X_train.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/train/data.csv",
    index=False,
    header=False,
)
y_train.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/train/label.csv",
    index=True,
    header=False,
)

# Validation
X_val.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/val/data.csv",
    index=False,
    header=False,
)
y_val.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/val/label.csv",
    index=True,
    header=False,
)

# Test
X_test.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/test/data.csv",
    index=False,
    header=False,
)
y_test.to_csv(
    "/home/dante/shareDANTE/KLTN/pythonFile/Ndata/test/label.csv",
    index=True,
    header=False,
)

# ---------------------------------------
# 7) In phân phối nhãn để kiểm tra hiệu quả stratify
# ---------------------------------------
print("\n--- Phân phối nhãn sau khi chia ---")
print("Train:\n", y_train["label"].value_counts().sort_index(), "\n")
print("Validation:\n", y_val["label"].value_counts().sort_index(), "\n")
print("Test:\n", y_test["label"].value_counts().sort_index(), "\n")
