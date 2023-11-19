"""
Project 5: Deque
CSE 331 FS23
Authored by Gabriel Sotelo
starter.py
"""

import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE (and `plot_speed`) if you don't want matplotlib
#from matplotlib import pyplot as plt

T = TypeVar('T')
CDLLNode = type('CDLLNode')

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque, which is the number of items currently in it.

        Time Complexity:
            O(1) - Constant time, as it directly returns the size attribute.

        Space Complexity:
            O(1) - Constant space, as no additional space is used.

        Returns:
            int: The number of items in the circular deque.
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Checks if the circular deque is empty.

        Time Complexity:
            O(1) - Constant time, as it directly compares the size attribute to 0.

        Space Complexity:
            O(1) - Constant space, as no additional space is used.

        Returns:
            bool: True if the circular deque is empty, False otherwise.
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        Retrieves the first element in the circular deque.

        Time Complexity:
            O(1) - Constant time, as it directly accesses the element at the front index.

        Space Complexity:
            O(1) - Constant space, as no additional space is used.

        Returns:
            T: The first element in the circular deque, or None if the deque is empty.
        """
        if self.size > 0:
            return self.queue[self.front]
        return None

    def back_element(self) -> T:
        """
        Retrieves the last element in the circular deque.

        Time Complexity:
            O(1) - Constant time, as it directly accesses the element at the back index.

        Space Complexity:
            O(1) - Constant space, as no additional space is used.

        Returns:
            T: The last element in the circular deque, or None if the deque is empty.
        """
        if self.size > 0:
            return self.queue[self.back]
        return None

    def grow(self) -> None:
        """
        Doubles the capacity of the circular deque by creating a new underlying Python list with double the capacity of
        the old one, and copies the values over. The new list will be 'unrolled' such that the front element is at index
        0 and the back element is at index size - 1.

        Time Complexity:
            O(n) - Linear time, as it needs to copy each element from the old list to the new one.

        Space Complexity:
            O(n) - Linear space, as it creates a new list with double the capacity of the old one.

        Returns:
            None
        """
        # Create a new list of double capacity
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity

        # Copy the elements in an "unrolled" fashion
        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]

        # Update the attributes
        self.queue = new_queue
        self.front = 0
        self.back = self.size - 1  # -1 because it's 0-indexed
        self.capacity = new_capacity

    def shrink(self) -> None:
        """
        Reduces the capacity of the circular deque by half, unless doing so would result in a capacity less than or
        equal to 4. The new list will be 'unrolled' such that the front element is at index 0 and the back element is at
        index size - 1.

        Time Complexity:
            O(n) - Linear time, as it needs to copy each element from the old list to the new one.

        Space Complexity:
            O(n) - Linear space, as it creates a new list with half the capacity of the old one.

        Returns:
            None
        """
        new_capacity = self.capacity // 2
        if new_capacity < 4:
            return

        new_queue = [None] * new_capacity

        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]

        self.queue = new_queue
        self.front = 0
        self.back = self.size - 1
        self.capacity = new_capacity

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Adds a value to either the front or back of the circular deque.

        Args:
            value (T): The value to be added to the deque.
            front (bool): If True, adds the value to the front of the deque; if False, adds it to the back.

        Time Complexity:
            O(1)* - Amortized constant time, as it sometimes needs to call the grow method which is O(n).

        Space Complexity:
            O(1)* - Amortized constant space, as it sometimes needs to allocate new space in the grow method.

        Returns:
            None
        """

        if self.size == 0:  # Enqueuing to an empty deque
            self.front = 0
            self.back = 0
            self.queue[self.front] = value
        elif front:
            self.front = (self.front - 1) % self.capacity
            self.queue[self.front] = value
        else:
            self.back = (self.back + 1) % self.capacity
            self.queue[self.back] = value

        self.size += 1
        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Removes and returns an item from either the front or the back of the circular deque.

        Args:
            front (bool): If True, removes the item from the front of the deque; if False, removes it from the back.

        Time Complexity:
            O(1)* - Amortized constant time, as it sometimes needs to call the shrink method which is O(n).

        Space Complexity:
            O(1) - Constant space, as it does not allocate additional space.

        Returns:
            T: The item removed from the circular deque, or None if the deque was empty.
        """
        # If the deque is empty
        if self.size == 0:
            return None

        # Determine which value to dequeue and adjust the appropriate pointer
        if front:
            removed_value = self.queue[self.front]
            self.front = (self.front + 1) % self.capacity
        else:
            removed_value = self.queue[self.back]
            self.back = (self.back - 1) % self.capacity

        # Decrement the size
        self.size -= 1

        # Check if we need to shrink the underlying list
        if self.size <= (self.capacity // 4) and (self.capacity // 2) >= 4:
            self.shrink()

        return removed_value

class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def insert(self, val: T, front: bool = True) -> None:
        """
        Inserts a new node with the given value into the circular doubly linked list (CDLL).

        Args:
            val (T): The value to be inserted into the CDLL.
            front (bool, optional): A flag that indicates whether to insert the node at the front (True) or back (False)
            of the CDLL. Defaults to True.

        The new node is inserted at the front of the CDLL if 'front' is True, and at the back if 'front' is False.
        If the CDLL is empty, the new node will be the only node in the CDLL and its next and prev pointers will point
        to itself, maintaining the circular property of the CDLL.

        Time Complexity:
            O(1) - Constant time, as it performs a fixed number of operations regardless of the size of the CDLL.

        Space Complexity:
            O(1) - Constant space, as it only creates one new node and does not use any additional space that grows with
            the input.

        Returns:
            None
        """
        new_node = CDLLNode(val)

        if not self.head:
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
        else:
            if front:
                new_node.next = self.head
                new_node.prev = self.head.prev
                self.head.prev.next = new_node
                self.head.prev = new_node
                self.head = new_node
            else:
                new_node.next = self.head
                new_node.prev = self.head.prev
                self.head.prev.next = new_node
                self.head.prev = new_node

        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        Removes a node from the circular doubly linked list (CDLL).

        Args:
            front (bool, optional): A flag that indicates whether to remove the node from the front (True) or back
            (False) of the CDLL. Defaults to True.

        The node is removed from the front of the CDLL if 'front' is True, and from the back if 'front' is False.
        If the CDLL is empty, the method does nothing.
        If the CDLL has only one node, removing it will set the head to None.

        Time Complexity:
            O(1) - Constant time, as it performs a fixed number of operations regardless of the size of the CDLL.

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            None
        """
        if not self.head:
            return

        if self.size == 1:
            self.head = None
        else:
            if front:
                self.head.prev.next = self.head.next
                self.head.next.prev = self.head.prev
                self.head = self.head.next
            else:
                self.head.prev.prev.next = self.head
                self.head.prev = self.head.prev.prev

        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#
    def __len__(self) -> int:
        """
        Returns the length/size of the CDLLCD, and hence the underlying CDLL.

        This method enables the use of the len() function on an instance of the CDLLCD class.

        Time Complexity:
            O(1) - Constant time, as it directly returns the size attribute of the CDLL instance.

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            int: The number of elements in the CDLLCD.
        """
        return self.CDLL.size

    def is_empty(self) -> bool:
        """
        Checks if the CDLLCD is empty.

        Time Complexity:
            O(1) - Constant time, as it directly checks the size attribute of the CDLL instance.

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            bool: True if the CDLLCD is empty, False otherwise.
        """
        return self.CDLL.size == 0

    def front_element(self) -> T:
        """
        Retrieves the first element in the CDLLCD.

        Time Complexity:
            O(1) - Constant time, as it directly accesses the head of the CDLL instance.

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            T: The first element of the CDLLCD, if it exists. Otherwise, None.
        """
        if self.CDLL.head:
            return self.CDLL.head.val
        else:
            return None

    def back_element(self) -> T:
        """
        Retrieves the last element in the CDLLCD.

        Time Complexity:
            O(1) - Constant time, as it directly accesses the previous node of the head of the CDLL instance.

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            T: The last element of the CDLLCD, if it exists. Otherwise, None.
        """
        if self.CDLL.head:
            return self.CDLL.head.prev.val 
        else:
            return None

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a value to the CDLLCD.

        Args:
            val (T): The value to be added to the CDLLCD.
            front (bool, optional): Indicates whether to add the value to the front (True) or back (False) of the
            CDLLCD. Defaults to True.

        This method utilizes the insert function of the CDLL class to add the value.

        Time Complexity:
            O(1) - Constant time, as the insert function of the CDLL class has a time complexity of O(1).

        Space Complexity:
            O(1) - Constant space, as the insert function of the CDLL class has a space complexity of O(1).

        Returns:
            None
        """
        self.CDLL.insert(val, front)

    def dequeue(self, front: bool = True) -> T:
        """
        Removes and returns a value from the CDLLCD.

        Args:
            front (bool, optional): Indicates whether to remove the value from the front (True) or back (False) of the
            CDLLCD. Defaults to True.

        This method utilizes the remove function of the CDLL class to remove the value.

        Time Complexity:
            O(1) - Constant time, as both the front_element, back_element and remove functions of the CDLL class have a
            time complexity of O(1).

        Space Complexity:
            O(1) - Constant space, as it does not use any additional space that grows with the input.

        Returns:
            T: The value removed from the CDLLCD, if it is not empty. Otherwise, None.
        """
        if self.is_empty():
            return None
        val = self.front_element() if front else self.back_element()
        self.CDLL.remove(front)
        return val


def plot_speed():
    """
    Compares performance of the CDLLCD and the standard array based deque
    """

    # First we'll test sequences of basic operations

    sizes = [100*i for i in range(0, 200, 5)]

    # (1) Grow large
    grow_avgs_array = []
    grow_avgs_CDLL = []

    for size in sizes:
        grow_avgs_array.append(0)
        grow_avgs_CDLL.append(0)
        data = list(range(size))
        for trial in range(3):

            gc.collect()  # What happens if you remove this? Hint: memory fragmention
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            grow_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            grow_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, grow_avgs_array, color='blue', label='Array')
    plt.plot(sizes, grow_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue and Grow")
    plt.legend(loc='best')
    plt.show()

    # (2) Grow Large then Shrink to zero

    shrink_avgs_array = []
    shrink_avgs_CDLL = []

    for size in sizes:
        shrink_avgs_array.append(0)
        shrink_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            for item in data:
                cd_array.dequeue(not item % 2)
            shrink_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            for item in data:
                cd_DLL.dequeue(not item % 2)
            shrink_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, shrink_avgs_array, color='blue', label='Array')
    plt.plot(sizes, shrink_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue, Grow, Dequeue, Shrink")
    plt.legend(loc='best')
    plt.show()

    # (3) Test with random operations

    random_avgs_array = []
    random_avgs_CDLL = []

    for size in sizes:
        random_avgs_array.append(0)
        random_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            shuffle(data)

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_array.enqueue(item, item % 2)
                else:
                    cd_array.dequeue(item % 2)
            random_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_DLL.enqueue(item, item % 2)
                else:
                    cd_DLL.dequeue(item % 2)
            random_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, random_avgs_array, color='blue', label='Array')
    plt.plot(sizes, random_avgs_CDLL, color='red', label='CDLL')
    plt.title("Operations in Random Order")
    plt.legend(loc='best')
    plt.show()

    def max_len_subarray(data, bound, structure):
        """
        returns the length of the largest subarray of `data` with sum less or eq to than `bound`
        :param data: list of integers to operate on
        :param bound: largest allowable sum
        :param structure: either a CircularDeque or a CDLLCD
        :return: the length
        """
        index, max_len, subarray_sum = 0, 0, 0
        while index < len(data):

            while subarray_sum <= bound and index < len(data):
                structure.enqueue(data[index])
                subarray_sum += data[index]
                index += 1
            max_len = max(max_len, subarray_sum)

            while subarray_sum > bound:
                subarray_sum -= structure.dequeue(False)

        return max_len

    # (4) A common application

    application_avgs_array = []
    application_avgs_CDLL = []

    data = [randint(0, 1) for i in range(5000)]
    window_lengths = list(range(0, 200, 5))

    for length in window_lengths:
        application_avgs_array.append(0)
        application_avgs_CDLL.append(0)

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            start = default_timer()
            max_len_subarray(data, length, cd_array)
            application_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            max_len_subarray(data, length, cd_DLL)
            application_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(window_lengths, application_avgs_array,
             color='blue', label='Array')
    plt.plot(window_lengths, application_avgs_CDLL, color='red', label='CDLL')
    plt.title("Sliding Window Application")
    plt.legend(loc='best')
    plt.show()
