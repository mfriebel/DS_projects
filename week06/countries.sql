DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    country VARCHAR(50),    --characters up to lenght given in ()
    population INTEGER,    -- 4 byte interger
    fertility REAL,     -- like a float
    continent VARCHAR(20)
);

-- INSERT INTO  countries(country, population, fertility, continent)
-- VALUES ('Bangladesh', 160995642, 2.12, 'Asia');

COPY countries(country, population, fertility, continent)
FROM '/Users/marf/Downloads/large_countries_2015.csv'
DELIMITER ','
CSV HEADER;