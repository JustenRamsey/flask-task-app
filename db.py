import sqlite3 
import click
import os
from flask import Flask, request, g, render_template, redirect, url_for
from flask import current_app
 #correct typo. Its actually os.path.dirname 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'mydatabase.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@click.command('init-db')
def init_db_command():
    """"Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



#initialize the database (run this once)
#init_db()



