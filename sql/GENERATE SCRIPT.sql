BEGIN;
truncate table "User_Role", "General", "User", "Vehicle", "Customer", "Config", "Shipment", "Pattern", "Work_statement", "Stillage_type", "Advanced_user", "Stillage", "Pattern_Item" restart identity cascade;






    CREATE OR REPLACE FUNCTION random_between_big(low BIGINT ,high BIGINT)
   RETURNS BIGINT AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$ language 'plpgsql' STRICT;
----------------
create or replace function random_timestamp() returns timestamp with time zone language sql as $$
select NOW() + (random() * (NOW()+'190 days' - NOW())) + '70 days' limit 1 $$;
-----------------------------------------------------------
create or replace function random_boolean() returns boolean language sql as $$
SELECT RANDOM()::INT::BOOLEAN limit 1 $$;
----------------------------------------------------
create or replace function random_text() returns text language sql as $$
select md5(random()::text) limit 1 $$;



CREATE OR REPLACE FUNCTION random_id_v_tabulke(_tbl text, OUT result text)
    LANGUAGE plpgsql AS
$func$
BEGIN
   EXECUTE format('SELECT "id" FROM %I ORDER BY random() LIMIT 1', _tbl)
   INTO result;
END
$func$;


create or replace function random_code() returns bigint language sql as $$
SELECT "code" FROM "User" ORDER BY random() LIMIT 1 $$;

-- General
insert into "General" ("Last_changes", "Last_available", "Automatic_export")
select	random_timestamp(),
        random_timestamp(),
		random_boolean()
from generate_series(1, 50) as seq(i);
--User_Role
--insert into "User_Role" ("name")
--select 'test'
--from generate_series(1, 100) as seq(i);
INSERT INTO "User_Role" ("name")
VALUES ('Užívateľ');

INSERT INTO "User_Role" ("name")
VALUES ('Operátor');

INSERT INTO "User_Role" ("name")
VALUES ('Administrátor');

-- User
insert into "User" ("code", "Name", "Last_name", "User_Role_id")
select	random_between_big(10001,99999),
		random_text(),
		random_text(),
		random_id_v_tabulke('User_Role')
from generate_series(1, 20) as seq(i);
-- Vehicle
INSERT INTO "Vehicle" ("SPZ")
VALUES ('BA420XX');
INSERT INTO "Vehicle" ("SPZ")
VALUES ('BA111SO');
INSERT INTO "Vehicle" ("SPZ")
VALUES ('NR223KU');
INSERT INTO "Vehicle" ("SPZ")
VALUES ('POKEMON');
-- Customer
INSERT INTO "Customer" ("Name")
VALUES ('BESTEST CORP INC.');

INSERT INTO "Customer" ("Name")
VALUES ('Zemiakove jogurty a.s.');

INSERT INTO "Customer" ("Name")
VALUES ('KOVÁČ – výroba kačičiek, s. r. o.');

-- Config
INSERT INTO "Config" ("Customer_id","Vehicle_id")
VALUES (random_id_v_tabulke('Customer'),random_id_v_tabulke('Vehicle'));
INSERT INTO "Config" ("Customer_id","Vehicle_id")
VALUES (random_id_v_tabulke('Customer'),random_id_v_tabulke('Vehicle'));
INSERT INTO "Config" ("Customer_id","Vehicle_id")
VALUES (random_id_v_tabulke('Customer'),random_id_v_tabulke('Vehicle'));
INSERT INTO "Config" ("Customer_id","Vehicle_id")
VALUES (random_id_v_tabulke('Customer'),random_id_v_tabulke('Vehicle'));

--Shipment
insert into "Shipment" ("User_code", "Date_time_close", "Customer_id", "Vehicle_id")
select	random_code(),
       random_timestamp(),
       random_id_v_tabulke('Customer'),
       random_id_v_tabulke('Vehicle')
from generate_series(1, 100) as seq(i);
-- Pattern
insert into "Pattern" ("Customer_id")
select	random_id_v_tabulke('Customer')
from generate_series(1, 6) as seq(i);
--Work_statement

insert into "Work_statement" ("User_code","Work", "Time_start", "Time_end")
select	random_code(),
		floor(random()),
		random_timestamp(),
		random_timestamp()

from generate_series(1, 50) as seq(i);
-- Stillage_type
insert into "Stillage_type" ("Name")
select	random_text()
from generate_series(1, 10) as seq(i);
--Pattern_Item
insert into "Pattern_Item" ("Number","Pattern_id","Stillage_type_id")
select	floor(random()),
       random_id_v_tabulke('Pattern'),
       random_id_v_tabulke('Stillage_type')


from generate_series(1, 100) as seq(i);

--Stillage
insert into "Stillage" ("Date_time_start", "Date_time_end",
                        "Stillage_number", "Stillage_Number_on_Header",
                        "First_scan_product", "Last_scan_product",
                        "JLR_Header_NO", "Carriage_L_JLR_H", "_Check",
                        "First_scan_TLS_code", "Last_scan_TLS_code",
                        "Stillage_Type_id", "Shipment_id",
                        "TLS_range_start", "TLS_range_stop", "Note")
select	random_timestamp(),
		random_timestamp(),
		random_between_big(1,11111111),
		random_between_big(1,11111111),
		random_between_big(1111,5555),
		random_between_big(5556,9999),
		random_between_big(1,99999),
		random_text(),
		1,
		random_between_big(111111,555555),
		random_between_big(555555,999999),
		random_id_v_tabulke('Stillage_type'),
		random_id_v_tabulke('Shipment'),
		random_between_big(1111,5555),
		random_between_big(5556,9999),
		random_text()


from generate_series(1, 50) as seq(i);

--Advanced_user
insert into "Advanced_user" ("User_code","Config_id")
select	random_code(),
       random_id_v_tabulke('Config')

from generate_series(1, 5) as seq(i);

drop function random_between_big(bigint, bigint) cascade;
drop function random_boolean() cascade;
drop function random_text() cascade;
drop function random_timestamp() cascade;
drop function random_id_v_tabulke(text) cascade;
drop function random_code() cascade;

--pridat index

COMMIT;

SELECT schemaname,relname,n_live_tup
  FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

--ROLLBACK;