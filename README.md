## Wikiracing(**tech task**)

Have you ever heard of a game where you need to get from one Wikipedia article to another with the minimum number of transitions?The program finds the shortest path.

A function that requires a parameter as two article names and returns a list of page names through which you can get to it, or an empty list if such a path could not be found.
example:
(‘Дружба’, ‘Рим’) -> [‘Дружба’, ‘Якопо Понтормо’, ‘Рим’]

*This is Python Junior test task given to me from a company*

So the requirements were:
* Only Ukrainian wikipedia
* Technical articles such as [Example](https://uk.wikipedia.org/wiki/%D0%92%D1%96%D0%BA%D1%96%D0%BF%D0%B5%D0%B4%D1%96%D1%8F:%D0%92%D1%96%D0%B9%D0%BD%D0%B0/%D0%A0%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%B8) no need to parse
* The frequency of requests must be limited. 
* Only the first 200 links on each page
* The resulting link relations from pages need to be stored in a postgres database running in the container
* The next time of running, database connections must be used to avoid making the same queries twice
* On the database that fills up after several runs, write queries(**queries.sql**) that look for:
  * Top 5 most popular articles (those with the most links to themselves)
  * Top 5 articles with the most links to other articles
  * For a given article, find the average number of second-level descendants
  * (On extra point) A query with -N parameter returns five traversal paths of length N. The pages in the path must not be repeated.
* The code will be tested on Python 3.10
