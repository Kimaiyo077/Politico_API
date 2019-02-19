import psycopg2
import os

#uri = os.getenv(['DATABASE_URI'])

test_uri = os.environ['DATABASE_URL']


def connection(url):
    con = psycopg2.connect(url)
    return con

def init_db():
    con = connection(uri)
    cur = con.cursor()
    queries = tables()

    for query in queries:
        cur.execute(query)
    con.commit()

    return con

def init_test_db():
    con = connection(test_uri)
    cur = con.cursor()
    queries = tables()

    for query in queries:
        cur.execute(query)
    con.commit()

    return con

def destroy_db():
    con = connection(test_uri)
    cur = con.cursor()

    users = """ DROP TABLE IF EXISTS users CASCADE;"""
    offices = """ DROP TABLE IF EXISTS offices CASCADE;"""
    parties = """ DROP TABLE IF EXISTS parties CASCADE;"""
    candidates = """ DROP TABLE IF EXISTS candidates CASCADE;"""
    votes = """ DROP TABLE IF EXISTS votes CASCADE;"""
    queries = [users, offices, parties, candidates, votes]

    for query in queries:
        cur.execute(query)
    con.commit()

def tables():
    users = """ CREATE TABLE IF NOT EXISTS users (
        userId SERIAL UNIQUE,
        nationalId NUMERIC NOT NULL,
        firstname VARCHAR NOT NULL,
        lastname VARCHAR NOT NULL,
        othername VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        phoneNumber VARCHAR NOT NULL,
        passportUrl TEXT NOT NULL,
        password VARCHAR NOT NULL,
        IsAdmin BOOLEAN DEFAULT False); """

    offices = """ CREATE TABLE IF NOT EXISTS offices (
        officeId SERIAL UNIQUE,
        officeType VARCHAR NOT NULL,
        officeName VARCHAR NOT NULL); """

    parties = """ CREATE TABLE IF NOT EXISTS parties (
        partyId SERIAL UNIQUE,
        partyName VARCHAR NOT NULL,
        hqAddress VARCHAR NOT NULL,
        logoUrl TEXT NOT NULL); """

    
    candidates = """ CREATE TABLE IF NOT EXISTS candidates (
        candidateId SERIAL UNIQUE,
        officeId integer REFERENCES offices (officeId) ON DELETE CASCADE,
        userId integer REFERENCES users (userId) ON DELETE CASCADE); """

    votes = """ CREATE TABLE IF NOT EXISTS votes (
        vote_id SERIAL UNIQUE,
        officeId integer REFERENCES offices (officeId) ON DELETE CASCADE,
        candidate integer REFERENCES candidates (candidateId) ON DELETE CASCADE,
        createdOn DATE DEFAULT CURRENT_TIMESTAMP,
        createdBy integer REFERENCES users (userId) ON DELETE SET NULL);"""

    queries = [users, offices, parties, candidates, votes]

    return queries