BEGIN;
CREATE EXTENSION IF NOT EXISTS tsm_system_rows;
-- niektore veci su skopcene od Dr. Šimku (konkretne zo sample projektu)
truncate table User_role, General, User, Vehicle, Customer, Config, Shipment, Pattern, Work_statement, Stillage_type, Advanced_user, Stillage, Pattern_Item restart identity cascade;






$$ language 'plpgsql' STRICT;
    CREATE OR REPLACE FUNCTION random_between_big(low BIGINT ,high BIGINT)
   RETURNS BIGINT AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);        --cmajznute z https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-random-range/
END;

-- General
insert into General (Last_changes, Last_available, Automatic_export)
select	now(),
        now(),
		TRUE
from generate_series(1, 1000000) as seq(i);
--User_Role
insert into User_Role (name)
select "test"
from generate_series(1, 100) as seq(i);


-- User
insert into User (code, Name, Last_name)
select	9,
		"fdsfsdfdsfsdas",
		"dasdasdasd"
from generate_series(1, 1000) as seq(i);
-- Vehicle
insert into Vehicle (Name)
select	"BA420XX"
from generate_series(1, 10000) as seq(i);
-- Customer

insert into Customer (Name)
select	"BESTEST CORP INC."
from generate_series(1, 10000) as seq(i);
-- Config
insert into Config (id)
select	md5(random()::text)

from generate_series(1, 530) as seq(i);
--Shipment
insert into Shipment (Date_time_close)
select	now()
from generate_series(1, 100000) as seq(i);
-- Pattern
insert into Pattern (id)
select	md5(random()::text))
from generate_series(1, 1000) as seq(i);
--Work_statement

insert into Work_statement (Work, Time_start, Time_end)
select	1,
		now(),
		now()

from generate_series(1, 1000000) as seq(i);
-- Stillage_type
insert into Stillage_type (Name)
select	"dsadsada"
from generate_series(1, 2500) as seq(i);
--Pattern_Item
insert into Pattern_Item (Number)
select	1


from generate_series(1, 500000) as seq(i);

--Stillage
insert into Stillage (Date_time_start, Date_time_end, Stillage_number)
select	now(),
		now(),
		55


from generate_series(1, 1000000) as seq(i);

--Advanced_user
insert into Stillage (id)
select	md5(random()::text)


from generate_series(1, 1000) as seq(i);

drop function random_between_big(bigint, bigint) cascade;


--pridat index


ROLLBACK;