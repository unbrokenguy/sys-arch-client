from ArrayList import ArrayList
from ArrayListIterator import ArrayListIterator


if __name__ == "__main__":
    array_list = ArrayList()
    array_list.add(1)
    array_list.add(2)
    array_list.add(3)
    array_list.add(4)
    array_list.add(5)
    array_list_iterator = array_list.iterator()
    while array_list_iterator.has_next():
        print(array_list_iterator.next())
