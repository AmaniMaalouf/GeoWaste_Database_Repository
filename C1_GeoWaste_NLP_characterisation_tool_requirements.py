# Install required libraries
!pip install selenium openai pandas openpyxl beautifulsoup4 reportlab llama_index==0.10.29

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus
import time
import pandas as pd
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from google.colab import files  # For downloading the file
import random
import textwrap
from urllib.parse import urlparse

# Import LangChain components
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
import numpy as np
import openai
from llama_index.llms.openai import OpenAI
import glob
import json
import asyncio
import sys
