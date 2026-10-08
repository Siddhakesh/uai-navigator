"""
CampusNav JSON Database Adapter
A MongoDB-compatible interface backed by JSON files.
Allows the same API code to work without a MongoDB installation.
Automatically migrates to real MongoDB when MONGO_URI is configured.
"""
import json
import os
import uuid
from pathlib import Path
from datetime import datetime


class JsonCollection:
    """Mimics PyMongo Collection API using a JSON file as storage."""

    def __init__(self, db_path: Path, collection_name: str):
        self.file = db_path / f"{collection_name}.json"
        self._ensure_file()

    def _ensure_file(self):
        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")

    def _load(self):
        try:
            return json.loads(self.file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, data):
        self.file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _match(self, doc, query):
        """Simple query matching (supports $or, $regex, $elemMatch)."""
        for key, value in query.items():
            if key == "$or":
                if not any(self._match(doc, sub_q) for sub_q in value):
                    return False
            elif key == "$and":
                if not all(self._match(doc, sub_q) for sub_q in value):
                    return False
            elif isinstance(value, dict):
                doc_val = doc.get(key)
                for op, op_val in value.items():
                    if op == "$regex":
                        import re
                        pattern = op_val if not isinstance(op_val, str) else re.compile(op_val, re.IGNORECASE)
                        if doc_val is None or not re.search(pattern, str(doc_val)):
                            return False
                    elif op == "$elemMatch":
                        if not isinstance(doc_val, list):
                            return False
                        matched = False
                        for elem in doc_val:
                            if self._match({"_val": elem}, {"_val": op_val}):
                                matched = True
                                break
                        if not matched:
                            return False
                    elif op == "$ne":
                        if doc_val == op_val:
                            return False
                    elif op == "$in":
                        if doc_val not in op_val:
                            return False
                    elif op == "$gt":
                        if not (doc_val > op_val):
                            return False
                    elif op == "$gte":
                        if not (doc_val >= op_val):
                            return False
                    elif op == "$lt":
                        if not (doc_val < op_val):
                            return False
                    elif op == "$lte":
                        if not (doc_val <= op_val):
                            return False
            else:
                if doc.get(key) != value:
                    return False
        return True

    def find(self, query=None, projection=None):
        data = self._load()
        if query:
            data = [doc for doc in data if self._match(doc, query)]
        return JsonCursor(data)

    def find_one(self, query=None):
        data = self._load()
        if query:
            for doc in data:
                if self._match(doc, query):
                    return doc
            return None
        return data[0] if data else None

    def insert_one(self, document):
        data = self._load()
        doc = dict(document)
        doc["_id"] = str(uuid.uuid4())
        data.append(doc)
        self._save(data)
        return InsertOneResult(doc["_id"])

    def insert_many(self, documents):
        data = self._load()
        ids = []
        for document in documents:
            doc = dict(document)
            doc["_id"] = str(uuid.uuid4())
            ids.append(doc["_id"])
            data.append(doc)
        self._save(data)
        return InsertManyResult(ids)

    def update_one(self, query, update):
        data = self._load()
        matched = 0
        for i, doc in enumerate(data):
            if self._match(doc, query):
                matched += 1
                if "$set" in update:
                    data[i].update(update["$set"])
                break
        self._save(data)
        return UpdateResult(matched)

    def update_many(self, query, update):
        data = self._load()
        matched = 0
        for i, doc in enumerate(data):
            if self._match(doc, query):
                matched += 1
                if "$set" in update:
                    data[i].update(update["$set"])
        self._save(data)
        return UpdateResult(matched)

    def delete_one(self, query):
        data = self._load()
        for i, doc in enumerate(data):
            if self._match(doc, query):
                data.pop(i)
                self._save(data)
                return DeleteResult(1)
        return DeleteResult(0)

    def delete_many(self, query):
        data = self._load()
        original_len = len(data)
        data = [doc for doc in data if not self._match(doc, query)]
        self._save(data)
        return DeleteResult(original_len - len(data))

    def count_documents(self, query=None):
        data = self._load()
        if query:
            return sum(1 for doc in data if self._match(doc, query))
        return len(data)

    def distinct(self, field, query=None):
        data = self._load()
        if query:
            data = [doc for doc in data if self._match(doc, query)]
        values = set()
        for doc in data:
            val = doc.get(field)
            if val is not None:
                if isinstance(val, list):
                    values.update(val)
                else:
                    values.add(val)
        return list(values)

    def drop(self):
        self._save([])

    def create_index(self, *args, **kwargs):
        pass  # No-op for JSON storage


class JsonCursor:
    """Mimics PyMongo Cursor."""

    def __init__(self, data):
        self._data = data
        self._limit_val = None
        self._skip_val = 0
        self._sort_val = None

    def limit(self, n):
        self._limit_val = n
        return self

    def skip(self, n):
        self._skip_val = n
        return self

    def sort(self, key, direction=1):
        self._sort_val = (key, direction)
        return self

    def __iter__(self):
        data = self._data[self._skip_val:]
        if self._sort_val:
            key, direction = self._sort_val
            data = sorted(data, key=lambda d: d.get(key, ""), reverse=(direction == -1))
        if self._limit_val is not None:
            data = data[:self._limit_val]
        return iter(data)

    def __len__(self):
        return len(list(self.__iter__()))


class InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class InsertManyResult:
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids


class UpdateResult:
    def __init__(self, matched_count):
        self.matched_count = matched_count
        self.modified_count = matched_count


class DeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class JsonDatabase:
    """Mimics PyMongo Database."""

    def __init__(self, db_path: Path):
        self._db_path = db_path
        db_path.mkdir(parents=True, exist_ok=True)
        self._collections = {}

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            self._collections[name] = JsonCollection(self._db_path, name)
        return self._collections[name]

    def __getitem__(self, name):
        return self.__getattr__(name)


class JsonDBAdapter:
    """Top-level adapter that provides a .db attribute like PyMongo's flask_pymongo."""

    def __init__(self):
        self.db = None

    def init_app(self, app):
        db_path = Path(app.config.get("JSON_DB_PATH", "./campusnav_data"))
        self.db = JsonDatabase(db_path)
