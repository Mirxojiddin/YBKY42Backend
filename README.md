# YBKY42Backend
Impactt co-working markazi rezidentlariga majlis xonalarni oldindan oson band qilish loyihasi backend qismi

# Tizim imkoniyatlari
-Xona ma'lumotlarini ko'rish
-Xonani bosh vaqtlarini  bildinagan resident uchun band qilish
-Faqat ish vaqtida belgiash

# Impacttdagi xonalarni mavjud ko'rish uchun API


```
GET /api/rooms
```

Parametrlar:

- `search`: Xona nomi orqali qidirish
- `type`: xona turi bo'yicha saralash (`focus`, `team`, `conference`)
- `page`: sahifa tartib raqami
- `page_size`: sahifadagi maksimum natijalar soni

HTTP 200

```json
{
    "page": 1,
    "count": 3,
    "page_size": 10,
    "results": [
        {
            "id": 1,
            "name": "express24",
            "type": "conference",
            "capacity": 15
        },
        {
            "id": 2,
            "name": "mytaxi",
            "type": "focus",
            "capacity": 1
        },
        {
            "id": 3,
            "name": "workly",
            "type": "team",
            "capacity": 5
        }
    ]
}
```

```
GET /api/rooms?search=workly
```
HTTP 200

```json
{
    "page": 1,
    "count": 1,
    "page_size": 10,
    "results": [
                {
            "id": 3,
            "name": "workly",
            "type": "team",
            "capacity": 5
        }
    ]
}
```
```
GET /api/rooms?search=new
```
HTTP 404 Mavjud bo'lmagan search ni kiritganda

```json
{
    "message": "Szi kiritgan parametirlar asosida xonalar topilmadi"
}
```

```
GET /api/rooms?type=focus
```

HTTP 200

```json
{
    "page": 1,
    "count": 1,
    "page_size": 10,
    "results": [
        {
            "id": 2,
            "name": "mytaxi",
            "type": "focus",
            "capacity": 1
        },
    ]
}
```

```
GET /api/rooms?type=new 
```
HTTP 404 Mavjud bo'lmagan type ni kiritganda

```json
{
    "message": "Szi kiritgan parametirlar asosida xonalar topilmadi"
}
```


```
GET /api/rooms?type=new&search=mytaxi
```
HTTP 404 Noto'g'ri type yoki search kiritganda

```json
{
    "message": "Szi kiritgan parametirlar asosida xonalar topilmadi"
}
```

```
GET /api/rooms?page_size=2
```

HTTP 200

```json
{
    "page": 1,
    "count": 3,
    "page_size": 2,
    "results": [
        {
            "id": 1,
            "name": "express24",
            "type": "conference",
            "capacity": 15
        },
        {
            "id": 2,
            "name": "mytaxi",
            "type": "focus",
            "capacity": 1
        },
    ]
}
```

```
GET /api/rooms?page=3
```

HTTP 404 Noto'g'ri page ni kiritganda

```json
{
    "detail": "Siz kiritgan sahifa mavjud emas"
}
```
# Xonani id orqali olish uchun API
```
GET /api/rooms/{id}
```
HTTP 200

```json
{
    "id": 1,
    "name": "express24",
    "type": "conference",
    "capacity": 15
}

```

HTTP 404 Mavjud bo'lmagan kunni kiritganda

```json
{
  "error": "Bunday xona topilmadi"
}

```


# Xonaning bo'sh vaqtlarini olish uchun API

```
GET /api/rooms/{id}/availability
```

Parametrlar:

- `date`: sana (ko'rsatilmasa bugungi sana olinadi)

Response 200 

```json
[
  {
    "start": "05-06-2023 9:00:00",
    "end": "05-06-2023 11:00:00"
  },
  {
    "start": "05-06-2023 13:00:00",
    "end": "05-06-2023 18:00:00"
  }
]
```

Response 400 Date ni noto'g'ri formatda kiritganda

```json
{
  "error": "Iltimos 'date' ni yil - oy - kun formatida kiriting"
}
```
Response 400 joriy kunda oldingi kunlarni kiritganda

```json
{
   "error": "Iltimos bugundan avvalgi kunni kiritmang"
}
```

Response 404 xona uchun bosh vaqt bo'lmaganda

```json
{
    "massage": "Xonaning {date} kuni uchun bosh vaqtlari topilmadi"
}
```

HTTP 404 Noto'g'ri xona tanlaganda

```json
{
  "error": "Bunday xona topilmadi"
}

```


---

## Xonani band qilish uchun API

```
POST /api/rooms/{id}/book
```

```json
{
  "resident": {
    "name": "Anvar Sanayev"
  },
  "start": "05-06-2023 9:00:00",
  "end": "05-06-2023 10:00:00"
}
```

---

HTTP 201: Xona muvaffaqiyatli band qilinganda

```json
{
  "message": "xona muvaffaqiyatli band qilindi"
}
```

HTTP 410: Tanlangan vaqtda xona band bo'lganda

```json
{
  "error": "Uzr, siz tanlagan vaqtda xona band qilingan"
}
```

# Validation data



HTTP 404 Noto'g'ri xona tanlaganda

```json
{
  "error": "Bunday xona topilmadi"
}

```

HTTP 404 xonada bo'sh qatlar mavjud bo'lmaganda

```json
{
  "error": "Xonaning siz tanlagan kuni uchun bosh vaqtlari topilmadi"
}

```

Response 400 joriy kunda oldingi kunlarni kiritganda

```json
{
   "error": "Iltimos bugundan avvalgi kunni kiritmang"
}
```

Response 400 resident ma'lumotlari kiritilmaganda

```json
{
   "error": "Iltimos resident ma'lumotlarini kiriting"
}
```

Response 400 residentning 'name' parametiri kiritlmaganda 

```json
{
   "error": "Iltimos resinedtni ismini 'name' orqali kiriting"
}
```

Response 400 start yoki end paramettlaridan biri yoki har ikkasi kiritilmaganda 

```json
{
   "error": "Iltimos start va end maydonlarni ikkisini ham kitiring"
}
```

Response 400 start yoki end noto'g'ri formatda kiritlganda

```json
{
   "error": "Iltimos sanalarnini y-o-k s-d-sek formatida kiriting"
}
```

Response 400 start va end o'zaro teng bo'lmagan kunni kiritganda

```json
{
   "error": "start va end ga kiritayotgan kunlari bir xil bo'lishi kerak"
}
```

Response 400 start va end ga joriy kundan oldingi kunlarini kiritganda

```json
{
   "error": "Iltimos bugundan avvalgi kunni kiritmang"
}
```

Response 400 startning vaqti enddan katta kiritlganda

```json
{
   "error": "start ning vaqti  endning vaqtidan kichik bo'lishi kerak"
}
```

Validationdan o'tgan ma'lumotlar qayta ishlanadi







