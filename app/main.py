from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader

from app.chains import Chain
from app.portfolio import Portfolio
from app.utils import clean_text

app = Flask(__name__)
chain = Chain()
portfolio = Portfolio()

@app.route("/", methods=["GET"])
def home():
    return "Cold Email Generator API is up!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        url = data.get("url", "")

        loader = WebBaseLoader([url])
        page_content = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = chain.extract_jobs(page_content)

        results = []
        for job in jobs:
            skills = job.get("skills", [])
            links = portfolio.query_links(skills)
            email = chain.write_mail(job, links)
            results.append({
                "job": job,
                "email": email
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
