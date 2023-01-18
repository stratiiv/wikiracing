SELECT to_url,COUNT(from_url) FROM link_relations GROUP BY to_url ORDER BY COUNT(*) DESC LIMIT 5;
SELECT from_url, COUNT(to_url) FROM link_relations GROUP BY from_url ORDER BY COUNT(*) DESC LIMIT 5;
