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
HTTP 404

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
HTTP 404

```json
{
    "message": "Szi kiritgan parametirlar asosida xonalar topilmadi"
}
```


```
GET /api/rooms?type=new&search=mytaxi
```
HTTP 404

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

HTTP 200

```json
{
    "detail": "Siz kiritgan sahifa mavjud emas"
}
```


