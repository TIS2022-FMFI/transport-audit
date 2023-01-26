# transport-audit
Verification of transport packages based on barcodes

# Ako inštalovať


### Základné predpoklady pre spojazdnenie aplikácie:
Telefón s Androidom  verzie > 8, internetovým pripojením a fotoaparátom.
Server dostupný z internetu (verejná ip adresa) s operačným systémom windows  / linux.
Systém slúžiaci na distribúciu reportov serveru.

### Server.
Mobilná aplikácia potrebuje komunikovať so serverom. Ako prvé je potrebné spojazdniť databázu. Postačuje stiahnuť najnovšie PostreSQL a spustiť GENERATE_SCRIPT (zložka ‚sql‘ v repozitári) a nastaviť default užívateľovi oprávnenia na USAGE, QUERY ,INSERT, UPDATE.
Ďalej je potrebné si stiahnuť a nainštalovať python najoptimálnejšie verzie 3.9.7 a doinštalovať nasledujúce knižnice:
```
aniso8601,click,colorama,Flask,Flask-RESTful,Flask-SQLAlchemy,greenlet,importlib-metadata,itsdangerous,Jinja2,MarkupSafe,numpy,psycopg2,python-dateutil,pytz,six,SQLAlchemy,SQLAlchemy-serializer,waitress,Werkzeug,zipp
```
Ďalej nasleduje inštalácia apache a PHP (najoptimálnejšie verzia 7.4.9)
V apache konfiguračnom súbore bude potrebné vytvoriť reverse proxy pre Rest api server napr takto:
```
<VirtualHost *:443>
    ServerName vzorova-domena.com
    ErrorLog ${APACHE_LOG_DIR}/erro.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    ProxyPass / http://127.0.0.1:14030/
    ProxyPassReverse / http://127.0.0.1:14030/
    ProxyRequests Off

	SSLCertificateFile /etc/letsencrypt/live/vzorova-domena.com /fullchain.pem
	SSLCertificateKeyFile /etc/letsencrypt/live/ vzorova-domena.com /privkey.pem
	Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
```
A potom priestor pre webovú administráciu, napr takto:
```
<VirtualHost *:80>
    DocumentRoot "/www/administration/"
    ServerName vzorova-domena.com
</VirtualHost>
```
teraz do priečinku vyššie zvolenom treba nahrať webovú verziu nachádzajúcu sa v repozitári pod priečinkom „web“.

Teraz si treba vygenerovať všeobecný API kľúč (či už cez akýkoľvek generátor hesiel, alebo si vymyslieť vlastný), aby všetky zariadenia mohli spolu komunikovať.
Do db.php treba zadať api kľúč aj prístup k databáze.
Následne si treba otvoriť server.py, ktorý sa bude nachádzať v priečinku určenom pre Rest-api.
V ňom treba zadať rovnaký api kľúč a taktiež zadať prístupové údaje do databázy – rovnako tak aj zadať cestu k importom.

Server.py sa dá spustiť napr. pomocou nasledujúceho príkazu v cmd:
```
@echo off
cmd /k "cd /d „cesta k python env“& activate.bat & cd /d ../../ & waitress-serve --listen=127.0.0.1:14030 --url-scheme 'https' --no-ipv6 server:app"
```
Serverová časť je pripravená 😊



### Android verzia:
Ako prvé je potrebné si zo zložky „src“ v repozitári aplikácie stiahnuť všetky súbory. V súbore config.py treba zadať doménu pre REST-api server, ktorý sa nastavoval vyššie a api kľúč  a následne aplikáciu skompilovať podľa návodu v zložke „manuály“ pod názvom „Kompilácia.pdf“.
Ak máme skompilovaný .apk súbor,  presunieme ho do android zariadenia (napr. pripojením telefónu k počítaču pomocou káblu).
Pre inštaláciu aplikácie je potrebné povoliť inštaláciu z neznámych zdrojov, zvyčajne nachádzajúcu sa 
###### nastavenia - > aplikácie -> Neznáme zdroje (Off) -> On (cesta sa môže líšiť v závislosti od nadstavby alebo verzie androidu).
V telefóne nainštalujte aplikáciu spustením naimportovaného .apk súboru.
Ešte pred spustením, povoľte aplikácií potrebné povolenia 
###### nastavenia - > aplikácie -> zobraziť všetky aplikácie -> Vybrať našu aplikáciu -> oprávnenia -> kamera, súborový systém -> povoliť On (cesta sa môže líšiť v závislosti od nadstavby alebo verzie androidu).
Aplikáciu je možné teraz spustiť a používať😊
