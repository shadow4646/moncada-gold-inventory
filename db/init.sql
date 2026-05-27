-- Moncada Gold - Schema inicial e inventario de joyas
-- Integración Continua - POLIGRAN Grupo B04

CREATE TABLE IF NOT EXISTS productos (
    id         SERIAL PRIMARY KEY,
    nombre     VARCHAR(150)   NOT NULL,
    categoria  VARCHAR(80)    NOT NULL,
    material   VARCHAR(100)   NOT NULL,
    precio     NUMERIC(10, 2) NOT NULL,
    stock      INTEGER        NOT NULL DEFAULT 0,
    created_at TIMESTAMP      NOT NULL DEFAULT NOW()
);

INSERT INTO productos (nombre, categoria, material, precio, stock) VALUES
    ('Anillo Eternidad',        'anillos',  'Oro laminado 18k',            85000.00, 12),
    ('Collar Corazón',          'collares', 'Plata 925',                   45000.00, 20),
    ('Pulsera Eslabón Dorado',  'pulseras', 'Oro laminado 18k',            65000.00,  8),
    ('Aretes Perla Gota',       'aretes',   'Plata 925',                   38000.00, 25),
    ('Cadena Figaro 50cm',      'cadenas',  'Oro laminado 18k',            95000.00, 10),
    ('Anillo Solitario Plata',  'anillos',  'Plata 925 con zirconia',      55000.00, 15),
    ('Collar Luna Creciente',   'collares', 'Oro laminado 18k',            72000.00,  6),
    ('Pulsera Charm Infinito',  'pulseras', 'Plata 925',                   42000.00, 18),
    ('Aretes Argolla Lisa',     'aretes',   'Oro laminado 18k',            48000.00, 30),
    ('Dije Moncada Logo',       'dijes',    'Oro laminado 18k bañado',     35000.00, 50);
