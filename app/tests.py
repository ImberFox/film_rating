from django.test import TestCase
from app.models import FilmRating
from django.test import Client
import simplejson as json
class TestModels(TestCase):
    def setUp(self):
        FilmRating.objects.create(film_id=5, film_rating=0, user_id=1)
        FilmRating.objects.create(film_id=5, film_rating=2, user_id=2)
        FilmRating.objects.create(film_id=5, film_rating=10, user_id=4)
        FilmRating.objects.create(film_id=5, film_rating=4, user_id=3)
        FilmRating.objects.create(film_id=2, film_rating=1, user_id=1)
        FilmRating.objects.create(film_id=2, film_rating=3, user_id=4)
        FilmRating.objects.create(film_id=3, film_rating=2, user_id=1)
        FilmRating.objects.create(film_id=4, film_rating=0, user_id=1)

    def test_get_rating_Ok(self):
        rating = FilmRating.objects.get_rating(4)
        self.assertEqual(rating, 0)
        rating = FilmRating.objects.get_rating(5)
        self.assertEqual(rating, 4)

    def test_get_rating_no_film(self):
        rating = FilmRating.objects.get_rating(100)
        self.assertEqual(rating, -1)

    def test_update_rating(self):
        rating = FilmRating.objects.save_rating(5, 6, 1)
        self.assertEqual(rating, 5.5)

    def test_set_rating_exist(self):
        rating = FilmRating.objects.save_rating(4, 5, 2)
        self.assertEqual(rating, 2.5)

    def test_set_rating_new(self):
        rating = FilmRating.objects.save_rating(7, 8, 2)
        self.assertEqual(rating, 8)

    def test_delete(self):
        cnt = FilmRating.objects.delete_ratings_by_film_id(5)
        self.assertEqual(cnt[0], 4)

    def test_get_users_by_film_id_not_exist(self):
        val = FilmRating.objects.get_users_by_film(100)
        self.assertEqual(val, -1)

    def test_get_users_by_film_id__exist(self):
        val = FilmRating.objects.get_users_by_film(5)
        self.assertEqual(val, [1,2,4,3])

    def test_get_users_by_film_id_not_exist(self):
        val = FilmRating.objects.get_films_by_user(100)
        self.assertEqual(val, -1)

    def test_get_users_by_film_id_not_exist(self):
        val = FilmRating.objects.get_films_by_user(1)
        self.assertEqual(val, [5,2,3,4])



class TetsSetRating(TestCase):
    def setUp(self):
        self.client = Client()
        FilmRating.objects.create(film_id=5, film_rating=0, user_id=1)
        FilmRating.objects.create(film_id=5, film_rating=2, user_id=2)
        FilmRating.objects.create(film_id=5, film_rating=10, user_id=4)
        FilmRating.objects.create(film_id=5, film_rating=4, user_id=3)
        FilmRating.objects.create(film_id=2, film_rating=1, user_id=1)
        FilmRating.objects.create(film_id=2, film_rating=3, user_id=1)
        FilmRating.objects.create(film_id=3, film_rating=2, user_id=1)
        FilmRating.objects.create(film_id=4, film_rating=0, user_id=1)

    def test_no_film_id(self):
        response = self.client.post('/set_rating', json.dumps({"filmId": ""}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmId is Empty")


    def test_film_id_is_string(self):
        response = self.client.post('/set_rating', json.dumps({"filmId": "srgre"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmId is not a digit")

    def test_film_id_lower_zero(self):
        response = self.client.post('/set_rating', json.dumps({"filmId": "-5"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmId cant be < 0")


    def test_no_film_rating(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": ""}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmRating is Empty")

    def test_film_rating_is_string(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": "srg"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmRating is not a digit")

    def test_film_rating_lower_zero(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": "-5"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "filmRating cant be < 0")

    def test_no_user_id(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": "5"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "userId is Empty")

    def test_user_id_is_string(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": "5", "userId":"sg"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "userId is not a digit")

    def test_user_id_lower_zero(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"5", "filmRating": "5", "userId": "-5"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "userId cant be < 0")

    def test_set_rating_Ok(self):
        response = self.client.post('/set_rating', json.dumps({"filmId":"10", "filmRating": "5", "userId": "1"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['respMsg'], "Ok")
        self.assertEqual(data['filmAvgRating'], 5.0)

class TestGetRating(TestCase):
    def setUp(self):
        self.client = Client()
        FilmRating.objects.create(film_id=5, film_rating=0, user_id=1)
        FilmRating.objects.create(film_id=5, film_rating=2, user_id=2)
        FilmRating.objects.create(film_id=5, film_rating=10, user_id=4)
        FilmRating.objects.create(film_id=5, film_rating=4, user_id=3)
        FilmRating.objects.create(film_id=2, film_rating=1, user_id=1)
        FilmRating.objects.create(film_id=2, film_rating=3, user_id=1)
        FilmRating.objects.create(film_id=3, film_rating=2, user_id=1)
        FilmRating.objects.create(film_id=4, film_rating=0, user_id=1)

    def test_get_film_rating_id_id_string(self):
        response = self.client.get('/get_rating/sdgsdrg')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "id is not a digit")

    def test_get_film_rating_id_less_zero(self):
        response = self.client.get('/get_rating/-2')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "id is cant be less 0")

    def test_get_film_rating_not_exist(self):
        response = self.client.get('/get_rating/100')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['respMsg'], "no rating")

    def test_get_film_rating_id_ok(self):
        response = self.client.get('/get_rating/5')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['respMsg'], "Ok")
        self.assertEqual(data['filmAvgRating'], 4.0)

class TestStatus(TestCase):
    def test_status(self):
        client = Client()
        response = client.get('/status')
        self.assertEqual(response.status_code, 200)

class TestDeleteRating(TestCase):
    def setUp(self):
        self.client = Client()

    def test_null_id(self):
        response = self.client.post('/delete_film_rating', json.dumps({}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['respMsg'], "filmId is Empty")

    def test_invalid_id(self):
        response = self.client.post('/delete_film_rating', json.dumps({"filmId": "sef"}), content_type="application/json")
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['respMsg'], "filmId is not a digit")

    def test_ok(self):
        response = self.client.post('/delete_film_rating', json.dumps({"filmId": "5"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

class TestSearchByObject(TestCase):
    def setUp(self):
        self.client = Client()
        FilmRating.objects.create(film_id=5, film_rating=0, user_id=1)
        FilmRating.objects.create(film_id=5, film_rating=2, user_id=2)
        FilmRating.objects.create(film_id=5, film_rating=10, user_id=4)
        FilmRating.objects.create(film_id=5, film_rating=4, user_id=3)
        FilmRating.objects.create(film_id=2, film_rating=1, user_id=1)
        FilmRating.objects.create(film_id=2, film_rating=3, user_id=3)
        FilmRating.objects.create(film_id=3, film_rating=2, user_id=1)
        FilmRating.objects.create(film_id=4, film_rating=0, user_id=1)

    def test_search_id_string(self):
        response = self.client.get('/get_linked_objects/sdgsdrg')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "id is not a digit")

    def test_search_id_less_zero(self):
        response = self.client.get('/get_linked_objects/-2')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['respMsg'], "id is cant be less 0")

    def test_search_by_film_id_not_exist(self):
        response = self.client.get('/get_linked_objects/100?search_by=film_id')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['respMsg'], "no users rated this film")

    def test_search_by_film_id_ok(self):
        response = self.client.get('/get_linked_objects/5?search_by=film_id')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['respMsg'], "Ok")
        self.assertEqual(data['userId'], [1,2,4,3])

    def test_search_by_user_id_not_exist(self):
        response = self.client.get('/get_linked_objects/100?search_by=user_id')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['respMsg'], "no films rated by user")

    def test_search_by_user_ok(self):
        response = self.client.get('/get_linked_objects/1?search_by=user_id')
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['respMsg'], "Ok")
        self.assertEqual(data['filmId'], [5, 2,3,4])


# Create your tests here.
