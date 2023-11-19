<!DOCTYPE html>
<html>
<head>
    <title>Circular-Double-Ended-Queues</title>
</head>
<body>

    <h1>Circular Deque Project</h1>
    <p>Author: Gabriel Sotelo</p>
    <p>CSE 331 FS23</p>

    <h2>Overview</h2>
    <p>This project involves the implementation and analysis of a Circular Deque using two different data structures: a Circular Doubly Linked List (CDLL) and an array-based implementation. It aims to demonstrate the efficiency and practicality of these structures in performing deque operations.</p>

    <h2>Features</h2>
    <ul>
        <li>Implementation of a Circular Deque using an array</li>
        <li>Implementation of a Circular Deque using a CDLL</li>
        <li>Support for basic operations such as enqueue, dequeue, and size queries</li>
        <li>Capacity management with grow and shrink functionalities</li>
        <li>Performance comparison between CDLL and array-based implementations</li>
    </ul>

    <h2>Installation</h2>
    <p>To run this project, clone the repository and ensure you have a Python interpreter installed. No additional dependencies are required.</p>

    <h2>Usage</h2>
    <p>Instantiate a Circular Deque object and use its methods to perform various operations. Example:</p>
    <pre>
        cdll_deque = CDLLCD()
        cdll_deque.enqueue(10)
        cdll_deque.enqueue(20, False)
        print(cdll_deque.dequeue())
    </pre>

    <h2>Contributing</h2>
    <p>Contributions to this project are welcome. Please fork the repository and submit a pull request for review.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License - see the LICENSE file for details.</p>

</body>
</html>
