-- dumps/airline.sql
-- Схема «авиакомпания» + тестовые данные для курса db_stud
-- PostgreSQL, UTF-8.

DROP SCHEMA IF EXISTS airline CASCADE;
CREATE SCHEMA airline;
SET search_path TO airline, public;

CREATE TABLE airport (
    airport_code CHAR(3) PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    city         VARCHAR(80)  NOT NULL,
    country      VARCHAR(80)  NOT NULL
);

CREATE TABLE aircraft (
    tail_number  VARCHAR(10) PRIMARY KEY,
    model        VARCHAR(60) NOT NULL,
    seats        INT NOT NULL CHECK (seats > 0)
);

CREATE TABLE flight (
    flight_id    SERIAL PRIMARY KEY,
    flight_no    VARCHAR(10) NOT NULL,
    dep_airport  CHAR(3) NOT NULL REFERENCES airport(airport_code),
    arr_airport  CHAR(3) NOT NULL REFERENCES airport(airport_code),
    dep_time     TIMESTAMPTZ NOT NULL,
    arr_time     TIMESTAMPTZ NOT NULL,
    aircraft     VARCHAR(10) NOT NULL REFERENCES aircraft(tail_number),
    CHECK (dep_airport <> arr_airport),
    CHECK (arr_time > dep_time)
);

CREATE TABLE passenger (
    passenger_id SERIAL PRIMARY KEY,
    last_name    VARCHAR(60) NOT NULL,
    first_name   VARCHAR(60) NOT NULL,
    email        VARCHAR(120) UNIQUE,
    passport_no  VARCHAR(20) UNIQUE
);

CREATE TABLE booking (
    booking_id   SERIAL PRIMARY KEY,
    passenger_id INT NOT NULL REFERENCES passenger(passenger_id),
    flight_id    INT NOT NULL REFERENCES flight(flight_id),
    seat_no      VARCHAR(4) NOT NULL,
    booked_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status       VARCHAR(20) NOT NULL DEFAULT 'confirmed'
        CHECK (status IN ('confirmed', 'cancelled', 'checked_in')),
    UNIQUE (flight_id, seat_no)
);

INSERT INTO airport (airport_code, name, city, country) VALUES
    ('SVO', 'Шереметьево', 'Москва', 'Россия'),
    ('LED', 'Пулково', 'Санкт-Петербург', 'Россия'),
    ('AER', 'Сочи', 'Сочи', 'Россия');

INSERT INTO aircraft (tail_number, model, seats) VALUES
    ('RA-73001', 'Airbus A320', 180),
    ('RA-73002', 'Boeing 737', 160);

INSERT INTO flight (flight_no, dep_airport, arr_airport, dep_time, arr_time, aircraft) VALUES
    ('SU100', 'SVO', 'LED', '2026-09-01 08:00+03', '2026-09-01 09:30+03', 'RA-73001'),
    ('SU200', 'LED', 'AER', '2026-09-01 12:00+03', '2026-09-01 15:00+03', 'RA-73002');

INSERT INTO passenger (last_name, first_name, email, passport_no) VALUES
    ('Иванов', 'Иван', 'ivanov@example.com', '4500123456'),
    ('Петрова', 'Мария', 'petrova@example.com', '4500654321');

INSERT INTO booking (passenger_id, flight_id, seat_no) VALUES
    (1, 1, '12A'),
    (2, 1, '12B');
