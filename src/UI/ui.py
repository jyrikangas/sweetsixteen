import os
from services.reference_service import ReferenceService
from services.parser import print_in_bibtex_format, write_bibtex_file


class UI:

    def __init__(self):
        self.ref_service = ReferenceService()
        self.ui_library = UIData()
        self.reference_types = self.ref_service.get_reference_type_names()
        self.commands = {
            "1": self.print_type_names,
            "2": self.add_reference,
            "3": self.print_reference_list,
            "4": print_in_bibtex_format,
            "5": self.delete_reference,
            "6": self.save_refs_to_bibtex_file
        }

    def print_menu(self):
        print("\n(1) Get available reference types")
        print("(2) Add reference")
        print("(3) Show all references in database")
        print("(4) Show references in bibtex format")
        print("(5) Delete reference from database")
        print("(6) Save references as bibtex file\n")
        print("(Other) End program\n")

    def print_type_names(self):
        ref_types = self.ref_service.get_reference_type_names()
        for r_type in ref_types:
            print(r_type)

    def add_reference(self):
        key = ''
        while key not in self.reference_types:
            key = input(
                f"Which reference type {'/'.join(self.reference_types)} ?: "
            )
        ref_dict = self.ref_query(key)
        self.ref_service.add_reference(ref_dict, key)

    def print_reference_list(self):
        all_references = self.ref_service.get_all_references()
        print("\n*** References in database ***")
        for reference in all_references:
            for key, value in reference.items():
                print(f"{key}: {value}")
            print("---")

    def delete_reference(self):
        ref_key = input("Enter citation key of reference to delete: ")
        if self.ref_service.check_reference_key_exists(ref_key):
            self.ref_service.delete_reference(ref_key)
            print("Reference was deleted from database.")
        else:
            print("No reference with such citation key.")

    def save_refs_to_bibtex_file(self):
        write_bibtex_file()
        print("The file 'bibtex.bib' was saved to the bibtex_files folder")

    def query(self):

        while True:
            os.system('clear')
            self.print_menu()
            cmd = input("Command: ")

            if cmd not in self.commands.keys():
                break

            self.commands[cmd]()
            next_input()

    def fields(self, type_name):
        fields = self.ref_service.get_fields_by_type_name(type_name)
        return fields

    def discard_author_or_editor(self):
        selection = ""
        while selection == "":
            selection = input(
                "Press 1 if your reference has an author and 2 if an editor: ")
        if selection == "1":
            return "editor"
        return "author"

    def input_valid(self, field, answer):
        rules = {
            "year": lambda x: x.isnumeric()
        }
        if field in rules.keys():
            return rules[field](answer)
        return True

    def query_entries(self, fields):
        ref_dict = {}
        optionality = ["(optional): ", "(required): "]
        for field, req in fields.items():
            answer = ""
            while True:
                answer = input(
                    self.ui_library.questions_dict[field] + f'{optionality[req]}')
                is_valid = self.input_valid(field, answer)
                if is_valid and answer != "":
                    break
                elif is_valid and req != 1:
                    break
            if answer != "":
                ref_dict[field] = answer

        return ref_dict

    def ref_query(self, type_name):
        fields = self.fields(type_name)
        if set(["author", "editor"]).issubset(fields.keys()):
            filtered_key = self.discard_author_or_editor()
            fields.pop(filtered_key)
        fields["key"] = 1
        return self.query_entries(fields)


class UIData:
    def __init__(self) -> None:
        self.questions_dict = {
            'key': 'Citation key ',
            'author': 'Author ',
            'author_firstname': 'First name ',
            'author_lastname': 'Last name',
            'editor': 'Editor ',
            'title': 'Title ',
            'publisher': 'Publisher ',
            'year': 'Year ',
            'journal': 'Journal ',
            'volume': 'Volume ',
            'series': 'Series ',
            'address': 'Address ',
            'edition': 'Edition ',
            'month': 'Month ',
            'chapter': 'Chapter ',
            'note': 'Note ',
            'number': 'Number ',
            'type': 'Type ',
            'school': 'School ',
            'booktitle': "Book title ",
            'howpublished': 'How published ',
            'pages': 'Pages '
        }

        '''if key=="book":
            keys=['key',
            'author',
            'editor',
            'title',
            'publisher',
            'year',
            'volume',
            'series',
            'address',
            'edition',
            'month',
            'note']
            return keys'''


def next_input():
    print()
    input("Press enter to continue...")
