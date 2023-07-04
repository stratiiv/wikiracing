# Wikiracing

Wikiracing is a game where the objective is to navigate from one Wikipedia article to another using the minimum number of transitions. This project implements a Python program that finds the shortest path between two given articles on the Ukrainian Wikipedia.

## Features
* Utilizes the Ukrainian Wikipedia to find the shortest path between articles.
* Considers only the first 200 links on each page.
* Implements a Dijkstra algorithm to find the minimum number of transitions.
* Stores the link relations from pages in a PostgreSQL database for efficient retrieval.
* Uses database connections to avoid duplicate queries on subsequent runs.
* Provides SQL queries for analysis of the filled database.

## Usage
1. Clone the repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Set up the PostgreSQL database and configure the database connection in config.py.
4. Run the program
```
python wikiracing.py
```
### Database Queries
The following SQL queries can be used to analyze the filled database:
* **Top 5 most popular articles (those with the most links to themselves):**
```sql
SELECT page_name
FROM link_relations
WHERE target_page_id = source_page_id
GROUP BY page_name
ORDER BY COUNT(*) DESC
LIMIT 5;
```

* **Top 5 articles with the most links to other articles:**
```sql
SELECT page_name
FROM link_relations
WHERE target_page_id != source_page_id
GROUP BY page_name
ORDER BY COUNT(*) DESC
LIMIT 5;
```

* **Average number of second-level descendants for a given article (replace 'article_name' with the desired article):**
```sql
SELECT AVG(descendant_count)
FROM (
    SELECT COUNT(*) AS descendant_count
    FROM link_relations lr1
    INNER JOIN link_relations lr2 ON lr1.target_page_id = lr2.source_page_id
    WHERE lr1.page_name = 'article_name'
    GROUP BY lr1.page_name, lr2.page_name
) AS subquery;
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

ImageAPI is open source and released under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for more details.



