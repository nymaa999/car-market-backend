<a id="readme-top"></a>

# Машины зарын системийн API гарын авлага

## Ерөнхий танилцуулга
Энэхүү баримт бичиг нь **Car Market** системийн Backend API-г фронтэнд (Web / Mobile) талаас хэрхэн ашиглахыг тайлбарлана.

## Үндсэн endpoint-ууд
- **Auth** – Бүртгүүлэх, Нэвтрэх
- **Cars** – Машины жагсаалт, хайлт, дэлгэрэнгүй, зар нэмэх
- **Reviews** – Үнэлгээ, сэтгэгдэл
- **Profiles** – Seller / Buyer профайл

---

## 1. Authentication (Хэрэглэгч)

### 1.1 Бүртгүүлэх
**Endpoint:** `POST /api/method/car_market.api.auth.sign_up`

Шинэ хэрэглэгч бүртгүүлэх.

**Request:**
```json
{
  "first_name": "Nyamdorj",
  "email": "nymaa@example.com",
  "phone": "99112233",
  "password": "secretpassword",
  "role": "buyer"
}
```

**Response (200 OK):**
```json
{
  "message": {
    "success": true,
    "message": "User created successfully"
  }
}
```

---

### 1.2 Нэвтрэх
**Endpoint:** `POST /api/method/car_market.api.auth.login`

**Request:**
```json
{
  "usr": "nymaa@example.com",
  "pwd": "secretpassword"
}
```

**Response (200 OK):**
```json
{
  "message": {
    "access_token": "<JWT_TOKEN>",
    "refresh_token": "<REFRESH_TOKEN>",
    "full_name": "Nyamdorj"
  }
}
```

---

## 2. Cars (Машины зарууд)

### 2.1 Зарын жагсаалт авах & Хайлт
**Endpoint:** `GET /api/method/car_market.api.cars.get_listings`

**Parameters:**
| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| brand | string | No | Машины брэнд (ж: Toyota) |
| min_price | float | No | Үнийн доод хязгаар |
| max_price | float | No | Үнийн дээд хязгаар |
| year | int | No | Үйлдвэрлэсэн он |

**Example Request:**
```
/api/method/car_market.api.cars.get_listings?brand=Toyota&max_price=50000000
```

**Response:**
```json
{
  "message": [
    {
      "name": "CAR-2025-0001",
      "title": "Toyota Prius 30",
      "brand": "Toyota",
      "price": 25000000,
      "main_image": "/files/prius30.jpg",
      "avg_rating": 4.5
    }
  ]
}
```

---

### 2.2 Зарын дэлгэрэнгүй
**Endpoint:** `GET /api/method/car_market.api.cars.get_detail`

**Parameters:**
| Parameter | Type | Description |
|---------|------|-------------|
| name | string | Зарын ID |

**Response:**
```json
{
  "message": {
    "title": "Toyota Prius 30 S Touring",
    "description": "Маш цэвэрхэн унасан",
    "price": 25000000,
    "year": 2015,
    "gallery": [
      {"image": "/files/img1.jpg"},
      {"image": "/files/img2.jpg"}
    ],
    "seller": {
      "full_name": "Bat",
      "phone": "99119911"
    }
  }
}
```

---

### 2.3 Шинэ зар оруулах (Seller only)
**Endpoint:** `POST /api/method/car_market.api.cars.create_listing`

**Request:**
```json
{
  "title": "Lexus 570 зарна",
  "brand": "Lexus",
  "model": "LX 570",
  "year": 2020,
  "price": 250000000,
  "mileage": 50000,
  "condition": "Used",
  "description": "Full option, хар өнгөтэй"
}
```

> Тайлбар: Зургийг тусдаа upload API ашиглан оруулна.

---

## 3. Reviews (Үнэлгээ)

### 3.1 Сэтгэгдэл бичих
**Endpoint:** `POST /api/method/car_market.api.reviews.create`

**Request:**
```json
{
  "listing": "CAR-2025-0001",
  "rating": 5,
  "comment": "Маш сайн машин байна."
}
```

---

### 3.2 Машины сэтгэгдлүүд авах
**Endpoint:** `GET /api/method/car_market.api.reviews.get_reviews`

**Parameters:**
| Parameter | Type | Description |
|---------|------|-------------|
| listing | string | Car Listing ID |

**Response:**
```json
{
  "message": [
    {
      "user": "Boldoo",
      "rating": 5,
      "comment": "Good car",
      "creation": "2025-12-05 10:00:00"
    }
  ]
}
```

---

## 4. Seller & Buyer Profile

### 4.1 Seller Profile үүсгэх
**Endpoint:** `POST /api/method/car_market.api.seller.create_profile`

**Request:**
```json
{
  "location": "Ulaanbaatar, Khan-Uul",
  "bio": "Найдвартай машин зардаг хувь хүн."
}
```

---

### 4.2 Хадгалсан зарууд (Buyer)
**Endpoint:** `POST /api/method/car_market.api.buyer.save_listing`

**Request:**
```json
{
  "listing": "CAR-2025-0001"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>