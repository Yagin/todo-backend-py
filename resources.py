from typing import List
import os, json

def print_with_indent(value, indent=0):
    indents = "\t" * indent
    print(f"{indents}{value}")

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        return {
            "title": self.title,
            "entries": [entry.json() for entry in self.entries]
        }

    @classmethod
    def from_json(cls, grocery_list: dict):
        new_entry = cls(grocery_list["title"])
        for sub_entry in grocery_list.get('entries', []):
            new_entry.add_entry(cls.from_json(sub_entry))
        return new_entry

    def save(self, path):
        with open(os.path.join(path, f"{self.title}.json"), 'w', encoding='utf-8') as file:
            json.dump(self.json(), file)  # file.wite(json())

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return cls.from_json(json.load(file))



class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = list()

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file in os.listdir(self.data_path):
            if file.endswith('json'):
                self.entries.append(Entry.load(os.path.join(self.data_path, file)))

    def add_entry(self, title: str):
        self.entries.append(Entry(title))

if __name__ == '__main__':
    category = Entry('Еда')
    category.add_entry(Entry('Морковь'))
    category.add_entry(Entry('Капуста'))
    # category.save('/tmp/')
    # print(category.json())
    # print(Entry.from_json(category.json()))