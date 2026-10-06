import json
import csv
import datetime

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

def find_item():
    code = input("Nhập mã món: ")
    menu_data = read_file_csv("menu.csv")
    
    check = False
    for item in menu_data:
        if item['id'].lower() == code.lower():
            print(f"Mã: {item['id'].upper()} | Tên: {item['name']} | Nhóm: {item['category']} | Giá: {int(item['price']):,}")
            check = True
            return
        
    if not check:
        print(f"[ERR-04]: Không tìm thấy món có mã {code.upper()}")

def in_hoa_don(shop_in4, tam_tinh, giam_gia, VAT, tong_tien, HD):
    print("-"*30)
    print(f"Tạm tính  :   {tam_tinh:7,}")
    print(f"Giảm giá  :   {giam_gia:7,}")
    print(f"VAT ({shop_in4['vat_rate']*100:.0f}%)      :   {VAT:7,}")
    print(f"Tổng tiền :   {tong_tien:7,} {shop_in4['currency']}")
    print(f"[OK] Đã lưu đơn {HD} vào orders.txt")

def create_order():
    menu_data = read_file_csv("menu.csv")
    shop_in4 = read_file_json("config.json")
        
    list_order = []
    
    while True:
        choice = input("Nhập mã món (Enter để kết thúc): ")
        
        if not choice:
            break
        try:
            quantity = int(input("Số lượng: "))

            if quantity <= 0:
                print("ERR-05: Số lượng phải là số nguyên dương")
                continue

        except ValueError:
            print("ERR-05: Số lượng không hợp lệ")
            continue
        
        check = False
        for item in menu_data:
            if item['id'].lower() == choice.lower():
                price = int(item['price'])*quantity
                print(f"  + {item['name']} x{quantity} = {price}")
                list_order.append({"id": item['id'], "name": item['name'], "quantity": quantity, "price": price})
                check = True
                continue
            
        if not check:
            print(f"[ERR-04]: Không tìm thấy món có mã {choice.upper()}")
        
    tam_tinh = sum([item['price'] for item in list_order])
    giam_gia = 0
    if tam_tinh >= shop_in4['discount_threshold']:
        giam_gia = tam_tinh * shop_in4['discount_rate']
    VAT = (tam_tinh - giam_gia) * shop_in4['vat_rate']
    tong_tien = round(tam_tinh - giam_gia + VAT)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    with open("orders.txt", "r", encoding = 'utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        if lines:
            last_line = lines[-1]
            parts = last_line.split("|")
            last_HD = parts[1].strip()
            last_number = int(last_HD[2:])
            new_number = last_number + 1
            HD = f"HD{new_number:03d}"
        else:
            HD = "HD001"
    
    str_items = ", ".join([f"{item['id']}x{item['quantity']}" for item in list_order])
    
    with open("orders.txt", "a", encoding = 'utf-8') as f:
        f.writelines([
            f"{time} | {HD} | {str_items} | {tong_tien}\n"
        ])
    in_hoa_don(shop_in4, tam_tinh, giam_gia, VAT, tong_tien, HD)

def show_history():
    with open("orders.txt", "r", encoding = 'utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    if lines:
        print(f"{'MÃ ĐƠN':<7} {'THỜI GIAN':<20} {'TỔNG TIỀN'}")
        for line in lines:
            parts = line.split("|")
            print(f"{parts[1].strip():<7} {parts[0].strip():<20} {int(parts[3].strip()):,}")
    else:
        print("[ERR-06] Chưa có đơn hàng nào trong lịch sử.")

def export_report():
    shop_in4 = read_file_json("config.json")
    with open("orders.txt", "r", encoding = 'utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total_revenue = 0
    total_orders = len(lines)
    item_sold = {}
    
    for line in lines:
        parts = line.split("|")
        total_revenue += int(parts[3].strip())
        items = parts[2].strip().split(", ")
        
        for item in items:
            item_id, quantity = item.split("x")
            quantity = int(quantity)
            if item_id in item_sold:
                item_sold[item_id] += quantity
            else:
                item_sold[item_id] = quantity
    
    best_seller = max(item_sold, key=item_sold.get) if item_sold else None
    max_quantity = item_sold[best_seller] if item_sold else 0
    
    report_data = {
    "total_orders": total_orders,
    "total_revenue": total_revenue,
    "items_sold": item_sold,
    "best_seller": {
        "id": best_seller,
        "name": next(item['name'] for item in read_file_csv("menu.csv") if item['id'] == best_seller),
        "quantity": max_quantity
    } if best_seller else None
    }
    with open("report.json", "w", encoding = 'utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Đã xuất báo cáo ra report.json ({total_orders} đơn, doanh thu {total_revenue:,} VND)")
    

def main():
    while True:
        main_menu()
        choice = input("Chọn chức năng: ")
        if choice == "1":
            show_menu()
        elif choice == "2":
            find_item()
        elif choice == "3":
            create_order()
        elif choice == "4":
            show_history()
        elif choice == "5":
            export_report()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ")
if __name__ == "__main__":
    main()