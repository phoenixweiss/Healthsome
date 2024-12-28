"""
Database Helpers for the Healthsome application.

This module provides utility functions for interacting with the SQLite database,
including executing queries, managing connections, and ensuring proper resource cleanup.
"""

import os
import sqlite3

from flask import g

DATABASE = os.getenv('DB_FILE', 'healthsome.db')

def get_db():
    """
    Get a database connection for the current application context.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=(), one=False):
    """
    Execute a SELECT query and return the results.

    Args:
        query (str): The SQL query to execute.
        args (tuple): The arguments for the query.
        one (bool): Whether to return only one result.

    Returns:
        list or sqlite3.Row: Query results as a list of rows or a single row if `one` is True.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """
    Execute an INSERT, UPDATE, or DELETE query.

    Args:
        query (str): The SQL query to execute.
        args (tuple): The arguments for the query.

    Returns:
        None
    """
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()

def close_db(e=None):
    """
    Close the database connection if it exists.

    Args:
        e (Exception, optional): An optional exception object.

    Returns:
        None
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()
