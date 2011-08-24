Code Standards
==============

tl;dr
~~~~~

Python:
-------
Follow python's standards (PEP8):

Line length of 79 characters seems ignored a lot, but having lines
go off the end of widescreen displays seems excessive. Perhaps 120?

Shish - In particular, have "if" and the effect on separate lines,
        so the code coverage tool can tell them apart. Otherwise,
        the coverage tool will see "I hit the if statement (the
        variable was false)" and mark the whole line as "tested"

in the src dir you can "make pep8" to have the code checked

Makefiles:
----------
Makefiles give very different meanings to tabs and spaces; as long as
the makefile has valid syntax it should be ok

HTML, JScript, CSS (Everything else):
-------------------------------------
Similar to python; 4 spaces for indentation


code comment keywords
~~~~~~~~~~~~~~~~~~~~~
Not set in stone, but consistency makes it easier to spot:

  NOTE
    an important bit of information that is key to this code but may not
    be obvious just by looking at it. Assumptions should be noted (and /
    or assert()'ed)

  TODO
    for when a developer knows what needs doing, but hasn't got around
    to it yet

  BUG
    for when a problem is known and reported and pinpointed, but can't
    be solved immediately

  undecided
    for when the code works, but really needs rewriting

  undecided
    workarounds for bugs in external libraries, this code can be removed
    once the library is updated, or we ship a custom fixed version

  undecided
    workarounds for bugs in IE, this code can be removed when IE is dead

  name
    a developer's login name followed by a dash indicates that they are
    voicing an opinion.

