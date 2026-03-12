# Plan

Skapa ett FastMCP gransnitt till SCB's PxWebAPI server. Exempel API anrop:

PxWebApi2:
https://statistikdatabasen.scb.se/api/v2/tables/TAB5974

# PxWebApi v2

SCB har tillsammans med Norges statistikbyrå (SSB) tagit fram ett nytt API, PxWebApi v2. Det lanserades i Statistikdatabasen oktober 2025.

API:et låter dig hämta statistik direkt från Statistikdatabasen i maskinläsbart format som kan användas för att automatisera datahämtning, bygga egna appar, rapporter eller analyser. 

Nya PxWebApi v2 är ännu bättre än PxWebApi v1 i och med att det är stabilare och tillåter kraftfullare frågor för uttag. Nya API:et används också för att tillhandahålla data i PxWeb 2 som en fristående applikation.

## Nytt i PxWebApi v2

- Via PxWebApi v2 kan du hämta ut data via GET, inte bara POST som tidigare. Frågan kan då definieras i URL:en.
- Kan gå mot antingen fil- eller SQL/CNMM databas
- Är en egen applikation som kan köras på Windows eller Linux

### Främsta skillnaderna mot PxWebApi v1 

- Strukturen för URL:erna är ändrad så att de blir stabilare och inte påverkas av strukturförändringar i databasen och samtidigt överensstämmer med en RESTful design.
- API:et kommer att exponera mer av den metadata vi har tillgång till.
- Användarupplevelsen för att hämta data kommer att förbättras.
- Det går att göra mer avancerade uttryck för att filtrera ut den informationen du vill hämta via API:et.

PxWebApi v2 är inte bakåtkompatibelt med PxWebApi 1

## Konvertera PxWebApi v1 till PxWebApi v2

För att underlätta övergången till PxWebApi v2 har vi tagit fram en konverterare som snabbt översätter dina befintliga uttag. Klistra in URL:en och JSON-frågan från PxWeb v1 och få fram ditt uttag som GET och POST i PxWebApi v2.

[Konvertera PxWebApi 1.0 till PxWebApi v2](https://pxapiconverter.scb.se/) 

## Dokumentation (engelska)

- [Användarhandledning](https://www.pxtools.net/PxWebApi/documentation/user-guide/)
- [Installera på en IIS-server](https://www.pxtools.net/PxWebApi/documentation/installation/)
- [Konfigurera PxWebApi 2](https://www.pxtools.net/PxWebApi/documentation/configuration/)

### Frågor och problem får du gärna notera som en issue på Github 

[https://github.com/PxTools/PxWebApi/issues](https://github.com/PxTools/PxWebApi/issues)

### Källkod

[https://github.com/PxTools/PxWebApi](https://github.com/PxTools/PxWebApi)

### Specifikation PxWebApi v2

[GitHub PxApiSpecs](https://github.com/PxTools/PxApiSpecs/blob/master/PxAPI-2.yml) som finns här ./docs/PxAPI-2.yml
