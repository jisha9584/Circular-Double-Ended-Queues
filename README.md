<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1>Project 5: Circular Deque Implementation</h1>

<p>This project includes the design and implementation of a Circular Deque, utilizing two different data structures: a Circular Doubly Linked List (CDLL) and an array. The primary operations of the Deque such as insertion, deletion, and dynamic resizing (grow/shrink) are implemented and analyzed for performance efficiency.</p>

<h2>Features</h2>
<ul>
    <li>Custom Circular Deque class with enqueue and dequeue functionalities.</li>
    <li>Performance comparison between array-based and linked list-based Deque.</li>
    <li>Efficient memory management with dynamic resizing methods.</li>
    <li>Utility functions for retrieving Deque size and checking if it's empty.</li>
</ul>

<h2>Usage</h2>
<p>Instantiate the CircularDeque class and use its methods to perform Deque operations. Here's an example:</p>
<pre>
<code>
CircularDeque deque = new CircularDeque();
deque.enqueue(1);
deque.enqueue(2, false);
int frontItem = deque.front_element();
int backItem = deque.back_element();
deque.dequeue();
deque.dequeue(true);
</code>
</pre>


</body>
</html>
