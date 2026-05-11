from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

genres = [
    {"id": 1, "name": "Фантастика"},
    {"id": 2, "name": "Драма"},
    {"id": 3, "name": "Криминал"},
    {"id": 4, "name": "Приключения"},
]

countries = [
    {"id": 1, "name": "США"},
    {"id": 2, "name": "Великобритания"},
    {"id": 3, "name": "Новая Зеландия"},
    {"id": 4, "name": "Япония"},
]

directors = [
    {"id": 1, "name": "Кристофер Нолан", "country_id": 2},
    {"id": 2, "name": "Фрэнк Дарабонт", "country_id": 1},
    {"id": 3, "name": "Фрэнсис Форд Коппола", "country_id": 1},
    {"id": 4, "name": "Питер Джексон", "country_id": 3},
    {"id": 5, "name": "Хаяо Миядзаки", "country_id": 4},
]

actors = [
    {"id": 1, "name": "Леонардо ДиКаприо"},
    {"id": 2, "name": "Джозеф Гордон-Левитт"},
    {"id": 3, "name": "Тим Роббинс"},
    {"id": 4, "name": "Морган Фриман"},
    {"id": 5, "name": "Марлон Брандо"},
    {"id": 6, "name": "Элайджа Вуд"},
    {"id": 7, "name": "Руми Хиираги"},
]

movies = [
    {
        "id": 1,
        "title": "Начало",
        "original_title": "Inception",
        "description": "Вор, умеющий извлекать секреты из подсознания, получает шанс на искупление через невозможную задачу.",
        "release_year": 2010,
        "duration": 148,
        "rating": 8.8,
        "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "genre_id": 1,
        "director_id": 1,
        "roles": [
            {"actor_id": 1, "character": "Доминик Кобб"},
            {"actor_id": 2, "character": "Артур"},
        ],
    },
    {
        "id": 2,
        "title": "Побег из Шоушенка",
        "original_title": "The Shawshank Redemption",
        "description": "История надежды, дружбы и внутренней свободы в стенах строгой тюрьмы.",
        "release_year": 1994,
        "duration": 142,
        "rating": 9.3,
        "poster_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "genre_id": 2,
        "director_id": 2,
        "roles": [
            {"actor_id": 3, "character": "Энди Дюфрейн"},
            {"actor_id": 4, "character": "Эллис Реддинг"},
        ],
    },
    {
        "id": 3,
        "title": "Крестный отец",
        "original_title": "The Godfather",
        "description": "Сага о семье Корлеоне и цене власти в криминальном мире.",
        "release_year": 1972,
        "duration": 175,
        "rating": 9.2,
        "poster_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "genre_id": 3,
        "director_id": 3,
        "roles": [{"actor_id": 5, "character": "Вито Корлеоне"}],
    },
    {
        "id": 4,
        "title": "Властелин колец: Братство кольца",
        "original_title": "The Lord of the Rings: The Fellowship of the Ring",
        "description": "Первое путешествие Братства, которому предстоит уничтожить Кольцо Всевластия.",
        "release_year": 2001,
        "duration": 178,
        "rating": 8.9,
        "poster_url": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
        "genre_id": 4,
        "director_id": 4,
        "roles": [{"actor_id": 6, "character": "Фродо Бэггинс"}],
    },
    {
        "id": 5,
        "title": "Унесенные призраками",
        "original_title": "Sen to Chihiro no Kamikakushi",
        "description": "Девочка Тихиро попадает в мир духов и ищет путь домой, сохраняя смелость и память о себе.",
        "release_year": 2001,
        "duration": 125,
        "rating": 8.6,
        "poster_url": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
        "genre_id": 4,
        "director_id": 5,
        "roles": [{"actor_id": 7, "character": "Тихиро"}],
    },
]

users = [
    {"id": 1, "first_name": "Анна", "last_name": "Петрова", "email": "anna@example.com", "rank": "User"},
    {"id": 2, "first_name": "Иван", "last_name": "Смирнов", "email": "ivan@example.com", "rank": "Admin"},
]

reviews = [
    {
        "id": 1,
        "movie_id": 1,
        "user_id": 1,
        "rating": 9,
        "text": "Сильная идея и отличная визуальная подача.",
        "publication_date": "2026-05-01T10:00:00+00:00",
    },
    {
        "id": 2,
        "movie_id": 2,
        "user_id": 2,
        "rating": 10,
        "text": "Классика, которую легко рекомендовать почти каждому.",
        "publication_date": "2026-05-02T12:30:00+00:00",
    },
]


def find_by_id(items, item_id):
    return next((item for item in items if item["id"] == item_id), None)


def serialize_movie(movie, include_reviews=False):
    genre = find_by_id(genres, movie["genre_id"])
    director = find_by_id(directors, movie["director_id"])
    country = find_by_id(countries, director["country_id"]) if director else None
    movie_reviews = [serialize_review(review) for review in reviews if review["movie_id"] == movie["id"]]
    average_review_rating = None
    if movie_reviews:
        average_review_rating = round(sum(item["rating"] for item in movie_reviews) / len(movie_reviews), 1)

    payload = {
        **movie,
        "genre": genre["name"] if genre else None,
        "director": director["name"] if director else None,
        "country": country["name"] if country else None,
        "actors": [
            {
                "name": find_by_id(actors, role["actor_id"])["name"],
                "character": role["character"],
            }
            for role in movie["roles"]
            if find_by_id(actors, role["actor_id"])
        ],
        "review_count": len(movie_reviews),
        "average_review_rating": average_review_rating,
    }

    if include_reviews:
        payload["reviews"] = movie_reviews

    return payload


def serialize_review(review):
    user = find_by_id(users, review["user_id"])
    return {
        **review,
        "author": f"{user['first_name']} {user['last_name']}" if user else "Гость",
    }


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "movie-library"})


@app.get("/api/catalog")
def get_catalog():
    return jsonify(
        {
            "genres": genres,
            "countries": countries,
            "directors": [
                {
                    **director,
                    "country": find_by_id(countries, director["country_id"])["name"],
                }
                for director in directors
            ],
        }
    )


@app.get("/api/movies")
def get_movies():
    query = (request.args.get("q") or "").strip().lower()
    genre = (request.args.get("genre") or "").strip()
    country = (request.args.get("country") or "").strip()
    director = (request.args.get("director") or "").strip()
    year_from = request.args.get("year_from", type=int)
    year_to = request.args.get("year_to", type=int)

    result = [serialize_movie(movie) for movie in movies]

    if query:
        result = [
            movie
            for movie in result
            if query in movie["title"].lower()
            or query in movie["original_title"].lower()
            or query in movie["description"].lower()
        ]
    if genre:
        result = [movie for movie in result if movie["genre"] == genre]
    if country:
        result = [movie for movie in result if movie["country"] == country]
    if director:
        result = [movie for movie in result if movie["director"] == director]
    if year_from:
        result = [movie for movie in result if movie["release_year"] >= year_from]
    if year_to:
        result = [movie for movie in result if movie["release_year"] <= year_to]

    return jsonify(result)


@app.get("/api/movies/<int:movie_id>")
def get_movie(movie_id):
    movie = find_by_id(movies, movie_id)
    if not movie:
        return jsonify({"error": "movie not found"}), 404

    return jsonify(serialize_movie(movie, include_reviews=True))


@app.post("/api/movies")
def add_movie():
    payload = request.get_json(silent=True) or {}
    required_fields = ["title", "original_title", "release_year", "duration", "genre_id", "director_id"]
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        return jsonify({"error": "required fields are missing", "fields": missing_fields}), 400

    next_id = max((movie["id"] for movie in movies), default=0) + 1
    movie = {
        "id": next_id,
        "title": payload["title"].strip(),
        "original_title": payload["original_title"].strip(),
        "description": (payload.get("description") or "").strip(),
        "release_year": int(payload["release_year"]),
        "duration": int(payload["duration"]),
        "rating": float(payload.get("rating") or 0),
        "poster_url": (payload.get("poster_url") or "").strip(),
        "genre_id": int(payload["genre_id"]),
        "director_id": int(payload["director_id"]),
        "roles": payload.get("roles") or [],
    }
    movies.append(movie)
    return jsonify(serialize_movie(movie)), 201


@app.post("/api/movies/<int:movie_id>/reviews")
def add_review(movie_id):
    if not find_by_id(movies, movie_id):
        return jsonify({"error": "movie not found"}), 404

    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    rating = payload.get("rating")
    if not text:
        return jsonify({"error": "review text is required"}), 400
    if not isinstance(rating, int) or rating < 1 or rating > 10:
        return jsonify({"error": "rating must be an integer from 1 to 10"}), 400

    review = {
        "id": max((item["id"] for item in reviews), default=0) + 1,
        "movie_id": movie_id,
        "user_id": int(payload.get("user_id") or 1),
        "rating": rating,
        "text": text,
        "publication_date": datetime.now(timezone.utc).isoformat(),
    }
    reviews.append(review)
    return jsonify(serialize_review(review)), 201


@app.delete("/api/reviews/<int:review_id>")
def delete_review(review_id):
    review = find_by_id(reviews, review_id)
    if not review:
        return jsonify({"error": "review not found"}), 404

    reviews.remove(review)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
