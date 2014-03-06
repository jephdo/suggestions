Suggestions
============

We've referred to things as objects, items or entities. I currently call them 
"documents" and each document can have associated "tags" which is a key-value pair.

For example the document "jetta" may have tags such as `{"year": "2013"}` or `{"vehicle type": "car"}`.

Go to `/documents/1/tags/` for a list of all currently associated tags with the 
document with ID number 1. The tags are sorted by their most "relevant" tag.


Setup
======
To get started quickly, run the following commands in shell:

```bash
git clone https://github.com/jephdo/suggestions.git
cd suggestions
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
python manage.py
```

The application can run Python2 or Python3. The two packages required are pyramid and SQLAlchemy. 
The script `manage.py` will generate a sqlite database in the top level folder and then begin
to serve the app at `localhost:8080`.


The Sample Database
=================
I used a sample CSV database of cars (approximately 4300 rows at 1.6mb) and generate
a sqlite database.

In the CSV, each row is a car and each row has maybe twenty columns. When inserting
each row into the database, it randomly chooses what columns to add as tags.

Therefor, not every car in the sqlite database has the same tags and the data
is sparse as in real usage.