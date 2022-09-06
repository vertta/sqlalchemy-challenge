-- Table: public.measurements
DROP TABLE IF EXISTS public.stations;
DROP TABLE IF EXISTS public.measurements;

CREATE TABLE IF NOT EXISTS public.stations
(
    station varchar(50),
    name Varchar(100),
    latitude decimal,
    longitude decimal,
    elevation decimal,
    CONSTRAINT stations_pkey PRIMARY KEY (station)
)
TABLESPACE pg_default;
;

CREATE TABLE IF NOT EXISTS public.measurements
(
    station varchar(50),
    date date,
    prcp float,
    tobs int ,
 PRIMARY KEY(station,date),
   CONSTRAINT fk_stations
      FOREIGN KEY(station) 
	  REFERENCES stations(station)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.measurements
    OWNER to postgres;