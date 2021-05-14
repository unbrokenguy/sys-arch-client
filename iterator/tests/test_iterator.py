import pytest

from iterator.collection import AnyCollection


@pytest.fixture
def collection():
    collection = AnyCollection()
    collection.append("String")
    collection.append(1)
    collection.append(None)
    return collection


def test_append_success():
    collection = AnyCollection()
    collection.append("String")
    collection.append(1)
    collection.append(None)
    assert len(collection.collection) == 3


def test_iterator(collection):
    li = [x for x in collection]
    assert len(li) == 3
    assert li[0] == "String"


def test_get_iterator_and_next(collection):
    iterator = collection.get_iterator()
    assert iterator.__class__.__name__ == "AnyIterator"
    assert iterator.next() == "String"


def test_get_reverse_iterator(collection):
    iterator = collection.get_iterator(direct_order=False)
    assert iterator.__class__.__name__ == "AnyIterator"
    assert iterator.next() is None
