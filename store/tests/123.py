def test_example_postgres(postgresql):

    """Check main postgresql fixture."""
    cur = postgresql.cursor()
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    postgresql.commit()
    cur.close()