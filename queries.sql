SELECT to_page,COUNT(from_page) FROM page_relations GROUP BY to_page ORDER BY COUNT(*) DESC LIMIT 5;
SELECT from_page, COUNT(to_page) FROM page_relations GROUP BY from_page ORDER BY COUNT(*) DESC LIMIT 5;

SELECT (SELECT COUNT(pr2.to_page)::float FROM page_relations pr JOIN page_relations pr2 ON pr.from_page=pr2.to_page)/
COUNT(DISTINCT pr.to_page) FROM page_relations pr JOIN page_relations pr2 ON pr.to_page=pr2.from_page;

