# Backend API với FastAPI

Đây là một dự án backend API được xây dựng bằng FastAPI theo các tiêu chuẩn hiện đại, có cấu trúc tốt, dễ dàng bảo trì và mở rộng. Dự án đã bao gồm một module xác thực người dùng hoàn chỉnh sử dụng JWT (cả access token và refresh token).

## Công nghệ sử dụng

*   **Framework:** FastAPI
*   **Database:** PostgreSQL (thiết kế cho các hoạt động bất đồng bộ)
*   **ORM:** SQLAlchemy 2.0 (với cú pháp `async/await`)
*   **Database Migrations:** Alembic
*   **Validation & Serialization:** Pydantic V2
*   **Authentication:** JWT (JSON Web Tokens) qua `python-jose`
*   **Password Hashing:** `passlib` với thuật toán bcrypt
*   **Dependency Management:** Poetry
*   **Configuration:** `pydantic-settings` để quản lý biến môi trường
*   **Testing:** `pytest` và `httpx`

## Cấu trúc thư mục

Dự án được tổ chức theo cấu trúc như sau:

```
.
├── alembic/                  # Thư mục cho Alembic migrations
├── app/                      # Thư mục code chính
│   ├── api/                  # Nơi chứa các API routers
│   │   └── v1/
│   │       ├── deps.py         # Dependencies (vd: get_current_user)
│   │       └── endpoints/      # Các API endpoint
│   │           ├── auth.py
│   │           └── users.py
│   ├── core/                   # Cấu hình, settings của ứng dụng
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/                   # CRUD operations (tương tác với DB)
│   │   └── crud_user.py
│   ├── db/                     # Thiết lập session database
│   │   └── session.py
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── token.py
│   │   └── user.py
│   └── main.py                 # Entry point của ứng dụng FastAPI
├── tests/                    # Thư mục chứa unit/integration tests
├── .env.example              # File biến môi trường mẫu
├── .gitignore
├── pyproject.toml            # File quản lý dependencies của Poetry
└── README.md
```

## Hướng dẫn cài đặt và sử dụng

Làm theo các bước sau để cài đặt và chạy dự án trên máy của bạn.

### Yêu cầu
*   Python 3.11+
*   Poetry
*   Một instance PostgreSQL đang hoạt động (có thể là local hoặc trên cloud)

### 1. Clone dự án

```bash
git clone <URL_repository>
cd <tên_thư_mục_dự_án>
```

### 2. Cấu hình biến môi trường

Tạo file `.env` bằng cách sao chép từ file `env.example`:

```bash
# Trên Windows (Command Prompt hoặc PowerShell)
copy env.example .env

# Trên macOS/Linux
cp env.example .env
```

Mở file `.env` và cập nhật các giá trị với thông tin kết nối đến cơ sở dữ liệu của bạn:

```dotenv
# PostgreSQL
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=your_host
POSTGRES_DB=your_db_name
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}

# JWT
SECRET_KEY=một_chuỗi_bí_mật_ngẫu_nhiên_và_mạnh
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```
**Lưu ý quan trọng:** Giá trị của `SECRET_KEY` phải là một chuỗi ký tự ngẫu nhiên, dài và được giữ bí mật tuyệt đối trong môi trường production.

### 3. Cài đặt Dependencies

Sử dụng Poetry để cài đặt tất cả các thư viện cần thiết. Lệnh này sẽ tự động tạo một môi trường ảo và cài đặt các gói được định nghĩa trong `pyproject.toml`.

```bash
poetry install
```

### 4. Chạy Database Migrations

Áp dụng các migration để tạo các bảng cần thiết trong cơ sở dữ liệu của bạn (ví dụ: bảng `users`).

```bash
poetry run alembic upgrade head
```

## Chạy ứng dụng

Để khởi động server phát triển với tính năng tự động tải lại khi có thay đổi:

```bash
poetry run uvicorn app.main:app --reload
```

API sẽ có thể truy cập tại `http://127.0.0.1:8000`. Bạn có thể xem tài liệu API tương tác (Swagger UI) tại [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Triển khai với Docker trên aaPanel

### Yêu cầu
- aaPanel đã được cài đặt
- Docker và Docker Compose đã được cài đặt trên aaPanel
- PostgreSQL đã được cài đặt và cấu hình

### Các bước triển khai

1. **Tải mã nguồn lên server**

   Sử dụng Git hoặc tính năng Upload của aaPanel để tải mã nguồn lên thư mục của bạn trên server.

2. **Cấu hình biến môi trường**

   Tạo file `.env` từ file `env.example` và cập nhật thông tin kết nối database:

   ```bash
   cp env.example .env
   nano .env  # hoặc sử dụng trình soạn thảo của aaPanel
   ```

   Cập nhật thông tin kết nối database với thông tin PostgreSQL đã có:

   ```
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_SERVER=your_postgres_host
   POSTGRES_DB=your_postgres_db
   DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}
   ```

3. **Xây dựng và chạy container Docker**

   ```bash
   docker-compose up -d --build
   ```

   Lệnh này sẽ xây dựng image Docker cho ứng dụng và khởi chạy container ở chế độ nền.

4. **Chạy migrations (nếu cần)**

   ```bash
   docker-compose exec backend poetry run alembic upgrade head
   ```

5. **Cấu hình Reverse Proxy (Nginx)**

   Trong aaPanel, tạo một trang web mới hoặc cập nhật một trang web hiện có:
   
   - Vào phần **Website** trong aaPanel
   - Thêm một site mới hoặc chọn site hiện có
   - Vào **Proxy** và thêm một proxy mới:
     - Tên: api (hoặc tên bạn muốn)
     - Target URL: http://127.0.0.1:8000 (cổng của FastAPI)
     - Chọn **Enable Proxy**
     - Lưu cài đặt

   FastAPI sẽ có thể truy cập qua domain của bạn, ví dụ: https://api.yourdomain.com

6. **Kiểm tra hoạt động**

   Truy cập vào đường dẫn /docs để kiểm tra API đã hoạt động:
   
   ```
   https://api.yourdomain.com/docs
   ```

## Chạy Tests

Để thực thi bộ test của dự án:

```bash
poetry run pytest
```