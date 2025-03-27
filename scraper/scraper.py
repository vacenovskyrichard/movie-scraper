import time
import random
import requests
import unicodedata
from typing import Optional
from bs4 import BeautifulSoup
from logger.logger import logger
from data.models import Movie, Actor
from data.utils import add_movie_and_actors
from config import TOP_300_FILMS_URLS, USER_AGENTS, CSFD_BASE_URL
from utils import normalize_text


def get_films_urls() -> list[str]:
    film_urls: list[str] = []
    session = requests.Session()  # Create a session object to reuse connections

    for url in TOP_300_FILMS_URLS:
        try:
            # Set a randomized User-Agent for each request
            headers = {"User-Agent": random.choice(USER_AGENTS)}

            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # raises an exception for HTTP errors (4xx, 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')
            film_elements = soup.find_all(class_='article-poster-60')  # get all film elements on current page

            for element in film_elements:
                film_title_element = element.find('a', class_='film-title-name')
                if film_title_element:
                    film_relative_link = film_title_element.get('href')
                    film_urls.append(CSFD_BASE_URL + film_relative_link)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

        time.sleep(random.uniform(1, 5))  # Add random delay between requests

    return film_urls


def get_movie(page_source_soup: BeautifulSoup) -> Optional[Movie]:
    div_tag = page_source_soup.find('div', class_='film-header-name')
    if not div_tag:  # Check if div exists
        return None

    title_tag = div_tag.find("h1")
    if not title_tag:
        return None
    title = title_tag.get_text(strip=True)
    return Movie(title=title, title_normalized=normalize_text(title)) if title_tag else None


def get_actors(page_source_soup: BeautifulSoup) -> list[Actor]:
    actors_div = page_source_soup.find('h4', string="Hrají:")
    if not actors_div:
        print("No actors found.")
        return []

    parent_div = actors_div.find_parent('div')  # Get its parent <div>

    # Find all <a> tags (main actors)
    actor_links = parent_div.find_all('a')

    # Also include actors inside <span class="more-member-1">
    more_actors_span = parent_div.find('span', class_='more-member-1')
    if more_actors_span:
        actor_links.extend(more_actors_span.find_all('a'))

    actors = [actor.get_text(strip=True) for actor in actor_links]  # Extract actor names

    actors_parsed = []
    for actor in actors:
        if " " in actor:  # Ensure there is a space (indicating first and last name)
            first_name, last_name = actor.rsplit(" ", 1)
            # Normalize names and store them in the parsed list
            actors_parsed.append(Actor(
                name=first_name,
                surname=last_name,
                full_name_normalized=f"{normalize_text(first_name)} {normalize_text(last_name)}"
            ))

    return actors_parsed


def scrape_and_save():
    films_urls = get_films_urls()
    request_session = requests.Session()

    for idx, film_url in enumerate(films_urls, 1):
        try:
            # Set a randomized User-Agent for each request
            headers = {"User-Agent": random.choice(USER_AGENTS)}

            response = request_session.get(film_url, headers=headers, timeout=10)  # timeout for response
            response.raise_for_status()  # raises an exception for HTTP errors (4xx, 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')
            actors = get_actors(soup)
            movie = get_movie(soup)
            logger.info(f"Adding movie {idx}/299: {movie.title}")
            add_movie_and_actors(movie, actors)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {film_url}: {e}")

        time.sleep(random.uniform(1, 5))  # Add random delay between requests


if __name__ == "__main__":
    scrape_and_save()
