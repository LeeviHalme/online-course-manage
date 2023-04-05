-- INIT EXTENSIONS
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- CREATE USER TYPES
CREATE TYPE user_type AS ENUM ('STUDENT', 'TEACHER');

-- CREATE USERS TABLE
CREATE TABLE users (
  id UUID NOT NULL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password_hash VARCHAR,
  type user_type,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE COURSES TABLE
CREATE TABLE courses (
  id UUID NOT NULL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  short_description VARCHAR(120) NOT NULL,
  description TEXT NOT NULL,
  invitation_code VARCHAR(15) NOT NULL,
  -- COURSE FLAGS (defaulted to private and hidden)
  is_public BOOLEAN NOT NULL DEFAULT false,
  is_hidden BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE PARTICIPANTS TABLE
-- Joined table for managing user-->course relations
CREATE TABLE participants (
  user_id UUID NOT NULL REFERENCES users(id),
  course_id UUID NOT NULL REFERENCES courses(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERT TEST USER
INSERT INTO users (id, name, email, type) VALUES (gen_random_uuid(), 'Teppo Testaaja', 'testi@leevihal.me', 'STUDENT');

-- INSERT TEST COURSE
INSERT INTO courses (id, name, short_description, description, invitation_code) VALUES (gen_random_uuid(), 'Esimerkkikurssi #1', 'Tämä kurssi on luotu sovelluksen testaamiseen.', 'Tämä on kurssin kuvaus. Voit kirjoittaa tähän kuvauksen kurssista.', 'abcdefg1234567');