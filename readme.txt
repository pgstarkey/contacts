Contacts project
----------------

Issues & work still to be completed (timed out):

- Testing so far has been with Advanced REST Client, unit tests for contacts.py still to be written
- Defensive coding in contacts.py, e.g. handling exceptions that may be thrown from database if for
example a PUT request is submitted for an existing resource.
- Problems with integration of Flask and Celery when trying to run the two Celery tasks.  Getting a
"key not found" exception on SQLALCHEMY_TRACK_MODIFICATIONS, no time to diagnose this, not obviously
related to the application code.  Celery task that uses the requests library seems to cause serialisation
exceptions to be thrown in Celery, the task works fine when called directly rather than via Celery.
- Maybe combine the two Celery tasks into a single task?

Other notes:

- Celery & Redis installed on Windows, Redis using the version downloaded from the Microsoft archive
- To run Celery worker tasks, it is necessary to use the -P eventlet switch
- SQLite database was created by running db.create_all() as a one-off in interactive mode
