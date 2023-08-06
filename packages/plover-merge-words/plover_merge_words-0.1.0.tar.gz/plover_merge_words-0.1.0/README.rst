##################
Plover Merge Words
##################

Avoid repeating yourself.

Usage
=====

Prevent the Stacking of Characters
----------------------------------

``{:merge:text}``

-  **text**: the text that shouldn't be repeated

Use Cases
^^^^^^^^^

- Merge with a prefix

  - Map your stroke to ``{:merge:word}``
  - ``{con^}continue`` → concontinue
  - ``{con^}{:merge:continue}`` → continue
  - ``{con^}{:merge:continue}{:merge:continue}`` → continue continue

- Ensure a word is always proceeded by a space

  - Map your stroke to ``{:merge: }word``
  - ``{con^}{:merge: }word`` → con word
  - ``{con^}{:merge: }word{:merge: }word`` → con word word

- Avoid repeating characters that you don't want to repeat

  - Map your stroke to ``{:merge: word}`` or ``{^}{:merge:word}``
  - ``hey{^}{:merge:.}{-|}there`` → hey. There
  - ``hey{^}{:merge:.}{-|}{^}{:merge:.}{-|}{^}{:merge:.}{-|}{^}{:merge:.}{-|}{^}{:merge:.}{-|}there`` → hey. There
