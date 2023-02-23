import random
from flask import Flask, render_template
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class TopicSourceGenerator:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
    
    def generate(self, topic, source):
        # Search Google using the custom search engine API
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=f"{topic, source}", cx=self.cse_id).execute()

        # Extract the search results and return them
        results = []
        for item in res.get("items", []):
            result = {"title": item["title"], "link": item["link"]}
            # Fetch the HTML content of the page and extract the publisher URL
            page = requests.get(item["link"]).content
            soup = BeautifulSoup(page, "html.parser")
            publisher_link = soup.find("link", rel="canonical")
            if publisher_link is not None:
                result["publisher_link"] = publisher_link["href"]
            else:
                result["publisher_link"] = ""

            result["publisher_link"] = item.get("publisher", {}).get("url", publisher_link)
            results.append(result)

        return results


# Define the topics and sources tables
topics = ['Assembly Line', 'Algorithms', 'Phrenology', 'Eugenics', 'Human Genetic Engineering', 'Plato', 'Utopian', 'Ethics', 'Pseudoscience', 'Game Theory', 'War Strategy', 'Self-imposed Nonage', 'Darwin', 'Natural Selection', 'Speciation', 'Impostor Syndrome', 'Fascism', 'Nazism', 'The Holocaust', 'Anti-Semitic', 'Maoism', 'Marshmallow Test', 'Cold War', 'Diaspora', 'Bureaucracy', 'Red Tapism', 'Meritocracy', 'Solipsism', 'academy', 'Narcissism', 'Egoism', 'Descriptivism', 'Prescriptivism', 'Dialectic', 'Indigenous', 'Existentialism', 'Rationalism', 'Semantic', 'Anthropology', 'Plurals', 'Schizophrenia', 'DID', 'Jekyll & Hyde', 'Rene Descartes', 'Dualism', 'Brand/Business', 'AI - Two Schools of Thought Homogeneity/Metrics', 'Atrophy-thinking skills', 'Homer', 'Runes', 'GDP/Its Limitations', 'Metrics', 'Romanticism', 'Imperialism', 'Age of Enlightenment', 'Individualism', 'The Enlightenment', 'Confusion Effect of Schooling (Fish)', 'Psychological contract', 'Gig employment', 'Bonded contract', 'Black Friday', 'The Great Depression', 'Liberalisation in India', 'Highbrow/Lowbrow People', 'Mixed Economy / Gig Economy', 'Socialism/Capitalism/Communism', 'Crowdfunding', 'Guerilla Marketing', 'Gamification', 'Filter Bubble']
sources = ["The Hindu", "The Guardian", "Narrative", "The Scientist", "Smithsonian Magazine", "Bloomberg", "Time", "Psychology Today", "New Scientist", "Scientific American", "American Scientist", "National Geographic", "History Extra", "History Net", "academia", "Chronicle of Higher Education", "Speaking Tree", "Big Think", "ALDaily", "RealClearScience", "Bevets", "The Wall Street Journal", "Feynman", "Huffington Post", "Alexander McCall Smith", "The New Atlantis", "CRVP", "The Telegraph", "Science", "Aeon", "BBC Science", "The Economist", "The New Yorker", "The New York Times"]


# Create a new instance of the generator
generator = TopicSourceGenerator("AIzaSyAFVfdTZAZ-VV7lJcAeOHERQe3_b5yEZIc", "16a564dca81a640c2")

@app.route("/")
def index():
    # Generate a new combination of topic and source
    topic = random.choice(topics)
    source = random.choice(sources)
    
    # Use the TopicSourceGenerator to search for results
    results = generator.generate(topic, source)
    
    # Pass the topic, source, and search results to the template
    return render_template("index.html", topic=topic, source=source, results=results)

if __name__ == "__main__":
    app.run()