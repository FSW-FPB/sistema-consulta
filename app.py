import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import json
from typing import List, Dict
from thefuzz import fuzz
import re

app = Flask(__name__)

# Set env Variables
load_dotenv()
JSON_FILE_PATH = os.getenv("JSON_FILE_PATH")
PORT = os.getenv("PORT")


def get_db():
    db_file = JSON_FILE_PATH

    if db_file.endswith(".json"):
        with open(db_file, "r", encoding='utf-8') as f:
            data_bases = json.load(f)
            db_list: List[Dict[str, str]] = data_bases
            db_dict = {data_base["code"]: data_base["name"] for data_base in data_bases}
    return db_list, db_dict


def is_similar(a, b, threshold=80):
    """
    Function to check similarity between two strings with flexible thresholds.
    It returns True if the similarity is above a high threshold (default 80)
    """
    # Calculate similarity scores using fuzzy matching
    similarity = fuzz.token_set_ratio(a, b)
    return similarity >= threshold


@app.route('/cid', methods=['GET'])
def fetch_all_cids():
    """
    Endpoint to retrieve all available CIDs.
    :return: JSON containing a list of CIDs and their descriptions.
    """
    return jsonify(db_list), 200


@app.route('/cid/<string:code>', methods=['GET'])
def search_cid_by_code(code):
    """
    Endpoint to retrieve CID information based on exact code.
    :param code: The CID code to be searched.
    :return: JSON containing the CID code and its description (name) or error message if not found.
    """

    # Converts the code to uppercase to ensure accurate matching.
    cid = db_dict.get(code.upper())

    # Checks if the CID exists in the database.
    if cid is not None:
        return jsonify([{"Código": code.upper(), "Nome": cid}]), 200
    return jsonify({"Error": "Nenhum CID correspondente encontrado"}), 404


@app.route('/cid/search/<string:search_term>', methods=['GET'])
def search_cid_by_name(search_term):
    """
    Endpoint to retrieve CID information based on name similarity, with optional search modes.
    :param search_term: name to search
    :return: JSON matching CID code and its description (name) or error message
    """
    # Get search mode from query parameters; default to "flexible"
    search_mode = request.args.get("search_mode", "flexible")

    # Flexible search - using fuzzywuzzy for approximate matching of the phrase
    if search_mode == "flexible":

        matches = [
            {"Código": code.upper(), "Nome": name}
            for code, name in db_dict.items()
            if is_similar(name, search_term)
        ]
    elif search_mode == "regular":
        pattern = r"\b" + r"\b.*\b".join(re.escape(word) for word in search_term.split()) + r"\b"
        matches = [
            {"Código": code.upper(), "Nome": name}
            for code, name in db_dict.items()
            if re.search(pattern, name, re.IGNORECASE)
        ]
    else:
        return jsonify({"Error": "Modo de busca especificado inválido"}), 400
    return jsonify(matches if matches else {"Error": "Nenhum CID correspondente encontrado"}), 200 if matches else 404


if __name__ == '__main__':
    db_list, db_dict = get_db()
    app.run(port=PORT, debug=True)
