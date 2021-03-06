# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Settings.
"""

# URI for dbpedia
DBP_URI = u'<http://dbpedia.org/sparql>'

# URI for linked movie db
LMDB_URI = u'<http://data.linkedmdb.org/sparql>'

# Generated query language
LANGUAGE = "sparql"

# NLTK config
NLTK_DATA_PATH = ["/media/Todos/HMMY/3.thesis/dependencies4project"]  # List of paths with NLTK data

# Encoding config
DEFAULT_ENCODING = "utf-8"

# Sparql config
SPARQL_PREAMBLE = u"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX quepy: <http://www.machinalis.com/quepy#>
PREFIX dbpedia: <http://dbpedia.org/ontology/>
PREFIX dbpprop: <http://dbpedia.org/property/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX dcterms: <http://purl.org/dc/terms/>
"""
