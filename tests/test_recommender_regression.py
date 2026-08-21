import sqlite3

import numpy as np


def _make_test_db():
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY, title TEXT)")
    connection.execute("INSERT INTO movies (id, title) VALUES (29, 'The Avengers')")
    connection.commit()
    return connection


def test_numpy_int64_id_must_be_cast_to_int_for_sqlite():
    """
    Regression test for a bug where movie IDs coming out of a pandas
    Series (numpy.int64) silently failed to match an INTEGER PRIMARY KEY
    column in SQLite, causing recommend_for_user() to always return an
    empty list even when valid recommendations existed.
    """
    connection = _make_test_db()
    cursor = connection.cursor()

    raw_id = np.int64(29)

    cursor.execute("SELECT id, title FROM movies WHERE id = ?", (raw_id,))
    assert cursor.fetchone() is None

    cursor.execute("SELECT id, title FROM movies WHERE id = ?", (int(raw_id),))
    assert cursor.fetchone() == (29, "The Avengers")

    connection.close()
