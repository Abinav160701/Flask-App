# Flask APP
## Description
<li>This will be a flash card app which helps the user with remembering things. Basically what the
backside of the card holds.</li>
<li>We score the user depending on how well he remembers the contents of the cards.</li>
<li>This will help the user keep track of the progress he’s made over time.</li>

## Technologies used
<li>Flask- For the application code
<li>Jinja2 templates – To generate templates and substitute values when rendering
<li>Bootstrap for HTML generation and styling- For both styling. Used both inline and external
CSS.
<li>SQLite- for data storage
<li>SQL-Alchemy- links to the database with a python code
  
## DB Schema Design
There are three tables in our database. The first one is the user data. New data is stored in the table
every time a new user registers in the app. This table contains five columns- id, username, password,
date_created and score. Username has a unique key constraint and id is the primary key.
The next table in our database is deck, which has relationship with username from user table. Other
columns in this table include- id, deck_name, user, date_created, score, is_public and last_rev. user
is the foreignkey for the table from table user(username) and primary key is id.
Each card in the table-card has a relation with deck. Columns in card are- card_id, front, back, score
and deck. The deck column is a foreign key for the table referenced from table deck(deck_name).
Card_id is the primary key for this table.
The card table has a relationship with the table deck and the user table. This has a well defined
structure. We create a new user which is free of constraints. Within each user, we add decks which
are uniquely identified by a user. Within decks, we have cards which are again uniquely identified by
the deck that holds it.

## API Design
An API based on the OAS 3.0.0 was created for cards, decks and users.
<li>Cards:
  <li>Create a new card in a particular deck for a particular user
  <li>Read a cards iteratively
<li>Decks:
  <li>Create a new deck for a particular user
  <li>Read, update or delete a specific deck by clicking on the deck.
<li>Users:
  <li>Create a new user
  <li>User can only be created and the contents in it can be updated. It cannot be deleted.

## Architecture and Features
<li>Models are in /Flashcard/models.py
<li>Controllers are in /Flashcard/views.py
<li>API is in /Flashcard/api.py
<li>All the HTML templates are in /Flashcard/templates
<li>create_app() in /Flashcard/__init__.py initializes the app and the API.
<li>app.py calls create_app() then runs the complete app and API on the specified host and port.

### Users:
  <li>User login with password is implemented using just fields. Users can be created at runtime.
  <li>Username has to be unique, only a length constraint is given. Password need not be unique.
  <li>Each user has a set of associated decks and cards that they create. Decks and cards are
specific to the user that created them.

### Decks:
  <li>Each user can create multiple decks.
  <li>When a deck is deleted, all the associated cards are deleted.
  <li>Different users can have decks with the same name. But each deck associated with a
particular user must have a unique name.

### Cards:
  <li>Each deck can have multiple cards. Cards are considered duplicate in a deck only if question
and answer match with an existing card. Duplicate cards are prevented from creation.
  <li>No constraints on question and answer for a card.
  <li>Each card has a difficulty ranking associated with it: Difficult - 5 pt,Medium - 10 pts & Easy -
15 pts.
  <li>When a user takes a test on a particular card, they guess the answer in their mind and then
rank the difficulty.
 
