import os
from django.test import TestCase, Client, TransactionTestCase
from .models import LTBType, LTBNumber, LTBEditionNumber, LTBNumberSet, LTBEdition, LTB
from stock.models import Quant


class LTBNumberTestCase(TestCase):
    def setUp(self):
        LTBNumber.objects.create(
            number=1
        )
        LTBNumber.objects.create(
            number=2
        )
        LTBNumber.objects.create(
            number=4
        )
        LTBNumber.objects.create(
            number=6
        )
        LTBNumber.objects.create(
            number=10
        )
        LTBNumber.objects.create(
            number=101
        )
        LTBNumber.objects.create(
            number=147
        )

    def test_check_numbers(self):
        number_6 = LTBNumber.objects.filter(number=6).first()
        number_1 = LTBNumber.objects.filter(number=8).first()

        self.assertIsNotNone(number_6)
        self.assertEqual(number_6.filled_number(), "006")
        self.assertIsNone(number_1)

    def test_next_number(self):
        number = LTBNumber.objects.filter(number=1).first()

        self.assertIsNone(number.get_previous_number())

        next_number = number.get_next_number()
        self.assertEqual(str(next_number), "002")
        self.assertEqual(str(next_number.get_previous_number()), "001")

        next_number = next_number.get_next_number()
        self.assertEqual(str(next_number), "004")
        self.assertEqual(str(next_number.get_previous_number()), "002")

        next_number = next_number.get_next_number()
        self.assertEqual(str(next_number), "006")
        self.assertEqual(str(next_number.get_previous_number()), "004")

        next_number = next_number.get_next_number()
        self.assertEqual(str(next_number), "010")
        self.assertEqual(str(next_number.get_previous_number()), "006")

        next_number = next_number.get_next_number()
        self.assertEqual(str(next_number), "101")
        self.assertEqual(str(next_number.get_previous_number()), "010")

        next_number = next_number.get_next_number()
        self.assertEqual(str(next_number), "147")
        self.assertEqual(str(next_number.get_previous_number()), "101")

        self.assertIsNone(next_number.get_next_number())


class LTBEditionNumberTestCase(TestCase):

    def setUp(self):
        LTBEditionNumber.objects.create(
            number=1
        )
        LTBEditionNumber.objects.create(
            number=2
        )
        LTBEditionNumber.objects.create(
            number=3
        )

    def test_check_edition_numbers(self):
        number_1 = LTBEditionNumber.objects.filter(number=1).first()
        number_4 = LTBEditionNumber.objects.filter(number=4).first()

        self.assertIsNotNone(number_1)
        self.assertEqual(str(number_1), "1. Auflage")
        self.assertIsNone(number_4)


class LTBTypeTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        path = os.path.abspath('media/cover/')
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

    def setUp(self):
        LTBType.objects.create(
            name="LTB History",
            code="LTBH",
            auto_url=True,
            type_url="/ausgaben/nebenreihen/history",
            current_number=3,
        )
        LTBType.objects.create(
            name="LTB Fantasy",
            code="LTBF",
            auto_url=True,
            type_url="/ausgaben/nebenreihen/fantasy",
            current_number=2,
        )

    def test_check_typs(self):
        ltbh_type = LTBType.objects.filter(code='LTBH').first()
        none_type = LTBType.objects.filter(code='XYZ').first()

        self.assertIsNotNone(ltbh_type)
        self.assertEqual(ltbh_type.slug, "LTBH".lower())
        self.assertIsNone(none_type)

    def test_create_books(self):
        ltbh_type = LTBType.objects.filter(code='LTBH').first()
        ltbh_type.create_books()

        nummern = len(LTBNumber.objects.all())
        number_sets = len(LTBNumberSet.objects.all())
        edition = len(LTBEdition.objects.all())
        book = len(LTB.objects.all())
        self.assertEquals(nummern, 3)
        self.assertEquals(number_sets, 3)
        self.assertEquals(edition, 3)
        self.assertEquals(book, 3)

        first_number = ltbh_type.first_number()
        self.assertEquals(first_number.slug, 'ltbh001')

        last_number = ltbh_type.last_number()
        self.assertEquals(last_number.slug, 'ltbh003')

        all_numbers = ltbh_type.all_numbers()
        self.assertEquals(len(all_numbers), 3)


class LTBNumberSetTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        path = os.path.abspath('media/cover/')
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

    def setUp(self):
        ltb_type = LTBType.objects.create(
            name="LTB History",
            code="LTBH",
            auto_url=True,
            type_url="/ausgaben/nebenreihen/history",
            current_number=3,
        )

        number = LTBNumber.objects.create(
            number=1
        )

        LTBNumberSet.objects.create(
            ltb_number=number,
            ltb_type=ltb_type,
        )

    def test_check_number_sets(self):
        ltb_number_set_exist = LTBNumberSet.objects.filter(slug='ltbh001').first()
        ltb_number_set_none = LTBNumberSet.objects.filter(slug='ltbh002').first()

        self.assertIsNotNone(ltb_number_set_exist)
        self.assertEqual(str(ltb_number_set_exist), "LTBH001")
        self.assertIsNone(ltb_number_set_none)

    def test_create_editions(self):
        ltb_number_set = LTBNumberSet.objects.filter(slug='ltbh001').first()
        ltb_number_set.create_editions()

        editions = len(LTBEdition.objects.all())
        edition = LTBEdition.objects.first()

        self.assertEqual(editions, 1)
        self.assertIsNotNone(edition)
        self.assertEqual(str(edition), "LTBH001 - Geheimnisse der Frühgeschichte 1. Auflage")


class LTBEditionTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        path = os.path.abspath('media/cover/')
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

    def setUp(self):
        ltb_type = LTBType.objects.create(
            name="LTB History",
            code="LTBH",
            auto_url=True,
            type_url="/ausgaben/nebenreihen/history",
            current_number=3,
        )

        ltb_number = LTBNumber.objects.create(
            number=1
        )

        ltb_number_set = LTBNumberSet.objects.create(
            ltb_number=ltb_number,
            ltb_type=ltb_type,
        )
        ltb_number_set.create_editions()

    def test_check_editions(self):
        ltb_edition_exist = LTBEdition.objects.filter(slug='ltbh001_e1').first()
        ltb_edition_none = LTBEdition.objects.filter(slug='ltbh001_e2').first()

        self.assertIsNotNone(ltb_edition_exist)
        self.assertEqual(str(ltb_edition_exist), "LTBH001 - Geheimnisse der Frühgeschichte 1. Auflage")
        self.assertIsNone(ltb_edition_none)


class LTBTTestCase(TestCase):
    ltb_edition = None

    @classmethod
    def tearDownClass(cls):
        path = os.path.abspath('media/cover/')
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))

    def setUp(self):
        ltb_type = LTBType.objects.create(
            name="Lustiges Taschenbuch",
            code="LTB",
            auto_url=True,
            type_url="/ausgaben/alle-ausgaben",
            current_number=2,
        )
        ltb_type.create_books()

        ltb_number = LTBNumber.objects.create(
            number=459
        )

        ltb_number_set = LTBNumberSet.objects.create(
            ltb_number=ltb_number,
            ltb_type=ltb_type,
        )
        ltb_number_set.create_editions()

        ltb = LTB.objects.filter(slug="ltb459_e1_1").get()
        ltb.name = "Blaue Edition"
        ltb.save()

        self.ltb_edition = LTBEdition.objects.filter(slug='ltb459_e1').first()

        ltb_version_2 = LTB(
            ltb_edition=self.ltb_edition,
            name="Rote Edition",
            sort=2,
            image_url="https://inducks.org/hr.php?normalsize=1&image=https://outducks.org/webusers/webusers/2014/10/de_ltb_459aa_001.jpg"
        )
        ltb_version_2.save()

        ltb_version3 = LTB(
            ltb_edition=self.ltb_edition,
            name="Grüne Edition",
            sort=3,
            image_url="https://inducks.org/hr.php?normalsize=1&image=https://outducks.org/webusers/webusers/2014/10/de_ltb_459ca_001.jpg"
        )
        ltb_version3.save()

    def check_ltb(self, ltb, data):
        self.assertIsNotNone(ltb)
        self.assertEqual(ltb.slug, data['slug'])
        self.assertEqual(ltb.complete_name_calc, data['name'])
        self.assertEqual(ltb.edition, data['edition'])
        self.assertEqual(ltb.number, data['number'])
        self.assertEqual(ltb.type, data['type'])
        self.assertEqual(ltb.stories, data['stories'])
        self.assertEqual(ltb.pages, data['pages'])
        self.assertEqual(str(ltb.release_date), data['release_date'])
        self.assertEqual(str(ltb), data['string'])

    def test_check_ltbs(self):
        ltb_1 = LTB.objects.filter(slug="ltb001_e1_1").first()
        ltb_2 = LTB.objects.filter(slug="ltb002_e2_1").first()
        ltb_3 = LTB.objects.filter(slug="ltb459_e1_2").first()
        ltb_none = LTB.objects.filter(slug="ltb003_e1_1").first()

        self.check_ltb(ltb_1, {
            'slug': "ltb001_e1_1",
            'name': "Der Kolumbusfalter",
            'edition': "1. Auflage",
            'number': "001",
            'type': "Lustiges Taschenbuch",
            'stories': 5,
            'pages': 250,
            'release_date': "1967-10-01",
            'string': "LTB001 - Der Kolumbusfalter 1. Auflage"
        })
        self.check_ltb(ltb_2, {
            'slug': "ltb002_e2_1",
            'name': "\"Hallo...Hier Micky!\"",
            'edition': "2. Auflage",
            'number': "002",
            'type': "Lustiges Taschenbuch",
            'stories': 5,
            'pages': 250,
            'release_date': "1990-01-01",
            'string': "LTB002 - \"Hallo...Hier Micky!\" 2. Auflage"
        })
        self.check_ltb(ltb_3, {
            'slug': "ltb459_e1_2",
            'name': "Der Fluch der Farben (Rote Edition)",
            'edition': "1. Auflage",
            'number': "459",
            'type': "Lustiges Taschenbuch",
            'stories': 10,
            'pages': 250,
            'release_date': "2014-09-16",
            'string': "LTB459 - Der Fluch der Farben (Rote Edition) 1. Auflage"
        })

        self.assertIsNone(ltb_none)

    def test_ltb_navigation(self):
        ltb = LTB.objects.filter(slug="ltb001_e1_1").first()

        self.assertIsNone(ltb.previous_ltb())

        next_ltb = ltb.next_ltb()
        self.assertEqual(next_ltb.slug, "ltb002_e1_1")
        self.assertEqual(next_ltb.previous_ltb().slug, "ltb001_e1_1")

        next_ltb = next_ltb.next_ltb()
        self.assertEqual(next_ltb.slug, "ltb459_e1_1")
        self.assertEqual(next_ltb.previous_ltb().slug, "ltb002_e1_1")

        self.assertIsNone(next_ltb.next_ltb())

    def test_editions(self):
        ltb_1 = LTB.objects.filter(slug="ltb001_e1_1").first()
        ltb_2 = LTB.objects.filter(slug="ltb002_e1_1").first()
        ltb_3 = LTB.objects.filter(slug="ltb459_e1_1").first()

        editions_1_count = ltb_1.ltb_editions_count()
        self.assertEqual(editions_1_count, 3)

        editions_2_count = ltb_2.ltb_editions_count()
        self.assertEqual(editions_2_count, 3)

        editions_3_count = ltb_3.ltb_editions_count()
        self.assertEqual(editions_3_count, 1)

    def test_versions(self):
        ltb_1 = LTB.objects.filter(slug="ltb459_e1_1").first()
        ltb_2 = LTB.objects.filter(slug="ltb459_e1_2").first()
        ltb_3 = LTB.objects.filter(slug="ltb459_e1_3").first()

        versions_1_count = ltb_1.ltb_versions_count()
        self.assertEqual(versions_1_count, 3)

        versions_2_count = ltb_2.ltb_versions_count()
        self.assertEqual(versions_2_count, 3)

        versions_3_count = ltb_3.ltb_versions_count()
        self.assertEqual(versions_3_count, 3)

    def test_absolute_url(self):
        ltb_1 = LTB.objects.filter(slug="ltb001_e1_1").first()
        ltb_2 = LTB.objects.filter(slug="ltb002_e2_1").first()
        ltb_3 = LTB.objects.filter(slug="ltb459_e1_2").first()

        self.assertEqual(ltb_1.get_absolute_url(), "/ltb/detail/ltb001_e1_1")
        self.assertEqual(ltb_2.get_absolute_url(), "/ltb/detail/ltb002_e2_1")
        self.assertEqual(ltb_3.get_absolute_url(), "/ltb/detail/ltb459_e1_2")

    def test_quatns(self):
        ltb_1 = LTB.objects.filter(slug="ltb001_e1_1").first()
        ltb_2 = LTB.objects.filter(slug="ltb002_e1_1").first()
        ltb_3 = LTB.objects.filter(slug="ltb459_e1_1").first()
        ltb_4 = LTB.objects.filter(slug="ltb002_e2_1").first()

        Quant(book=ltb_1, is_first_edition=True).save()
        Quant(book=ltb_1, is_first_edition=False).save()
        Quant(book=ltb_1, is_first_edition=False).save()

        Quant(book=ltb_2, is_first_edition=False).save()
        Quant(book=ltb_2, is_first_edition=False).save()

        Quant(book=ltb_3, is_first_edition=False).save()
        Quant(book=ltb_3, is_first_edition=False).save()
        Quant(book=ltb_3, is_first_edition=True).save()

        self.assertEqual(ltb_1.inventory_count(), 3)
        self.assertTrue(ltb_1.have_first_edition())
        self.assertEqual(ltb_2.inventory_count(), 2)
        self.assertFalse(ltb_2.have_first_edition())
        self.assertEqual(ltb_3.inventory_count(), 3)
        self.assertTrue(ltb_3.have_first_edition())
        self.assertEqual(ltb_4.inventory_count(), 0)
        self.assertFalse(ltb_4.have_first_edition())

        self.assertEqual(len(LTB.in_stock.all()), 3)
        self.assertEqual(len(LTB.not_in_stock.all()), 6)


# class LTBViewTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         ltb_type = LTBType(
#             name="Lustiges Taschenbuch",
#             code="LTB",
#             auto_url=True,
#             type_url="/ausgaben/alle-ausgaben",
#             current_number=3,
#         )
#         ltb_type.save()
#         ltb_type.create_books()
#
#     @classmethod
#     def tearDownClass(cls):
#         path = os.path.abspath('media/cover/')
#         filelist = [f for f in os.listdir(path)]
#         for f in filelist:
#             os.remove(os.path.join(path, f))

