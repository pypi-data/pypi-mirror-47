## Control all the things.

Still pre-alpha, this takes my work from Bibliopixel and generalizes it to control any real-time thing 
from any other.

# Random notes follow

We want to construct a hierarchical collection of Python objects from a data
file.

We will be rewriting a big Python dictionary so that we can reach all the parts
of it from the top.


# Three types of data:

* simple - strings, lists, dictionaries, booleans, `None`, numbers
* class - represents a Python class that gets constructed
* container class - a Python class that contains other class or simple data
  within it

# High-level

We have a huge dictionary.

At each level, a special member `_` has the type information - either a
typename, or the actual class.


# Details

Class data corresponds to a Python constructor.

Classes have attributes - either read-only (set in the constructor) or
read-write.

Classes have methods

A Class always has a type attribute whose name will probably be `_`.

There are potential customization points here:

These two will be classmethods:

1. pre_construction - rewrite the dictionary
2. at construction - before any child is created or public attribute is set.

-- after this step, we're an object

3. post-attribute - after all the attributes have been set
4. post-child - after all children are created
5. post-parent - after your parent has created all your siblings
6. ready - right before we're ready to start

Two different ways to construct!

1.  construct/set/init

Classes with an empty constructor, setters, and then an init() method or function

    a = Class()
    a.foo = 1
    a.bar = 'hello'
    a.init()  # or init(a)

2. Constructor-only

    a = Class(foo=1, bar='hello')


# On time and data

Look at timed MIDI - there are many ways to represent it:

1. as a packed stream of MIDI data using running status with a separate,
parallel list of time annotations indicating when things happen

2. As a straightforward list of MIDI data/absolute time pairs

3. as a list of items that are either MIDI data or absolute times or both

4., 5. are like 2. and 3. with relative times.

Suppose memory were free.  Then we'd have standalone events that had just MIDI
and absolute time.  They need nothing to be able to be played.

"Good" absolute time would handle down to a microsecond and up to years.
A year is very nearly pi * 10^7 seconds.

2 bytes for seconds is 65,536 divisions per second
3 bytes for fractional seconds gives 16,777,216 divisions per second
4 bytes is 4,294,967,296 divisions per second - gigahertz range

2 bytes of seconds is 18 hours
3 bytes of seconds is 194 days
4 bytes of seconds is 136 years

So 4 bytes is good enough for most musical time, and at that point you can go
to eight bytes.

This comes out pretty nicely as eight bytes:


TIME TIME TIME TIME :  STATUS DATA [DATA] wasted

It's a little wasteful - we waste between 1 and 2 bytes per eight - but it's
really easy to program to.

Suppose one energetic person can play 10 notes a second and sends three
controllers (breath, aftertouch, pedal) which each change ten times a second.

So that's 40 events per second or 320 bytes per second.

If you had a 16 person band playing that way all the time and you recorded all
of it for one hour, then this would total:

    320 * 64 * 60 * 60

or 18MB.

So with modern memory it just isn't that bad...
