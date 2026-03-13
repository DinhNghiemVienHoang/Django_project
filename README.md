# WEBSITE BÁN HOA TƯƠI – FLOWER SHOP

## 1. Mô tả đề tài
Website bán hoa tươi được xây dựng bằng ngôn ngữ lập trình **Python** sử dụng framework **Django**.  
Hệ thống phục vụ cho mục đích học tập và đáp ứng các tiêu chí của bài kiểm tra kỹ năng.

Website cho phép người dùng xem sản phẩm, đặt hàng và quản trị viên quản lý đơn hàng.

## 2. Công nghệ sử dụng
- Ngôn ngữ lập trình: Python  
- Framework: Django  
- Cơ sở dữ liệu: SQLite  
- Giao diện: HTML, CSS, Bootstrap

## 3. Cấu trúc dự án
Dự án được tổ chức theo cấu trúc chuẩn của Django:

Django_project/
│
├── core/ # App chính
│ ├── migrations/
│ ├── templates/
│ │ └── core/
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── dashboard.html
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│
├── config/ # Cấu hình project
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── media/ # Lưu ảnh sản phẩm
├── db.sqlite3 # Cơ sở dữ liệu SQLite
├── manage.py
├── requirements.txt
└── README.md

## 4. Các chức năng

### 4.1 Chức năng người dùng
- Xem danh sách sản phẩm hoa
- Đăng ký tài khoản
- Đăng nhập / đăng xuất
- Đặt hàng
- Xem đơn hàng của mình

### 4.2 Chức năng quản trị
- Quản lý sản phẩm hoa
- Xem danh sách đơn hàng
- Duyệt hoặc từ chối đơn hàng
- Xem thống kê số lượng đơn hàng và doanh thu

## 5. Kết nối cơ sở dữ liệu
Hệ thống sử dụng **SQLite** làm cơ sở dữ liệu, được cấu hình trong file `settings.py`.  
Dữ liệu được lưu trong file `db.sqlite3`.

Việc hiển thị danh sách sản phẩm và đơn hàng trên website chứng minh hệ thống đã kết nối cơ sở dữ liệu thành công.

## 6. Hiển thị dữ liệu mẫu (Seed data)
- Dữ liệu sản phẩm hoa được hiển thị trên **trang chủ**
- Dữ liệu đơn hàng được hiển thị trong **trang quản trị / dashboard**

Các dữ liệu này được tạo thông qua giao diện quản trị và quá trình đặt hàng của người dùng.

## 7. Giao diện, menu và layout thống nhất
- Website có **menu điều hướng**, **header** và **footer**
- Các thành phần này được xây dựng trong file `base.html`
- Các trang khác kế thừa layout chung thông qua template inheritance của Django

Nhờ đó, giao diện website được hiển thị thống nhất trên toàn bộ hệ thống.

## 8. Template inheritance
Dự án sử dụng template inheritance:
- `base.html` làm layout chung
- Các trang con kế thừa bằng `{% extends %}`

Cách làm này giúp giảm trùng lặp code và dễ bảo trì.

## 9. Phân quyền người dùng

Hệ thống phân quyền thành 3 vai trò:

- Guest (khách): 
  - Xem danh sách sản phẩm

- User (người dùng đã đăng nhập):
  - Đặt hàng
  - Xem đơn hàng của mình

- Admin (quản trị viên):
  - Quản lý sản phẩm
  - Quản lý danh mục
  - Duyệt / từ chối đơn hàng
  - Xem thống kê đơn hàng và doanh thu

## 10. Luồng xử lý đặt hàng

1. Người dùng đăng nhập hệ thống
2. Người dùng chọn sản phẩm
3. Nhấn nút "Đặt hàng"
4. Hệ thống tạo đơn hàng với trạng thái "pending"
5. Quản trị viên đăng nhập trang quản trị
6. Admin duyệt hoặc từ chối đơn hàng
7. Trạng thái đơn hàng được cập nhật:
   - pending
   - approved
   - rejected

## 11. Bảo mật hệ thống

Hệ thống sử dụng file .env để lưu các biến môi trường như SECRET_KEY và DEBUG nhằm tăng cường bảo mật và tách cấu hình khỏi mã nguồn.

## 12. Kiểm thử hệ thống

Các chức năng chính đã được kiểm thử thủ công:

- Đăng ký tài khoản
- Đăng nhập / đăng xuất
- Xem danh sách sản phẩm
- Tìm kiếm và sắp xếp sản phẩm
- Đặt hàng
- Xem đơn hàng của người dùng
- Duyệt / từ chối đơn hàng trong trang quản trị
- Hiển thị thống kê đơn hàng

Kết quả: Các chức năng hoạt động đúng theo yêu cầu.

## 13. Hướng dẫn chạy thử chương trình

### Bước 1: Cài đặt thư viện
pip install -r requirements.txt
### Bước 2: Khởi tạo cơ sở dữ liệu
python manage.py migrate
### Bước 3: Chạy chương trình
python manage.py runserver
### Bước 4: Truy cập hệ thống
Website: http://127.0.0.1:8000/
Trang quản trị: http://127.0.0.1:8000/admin/

## 14. Tài Khoản demo
Admin: 
username: admin
password: duanhoa123
User:
username: Duong_Em
password: duanhoa123