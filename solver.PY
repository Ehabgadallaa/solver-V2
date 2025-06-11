
import subprocess
import sys

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pulp', 'pandas', 'openpyxl'])
    print("\n1.") #تم تثبيت المكتبات بنجاح
except subprocess.CalledProcessError as e:
    print(f"\n2: {e}") #حدث خطأ أثناء تثبيت المكتبا
    exit()
# --- الكود الأول: معالجة ملفات 'Sales DDP *.xlsx' ---
import pandas as pd
import re
import glob
import os

pattern_sales = os.path.join('Documents', 'Sales DDP *.xlsx')
matching_sales_files = glob.glob(pattern_sales)

#pattern_sales = 'Sales DDP *.xlsx'
#matching_sales_files = glob.glob(pattern_sales)
merged_sales_df = pd.DataFrame()  # تهيئة DataFrame لتخزين بيانات المبيعات المدمجة

if matching_sales_files:
    all_data_with_sheet_name = []
    output_sales_file = 'Sales DDP.xlsx'

    for source_file in matching_sales_files:
        print(f"\nجاري معالجة ملف المبيعات: {source_file}")
        try:
            xls = pd.ExcelFile(source_file)
            sheet_names = xls.sheet_names

            for i in range(1, 31):
                sheet_name_to_read = str(i)
                if sheet_name_to_read in sheet_names:
                    try:
                        # قراءة البيانات من الشيت المحدد بداية من الصف الرابع
                        df = pd.read_excel(xls, sheet_name=sheet_name_to_read, skiprows=3)

                        # إنشاء قاموس لتجميع البيانات لهذا الشيت مع اسم الشيت
                        merged_data_sheet = {}
                        base_columns_sheet = set()
                        for col in df.columns:
                            match = re.match(r'([a-zA-Z]+)(\.\d+)?', str(col))
                            if match:
                                base_columns_sheet.add(match.group(1))

                        for base_col in sorted(list(base_columns_sheet)):
                            all_values = []
                            for col in df.columns:
                                match = re.match(r'([a-zA-Z]+)(\.\d+)?', str(col))
                                if match and match.group(1) == base_col:
                                    all_values.extend(df[col].tolist())
                            merged_data_sheet[base_col] = all_values

                        # إضافة اسم الشيت إلى البيانات المجمعة لهذا الشيت
                        max_len_sheet = max(len(v) for v in merged_data_sheet.values()) if merged_data_sheet else 0
                        df_sheet = pd.DataFrame({col: data + [None] * (max_len_sheet - len(data))
                                                 for col, data in merged_data_sheet.items()})
                        if not df_sheet.empty:
                            df_sheet['Day'] = sheet_name_to_read

                            # تطبيق شروط التصفية: Status is null و QTY > 0
                            df_sheet_filtered = df_sheet[df_sheet['Status'].isnull() & (df_sheet['QTY'] > 0)]
                            all_data_with_sheet_name.append(df_sheet_filtered)

                        print(f"تمت معالجة الشيت '{sheet_name_to_read}' من الملف '{source_file}' وإضافة اسم الشيت وتطبيق شروط التصفية.")

                    except Exception as e:
                        print(f"حدث خطأ أثناء معالجة الشيت '{sheet_name_to_read}' من الملف '{source_file}': {e}")
                else:
                    print(f"الشيت '{sheet_name_to_read}' غير موجود في الملف '{source_file}'.")

        except FileNotFoundError:
            print(f'Error: الملف "{source_file}" غير موجود.')
        except Exception as e:
            print(f'حدث خطأ عام أثناء معالجة الملف "{source_file}": {e}')

    # دمج جميع البيانات من جميع الشيتات
    if all_data_with_sheet_name:
        merged_sales_df = pd.concat(all_data_with_sheet_name, ignore_index=True)

        # حفظ DataFrame المدمج إلى ملف Excel (سيتم استخدامه في الكود الثاني)
        try:
            merged_sales_df.to_excel(output_sales_file, index=False)
            print(f"\nتم تجميع ودمج بيانات المبيعات وحفظها في '{output_sales_file}'")
        except Exception as e:
            print(f"8'{output_sales_file}': {e}")#حدث خطأ أثناء حفظ ملف المبيعات 
    else:
        print("\n9.")#لم يتم العثور على أي بيانات مبيعات مطابقة للشروط

else:
    print(f"لم يتم العثور على أي ملفات تطابق نمط المبيعات '{pattern_sales}'")

# --- الكود الثاني: معالجة ملفات CSV ودمجها مع نتائج الكود الأول ---
pattern_order = 'order_search*.csv'
matching_order_files = glob.glob(pattern_order)

# اسم ملف Excel الأول المراد دمجه (الناتج من الكود الأول)
excel_file_path = 'Sales DDP.xlsx'
excel_sheet_name = 'Sheet1'
excel_order_column = 'Order'
excel_day_column = 'Day'  # اسم عمود اليوم في ملف Excel الأول

# اسم ملف Excel الثاني المراد دمجه (TZONE.xlsx)
tzone_excel_path = 'TZONE.xlsx'
tzone_sheet_name = 'Solver'
tzone_sap_column = 'SHIPTO_SAP_NO'  # اسم عمود الربط في TZONE.xlsx

# اسم العمود المشترك بعد الدمج الأول
merged_sap_column = 'SHIPTO_SAP_NO'

# اسم الملف Excel الذي سيتم حفظ المخرجات النهائية فيه
output_file_path_final = 'Order_Out.xlsx'

if matching_order_files:
    all_selected_data = []  # لجمع البيانات من جميع ملفات CSV

    for file_path in matching_order_files:
        print(f"\nجاري معالجة ملف CSV: {file_path}")
        try:
            # قراءة الملف CSV مع تحديد الفاصل المستخدم
            df_csv = pd.read_csv(file_path, sep=';')

            # التحقق من وجود عمود '#ORDER_NUMBER'
            if '#ORDER_NUMBER' not in df_csv.columns:
                print(f"تحذير: العمود '#ORDER_NUMBER' غير موجود في الملف '{file_path}'.")
                continue  # الانتقال إلى الملف التالي

            # استخراج أول 8 حروف من عمود '#ORDER_NUMBER'
            df_csv['ORDER_NUMBER_SHORT'] = df_csv['#ORDER_NUMBER'].astype(str).str[:8]

            # قائمة بأسماء الأعمدة المطلوبة من ملفات CSV (تأكد من وجود 'SHIPTO_SAP_NO')
            selected_columns_csv = ['SHIPTO_ADDRESS', 'CITY', 'ORDER_NUMBER_SHORT', 'SHIPTO_SAP_NO']

            # التحقق من وجود الأعمدة المطلوبة في DataFrame الخاص بملف CSV
            columns_not_found_csv = [col for col in selected_columns_csv if col not in df_csv.columns]
            if columns_not_found_csv:
                print(f"تحذير: الأعمدة التالية غير موجودة في الملف '{file_path}': {columns_not_found_csv}")
            else:
                # استخراج الأعمدة المحددة من ملف CSV
                selected_data_csv = df_csv[selected_columns_csv]

                # إضافة البيانات المستخرجة من ملف CSV إلى القائمة
                all_selected_data.append(selected_data_csv)

        except FileNotFoundError:
            print(f"خطأ: الملف '{file_path}' غير موجود.")
        except Exception as e:
            print(f"حدث خطأ أثناء معالجة الملف '{file_path}': {e}")

    # دمج البيانات من جميع ملفات CSV إذا كانت هناك أي بيانات
    if all_selected_data:
        combined_data_csv = pd.concat(all_selected_data, ignore_index=True)

        try:
            # قراءة ملف Excel الأول ('Sales DDP.xlsx') الناتج من الكود الأول
            df_excel = pd.read_excel(excel_file_path, sheet_name=excel_sheet_name)

            # التحقق من وجود عمود 'Order' في ملف Excel الأول
            if excel_order_column not in df_excel.columns:
                print(f"تحذير: العمود '{excel_order_column}' غير موجود في ملف Excel '{excel_file_path}' ورقة '{excel_sheet_name}'.")
            else:
                # استخراج أول 8 أرقام من عمود 'Order' في ملف Excel الأول وإنشاء عمود مطابق
                df_excel['ORDER_NUMBER_SHORT_EXCEL'] = df_excel[excel_order_column].astype(str).str[:8]

                # دمج البيانات بناءً على عمود ORDER_NUMBER_SHORT
                merged_data = pd.merge(combined_data_csv, df_excel, left_on='ORDER_NUMBER_SHORT', right_on='ORDER_NUMBER_SHORT_EXCEL', how='left')

                # إزالة العمود المساعد من ملف Excel الأول بعد الدمج
                merged_data.drop(columns=['ORDER_NUMBER_SHORT_EXCEL'], inplace=True)

                # إزالة الصفوف المكررة بناءً على عمود 'ORDER_NUMBER_SHORT' بعد الدمج
                merged_data.drop_duplicates(subset=['ORDER_NUMBER_SHORT'], keep='first', inplace=True)

                # **تصفية البيانات لإبقاء الصفوف التي تحتوي على قيمة في عمود 'Day'**
                if excel_day_column in merged_data.columns:
                    merged_data = merged_data.dropna(subset=[excel_day_column])

                    # **فرز البيانات بناءً على عمود 'Day'**
                    merged_data.sort_values(by=excel_day_column, inplace=True)
                else:
                    print(f"تحذير: العمود '{excel_day_column}' غير موجود في البيانات المدمجة، لذا لم يتم تطبيق تصفية أو فرز بناءً عليه.")

                print("\nfirast Sales DDP.xlsx:")#أول 5 صفوف من البيانات المدمجة مع
                print(merged_data.head())
                print("\n 5 Sales DDP.xlsx:")#أعمدة البيانات المدمجة مع 
                print(merged_data.columns)

                # --- الآن، قم بدمج البيانات مع ملف 'TZONE.xlsx' ---
                try:
                    # قراءة ملف Excel الثاني ('TZONE.xlsx')
                    df_tzone = pd.read_excel(tzone_excel_path, sheet_name=tzone_sheet_name)

                    print("\nأول 5 صفوف من بيانات TZONE.xlsx:")
                    print(df_tzone.head())
                    print("\nأعمدة بيانات TZONE.xlsx:")
                    print(df_tzone.columns)

                    # --- التحقق من أنواع البيانات ---
                    print(f"\nنوع بيانات عمود '{merged_sap_column}' في البيانات المدمجة:")
                    print(merged_data[merged_sap_column].dtype)

                    print(f"\nنوع بيانات عمود '{tzone_sap_column}' في بيانات TZONE:")
                    print(df_tzone[tzone_sap_column].dtype)
                    # --- نهاية التحقق من أنواع البيانات ---

                    # --- تنظيف عمود الربط في البيانات المدمجة ---
                    merged_data[merged_sap_column] = merged_data[merged_sap_column].astype(str).str.strip()

                    # --- تنظيف عمود الربط في بيانات TZONE ---
                    df_tzone[tzone_sap_column] = df_tzone[tzone_sap_column].astype(str).str.strip()

                    # دمج البيانات بناءً على عمود SHIPTO_SAP_NO
                    final_merged_data = pd.merge(merged_data, df_tzone, left_on=merged_sap_column, right_on=tzone_sap_column, how='left')

                    # عرض أول 5 صفوف من البيانات المدمجة النهائية
                    print("\nالبيانات المدمجة النهائية بعد دمجها مع 'TZONE.xlsx':")
                    print(final_merged_data.head())

                    # حفظ البيانات المدمجة النهائية إلى ملف Excel جديد
                    final_merged_data.to_excel(output_file_path_final, index=False)
                    print(f"\nتم حفظ البيانات المدمجة النهائية إلى ملف Excel '{output_file_path_final}'")

                except FileNotFoundError:
                    print(f"خطأ: الملف '{tzone_excel_path}' غير موجود.")
                except KeyError:
                    print(f"خطأ: الورقة '{tzone_sheet_name}' غير موجودة في ملف Excel '{tzone_excel_path}'.")
                except Exception as e:
                    print(f"حدث خطأ أثناء معالجة ملف Excel '{tzone_excel_path}': {e}")

        except FileNotFoundError:
            print(f"خطأ: ملف Excel '{excel_file_path}' غير موجود.")
        except KeyError:
            print(f"خطأ: الورقة '{excel_sheet_name}' غير موجودة في ملف Excel '{excel_file_path}'.")
        except Exception as e:
            print(f"حدث خطأ أثناء معالجة ملف Excel '{excel_file_path}': {e}")

    else:
        print("5") #print("لم يتم العثور على أي ملفات CSV لتتم معالجتها.")

