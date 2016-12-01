# scrapper
A web scrapper for scrapping laboratory names and addresses from Practo.com


To start the project you will first need to create the database using the schema.sql.
Creates a basic db with a table is called leads (developed it for getting potential leads for my company).

practo.py scraps the site.
DbManager includes basisc access to the Database
customer.py was written to identify similar sounding customers to heelp grouping chains of laboratories

Libraries used
BeautifulSoup
requests
Levenshtein

Usage

./practo.py <cityname>

Here cityname is typically the cities as stored in the practo urls - chennai, pune etc.
