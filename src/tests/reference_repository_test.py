import unittest
from utils.initialize_test_database import initialize_test_database
from repositories.reference_repository import test_reference_repository as ref_repository

BOOK_ENTRY_DATA = {
    "address": "Osoite123",
    "author": "Authori",
    "edition": "1",
    "editor": "Editor123",
    "month": "January",
    "note": "This is a note",
    "number": "4",
    "publisher": "Otava",
    "series": "Series?",
    "title": "Muumit laaksossa",
    "volume": "2",
    "year": "2022",
    "author_firstname": "Authori",
    "author_lastname": "Authorinen"
}


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        # initilizes the database and inserts two references into the database
        initialize_test_database()
        self._ref_repository = ref_repository
        self._ref_repository.add_reference(
            {"key": "BOOK123", "type_id": 1}, "book")
        self._ref_repository.add_reference(
            {"key": "BOOK124", "type_id": 1}, "book")
        self._ref_repository.add_reference_entries(BOOK_ENTRY_DATA, 1)

    def test_get_all_reference_type_from_database(self):
        types_in_database = self._ref_repository.get_ref_type_names()
        ref_types = ['book', 'article', 'misc', 'phdthesis', 'incollection']
        self.assertListEqual(types_in_database, ref_types)

    def test_get_all_references_from_database(self):
        references = self._ref_repository.get_all_references()

        self.assertEqual(references[0]["ref_key"], "BOOK123")
        self.assertEqual(references[1]["ref_key"], "BOOK124")

    def test_get_reference_with_key_from_database(self):
        reference = self._ref_repository.get_reference_with_key("BOOK123")

        self.assertEqual(reference["ref_key"], "BOOK123")

    def test_adding_book_reference_with_valid_data_adds_book_to_database(self):
        new_book = {
            "key": "auth2022ABBT",
            "type_id": 1
        }

        self._ref_repository.add_reference(new_book, "book")

        ref_list = self._ref_repository.get_all_references()
        self.assertEqual(len(ref_list), 3)

    def test_adding_book_entries(self):
        ref_data = {"type_id": 1, "ref_key": "BOOK124"}
        book_entries = {
            "address": "Osoite123",
            "author": "Authori",
            "edition": "1",
            "editor": "Editor123",
            "month": "January",
            "note": "This is a note",
            "number": "4",
            "publisher": "Otava",
            "series": "Series?",
            "title": "Muumit laaksossa",
            "volume": "2",
            "year": "2022",
            "author_firstname": "Authori",
            "author_lastname": "Authorinen"
        }

        self._ref_repository.add_reference_entries(
            {**ref_data, **book_entries}, 2)
        result = self._ref_repository.get_reference_entries(2)

        self.assertEqual(result["address"], "Osoite123")
        self.assertDictEqual(book_entries, result)

    def test_get_all_references_with_entries(self):
        ref_data = {"id": 1, "type_id": 1,
                    "ref_key": "BOOK123", **BOOK_ENTRY_DATA}
        ref_list = self._ref_repository.get_all_references_with_entries()

        self.assertEqual(len(ref_list), 2)
        self.assertDictEqual(ref_data, ref_list[0])

    def test_deleting_reference_removes_reference_info_from_latex_references_table(self):
        ref_info = {
            "key": "auth1973",
            "type_id": 1,
        }

        self._ref_repository.add_reference(ref_info, "book")

        self._ref_repository.delete_reference("auth1973")
        result = self._ref_repository.get_all_references()

        self.assertEqual(len(result), 2)
        for stored_ref in result:
            self.assertNotEqual(stored_ref["ref_key"], "auth1973")

    def test_deleting_reference_removes_all_related_data_from_reference_entries_table(self):
        ref_info = {
            "key": "auth1973",
            "type_id": 1,
        }

        ref_id = self._ref_repository.add_reference(ref_info, "book")

        ref_data = {"type_id": 1, "ref_key": "auth1973"}
        book_entries = {
            "address": "Book Lane 1",
            "author": "Annie Author",
            "edition": "1",
            "editor": "Eddie Editor",
            "month": "January",
            "note": "This is a note",
            "number": "4",
            "publisher": "Publisher Publishing Ltd",
            "series": "Series?",
            "title": "The Best Book Ever",
            "volume": "2",
            "year": "1979",
            "author_firstname": "Annie",
            "author_lastname": "Author"
        }

        self._ref_repository.add_reference_entries(
            {**ref_data, **book_entries},
            ref_id
        )

        self._ref_repository.delete_reference("auth1973")
        result = self._ref_repository.get_reference_entries(ref_id)

        self.assertEqual(result, {})

    def test_check_for_existing_cite_key_returns_cite_key_if_key_exists(self):
        returned_key = self._ref_repository.check_ref_key_exists("BOOK123")
        self.assertEqual(returned_key, "BOOK123")

    def test_check_for_existing_cite_key_returns_None_if_key_does_not_exist(self):
        returned_key = self._ref_repository.check_ref_key_exists("foobar")
        self.assertIsNone(returned_key)
    
    def test_get_ref_type_id_by_name_returns_None_if_no_such_ref_type(self):
        returned_id = self._ref_repository.get_id_of_reference_type_by_name("foo")
        self.assertIsNone(returned_id)

    def test_get_field_types_by_type_name_book_returns_correct_fields(self):
        field_list = self._ref_repository.get_field_types_by_name("book")

        correct_fields = [
            {"type_name": "author", "required": 1},
            {"type_name": "editor", "required": 1},
            {"type_name": "publisher", "required": 1},
            {"type_name": "title", "required": 1},
            {"type_name": "year", "required": 1},
            {"type_name": "author_firstname", "required": 1},
            {"type_name": "author_lastname", "required": 1},
            {"type_name": "address", "required": 0},
            {"type_name": "edition", "required": 0},
            {"type_name": "month", "required": 0},
            {"type_name": "note", "required": 0},
            {"type_name": "number", "required": 0},
            {"type_name": "series", "required": 0},
            {"type_name": "volume", "required": 0}
        ]

        for i in range(0, len(correct_fields)):
            self.assertEqual(field_list[i], correct_fields[i])
