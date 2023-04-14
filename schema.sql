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

-- CREATE MATERIALS TABLE
-- Joined table for managing course-->material relations
CREATE TABLE materials (
  course_id UUID NOT NULL REFERENCES courses(id),
  name VARCHAR(25) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE PARTICIPANTS TABLE
-- Joined table for managing user-->course relations
CREATE TABLE participants (
  user_id UUID NOT NULL REFERENCES users(id),
  course_id UUID NOT NULL REFERENCES courses(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE COMPLETION TYPES
CREATE TYPE grade_type AS ENUM ('L', 'E', 'M', 'C', 'B', 'A');

-- CREATE COMPLETIONS TABLE
-- Joined table for managing user-->course completion relations
CREATE TABLE completions (
  user_id UUID NOT NULL REFERENCES users(id),
  course_id UUID NOT NULL REFERENCES courses(id),
  grade grade_type,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE EXERCISE QUESTIONS TABLE
CREATE TABLE exercise_questions (
  id UUID NOT NULL PRIMARY KEY,
  course_id UUID NOT NULL REFERENCES courses(id),
  question TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE EXERCISE ANSWERS TABLE
CREATE TABLE exercise_answers (
  question_id UUID NOT NULL REFERENCES exercise_questions(id),
  answer TEXT NOT NULL,
  correct BOOLEAN NOT NULL,
);

-- INSERT TEST USER
INSERT INTO users (id, name, email, type, password_hash) VALUES (gen_random_uuid(), 'Teppo Testaaja', 'testi@leevihal.me', 'STUDENT', 'pbkdf2:sha256:260000$Wj1Grv19zhSiZBO8$e936e501611b73a1fff0e12d2b3910b251654e90f44e33320749be14319f63ac');

-- INSERT TEST COURSE
INSERT INTO courses (id, name, short_description, description, invitation_code, is_hidden) VALUES (gen_random_uuid(), 'Esimerkkikurssi #1', 'Tämä kurssi on luotu sovelluksen testaamiseen.', 'Tämä on kurssin kuvaus. Voit kirjoittaa tähän kuvauksen kurssista.', 'abcdefg1234567', false);