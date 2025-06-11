import pandas as pd

folder_path = r"D:\MyVBConsoleApp1\MyVBProject\Documents"
csv_file = f"{folder_path}\\order.csv"
excel_file = f"{folder_path}\\a.xlsx"

# استخدم جميع الإعدادات المناسبة
df = pd.read_csv(
    csv_file,
    sep=';',
    encoding='utf-8',
    quotechar='"',
    on_bad_lines='skip',
    engine='python'
)

print(df.head())  # لمراجعة شكل البيانات

df.to_excel(excel_file, index=False)

print("ok:", excel_file)