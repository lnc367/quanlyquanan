import json
import csv

def read_file_json(file_path):
    with open (file_path, "r", encoding = 'utf-8') as f:
        data = json.load(f)
    return data

def read_file_csv(file_path):
    with open (file_path, "r", encoding = 'utf-8') as f:
        data = list(csv.DictReader(f))
    return data

def main_menu():
    shop_data = read_file_json("config.json")
    title = f"====== {shop_data['shop_name'].upper()} ======"
    print(title)
    print("""1. Xem thực đơn
2. Tìm món theo mã
3. Tạo đơn hàng
4. Xem lịch sử đơn hàng
5. Xuất báo cáo doanh thu
0. Thoát""")
    print("="*len(title))

def show_menu():
    menu_data = read_file_csv("menu.csv")
    text = f"{'MÃ':<6} {'TÊN MÓN':<15} {'NHÓM':<7} {'ĐƠN GIÁ':>10}"
    print(text)
    print("-"*len(text))
    total = 0
    for product in menu_data:
        print(f"{product['id']:<6} {product['name']:<15} {product['category']:<7} {int(product['price']):>10,}")
        total += 1
    print("-"*len(text))
    print(f"Tổng số món: {total}")
    
def ERR_04(list,code,command):
    check = False
    for item in list:
        if item['id'].lower() == code.lower():
            print(f"Mã: {item['id'].upper()} | Tên: {item['name']} | Nhóm: {item['category']} | Giá: {int(item['price']):,}")
            check = True
            command
    if not check:
        print(f"[ERR-04]: Không tìm thấy món có mã {code.upper()}")

def find_item():
    code = input("Nhập mã món: ")
    menu_data = read_file_csv("menu.csv")
    ERR_04(menu_data,code,return)
    # check = False
    
    # for item in menu_data:
    #     if item['id'].lower() == code.lower():
    #         print(f"Mã: {item['id'].upper()} | Tên: {item['name']} | Nhóm: {item['category']} | Giá: {int(item['price']):,}")
    #         check = True
    #         return
    # if not check:
    #     print(f"[ERR-04]: Không tìm thấy món có mã {code.upper()}")
            
def create_order():
    menu_data = read_file_csv("menu.csv")
    while True:
        choice = input("Nhập mã món (Enter để kết thúc): ")
        if not choice:
            break
        quantity = int(input("Số lượng: "))
        for item in menu_data:
            if not(item['id'].lower() == choice.lower()):
                print(f"[ERR-04]: Không tìm thấy món có mã {choice.upper()}")
                continue
        
        
        print(f"")
        
def main():
    while True:
        main_menu()
        choice = input("Chọn chức năng: ")
        if choice == "1":
            show_menu()
        elif choice == "2":
            find_item()
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ")
if __name__ == "__main__":
    main()