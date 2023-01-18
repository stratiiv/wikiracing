from typing import List
import wikipedia as wk
from collections import deque
import networkx as nx
from ratelimit import limits,sleep_and_retry
import psycopg2
from dbcfg.config import config
import time

requests_per_minute = 100
links_per_page = 200
wk.set_lang('uk')

class WikiRacer:
    @staticmethod
    def get_link_titles(title: str) -> List[str]:

        try:
            page = wk.page(title)
            return page.links[:links_per_page]
        except:
            return []    
    
    @staticmethod
    def add_relations_to_db(from_page,links):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
            print("Connected to add some relations =)")
            cur.execute('''CREATE TABLE IF NOT EXISTS page_relations (
                id BIGSERIAL PRIMARY KEY,
                from_page VARCHAR(255),
                to_page VARCHAR(255)
                );
                ''')
            
            insert_query = """INSERT INTO page_relations(
                    from_page,
                    to_page)
                    VALUES(%s,%s);"""
            for to_page in links:
                to_insert = (from_page, to_page)
                cur.execute(insert_query,to_insert)

            conn.commit()
            cur.close()
            print("Added some relations successfully")
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        
    def find_path(self, start: str, finish: str) -> List[str]:
        # implementation goes here
        if not WikiRacer.get_link_titles(start) or not WikiRacer.get_link_titles(finish):
            return []
        
        cache = WikiRacer.from_db(start,finish)
        if cache:
            return cache

        graph = nx.Graph()
        queue = deque()
        queue.append(start)
        found = False
        while not found:
            for page in list(queue):
                print('--------------------------')
                print(f'Item in queue is: {page}')
                link_titles = WikiRacer.get_link_titles(page)
                WikiRacer.add_relations_to_db(page,link_titles)
                if finish in link_titles:
                    print('Path found! Adding to DB..')
                    graph.add_edge(page,finish)
                    found = True
                    shortest_path = nx.dijkstra_path(graph,start,finish)
                    WikiRacer.add_shortest_to_db(shortest_path)
                    return shortest_path
                for title in link_titles:
                    queue.append(title)
                    graph.add_edge(page,title)
                queue.popleft() 
        
    
    
    def from_db(from_page,to_page):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
            select_query = """SELECT path FROM shortest_path WHERE from_page=(%s) AND to_page=(%s);"""
            cur.execute(select_query,(from_page,to_page))
            select_result = cur.fetchone()
            if select_result is not None:
                print('Found existing path in DB!')
                try:
                    path = select_result[0].split(' -> ')
                except AttributeError:
                    path = select_result[0]
                finally:
                    output = [from_page,*path,to_page]
            else:
                print("No already existing path found, finding one soon!")
                output = []
        except (psycopg2.DatabaseError) as error:
            output=[]
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                return output

    def add_shortest_to_db(path: List):
        from_page = path[0]
        to_page = path[-1]
        path = ' -> '.join(path[1:-1])
        to_insert = (from_page, to_page, path) 
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
            cur.execute('''CREATE TABLE IF NOT EXISTS shortest_path (
                id BIGSERIAL PRIMARY KEY,
                from_page VARCHAR(255),
                to_page VARCHAR(255),
                path text
                );
                ''')
            insert_query = """INSERT INTO shortest_path(
                        from_page,
                        to_page,
                        path)
                    VALUES(%s,%s,%s);
                        """
            cur.execute(insert_query,to_insert)
            conn.commit()
            cur.close()
            print("Added path to DB!")
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')



wr=WikiRacer()
min_path = wr.find_path('Фестиваль', 'Пілястра')
# min_path = wr.find_path('Дружба', 'Рим')
# min_path = wr.find_path('Мітохондріальна ДНК', 'Вітамін K')
# min_path = wr.find_path('Марка (грошова одиниця)', 'Китайський календар')
# min_path = wr.find_path('Дружина (військо)', '6 жовтня')
print(min_path)

