# Readme document for database & ETL Pipeline project:
=============================================================================================
## 1) Purpose: ** The main purpose for create this database (sparkifyDB) is being able to analysis the data inside it after proccessing it using several files and ETL pipeline 'etl.py' **

---------------------------------------------------------------------------------------------
## 2) How to run the Python script?

**The first thing during all this project is the create_tables.py Python file,** which you will be running before each step if you modified anything in the database to apply your modifications

**You can run it by the following command in the Python3 terminal:**

!python create_tables.py

*NOTE: if there is an error, check your code in 'create_tables.py' and make sure that you followed the instructions*

**And you can also run etl.py file after you are done editing it by:**

!python etl.py

---------------------------------------------------------------------------------------------

## 3) Explanation of the files in the repository:

Here is an explanation of each file:

- create_tables.py: where your database and tables will be created via 'sql_queries.py'.
- etl.py: where you will create an ETL pipeline to transfer the data from the source into the database.
- etl.ipynb: this file will show you the instructions to create your own ETL pipeline successfully and you should follow it before running 'etl.py'.
- sql_queries.py: here you will write every SQL query to be running by other files.
- test.ipynb: this file will help you to test your files 'create_tables.py' and 'etl.py' and make sure they are running correctly.

And also we have 'data' folder which contains either 'song_data' files and 'log_data' files and you will test your code based on those files.


---------------------------------------------------------------------------------------------
## 4) Justification of ( The database schema design and ETL pipeline ):

I have create the database according to the star schema data model which will contains:

- songplays table (Fact Table): contains the primary key of each dimension table plus three columns (session_id, locatio, user_agent)

### Dimension tables:
- users table: where you will save users data (user_id, first_name, last_name, gender, level).
- songs table: where you will save songs data (song_id, title, artist_id, year, duration).
- artists table: where you will save artists data (artist_id, name, location, latitude, longitude).
- time table: where you will save timestamps of each record in 'songplays' table and time data will be divided into (hour, day, week, month, year, weekday).

### ETL Pipeline:

**let's see the definition of ETL pipeline:**
*ETL pipeline: is the set of processes used to move data from a source or multiple sources into a database such as a data warehouse.*

**And here you will use this ETL pipeline to move the data from the source 'JSON files in data folder' into your music database 'sparkifydb' after proccessing it via several methods in 'etl.py' file**

---------------------------------------------------------------------------------------------
## 5) Example of queries and results for songplay analysis:

SELECT * FROM songs LIMIT 5;

song_id	 title	 artist_id	 year	 duration
========================================================================
SOMZWCG12A8C13C480	I Didn't Mean To	ARD7TVE1187B99BFB1	0	218.93179
------------------------------------------------------------------------
SOUDSGM12AC9618304	Insatiable (Instrumental Version)	ARNTLGG11E2835DDB9	0	266.39628
------------------------------------------------------------------------
SOIAZJW12AB01853F1	Pink World	AR8ZCNI1187B9A069B	1984	269.81832
------------------------------------------------------------------------
SOHKNRJ12A6701D1F8	Drop of Rain	AR10USD1187B99F3F1	0	189.57016
------------------------------------------------------------------------
SOCIWDW12A8C13D406	Soul Deep	ARMJAGH1187FB546F3	1969	148.03546
------------------------------------------------------------------------


SELECT * FROM songplays

songplay_id	start_time	user_id	level	song_id	artist_id	session_id	location	user_agent
========================================================================
1	2018-11-30 00:22:07.796000	91	free	None	None	829	Dallas-Fort Worth-Arlington, TX	Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)
------------------------------------------------------------------------

---------------------------------------------------------------------------------------------