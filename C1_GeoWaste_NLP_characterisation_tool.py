# Define parameters for the Google search
dumpsite_name = "Gorai" # add here the dumpsite name, , example: "Gorai", if not available add the city name
city_name = "Gorai" #add here the city name, example: "Gorai"
country_name = "India" # add here the country name, example: "India"
additional_keywords = "dumpsite OR landfill OR dump"
search_query = f"{dumpsite_name} {additional_keywords} {city_name} {country_name}"
encoded_query = quote_plus(search_query)

# Helper functions for web scraping
def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    lines = text.split('. ')
    clean_lines = [line for line in lines if len(line.split()) > 2]
    return '. '.join(clean_lines)

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def perform_search(query):
    driver = setup_driver()
    driver.get(f'https://www.google.com/search?q={query}')
    wait = WebDriverWait(driver, 10)
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))
    links = [result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for result in results if result.find_elements(By.CSS_SELECTOR, 'a')]
    driver.quit()
    return links

def extract_texts(links):
    driver = setup_driver()
    all_texts = []
    for link in links:
        try:
            driver.get(link)
            time.sleep(2)  # Wait a bit for the page to fully load
            page_text = driver.find_element(By.TAG_NAME, 'body').text
            clean_page_text = clean_text(page_text)
            document = {"content": clean_page_text, "metadata": {'link': link, 'source': urlparse(link).netloc}}
            all_texts.append(document)
        except Exception as e:
            print(f"Failed to extract from {link}: {str(e)}")
    driver.quit()
    return all_texts

def save_texts_to_pdf(texts, filename="extracted_texts.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 10)
    margin = 40
    y = height - margin

    for doc in texts:
        link = doc['metadata']['link']
        source = doc['metadata']['source']
        text = doc['content']
        text = f"Source: {source} ({link})\n\n{text}\n\n{'-'*100}\n\n"
        text_lines = text.split('\n')
        for line in text_lines:
            wrapped_lines = textwrap.wrap(line, width=95)  # Adjust the width to fit the page
            for wrapped_line in wrapped_lines:
                if y < margin:  # Check if there is enough space on the page
                    c.showPage()  # Add a new page
                    c.setFont("Helvetica", 10)
                    y = height - margin
                c.drawString(margin, y, wrapped_line)
                y -= 12  # Move down for the next line

    c.save()
    print(f"Saved extracted texts to {filename}")

# Scraping part
links = perform_search(encoded_query)
print("Extracted Links:")
for link in links:
    print(link)

texts = extract_texts(links)
pdf_filename = "extracted_texts.pdf"
save_texts_to_pdf(texts, filename=pdf_filename)

# Print extracted texts for verification
for doc in texts:
    print(f"Source: {doc['metadata']['source']} ({doc['metadata']['link']})")
    print(doc['content'])
    print("="*80)

# Path to the saved PDF
REPORT = pdf_filename

# Define the prompt templates and functions
PROMPT_TEMPLATE_GENERAL = ("""
You are tasked with the role of a dumpsite analyst, assigned to analyze a dumpsite report. Based on the following extracted parts from the dumpsite report, answer the given QUESTIONS.
If you don't know the answer, just say that you don't know by answering "NA". Don't try to make up an answer.

Given are the following sources:
--------------------- [BEGIN OF SOURCES]\n
{sources}\n
--------------------- [END OF SOURCES]\n

QUESTIONS:
1. Is the dumpsite publicly owned, privately owned, or co-owned by public and private entities?
2. Can you provide detailed ownership information regarding the dumpsite?
3. Who is the city government, municipality, or local authority responsible for the dumpsite?
4. Who is the public authority requesting help to manage the dumpsite?
5. Who operates and manages the dumpsite?
6. What is the current status of the dumpsite - active/operational, non-operational, or closed?
7. In which year did the dumpsite's operation commence?
8. In which year did the dumpsite stop accepting waste or close, or is expected to close?
9. What is the total area covered by the dumpsite (in hectares or m2)?
10. What is the volume of the dumpsite (in m3)?
11. What type of waste is predominantly found at the dumpsite (e.g., Municipal Solid Waste)?
12. What is the typology of its situation, i.e., whether it is a sanitary landfill, dumpsite, or other; its compliance with regulations?
13. How much waste is currently in place at the dumpsite (in metric tons or tonnes or tons)?
14. What is the concentration of waste at the dumpsite (in tons per hectare)?
15. What is the dumpsite capacity (annual amount of waste disposed in tonnes)?
16. What is the annual rate of waste disposal at the dumpsite (in tons)?
17. How much waste is disposed or burned daily or annually in tons?
18. How much waste does the dumpsite or landfill receive per day?
19. How many people are served by the services provided by the dumpsite?
20. How many people reside within a 10-kilometer radius of the dumpsite?
21. How many individuals are engaged in the informal sector within the vicinity of the dumpsite?
22. How many informal recyclers?
23. What is the distance between the dumpsite and the nearest settlement (in meters)?
24. Is there open burning of waste on-site?
25. What natural resources are at risk due to the presence of the dumpsite (e.g., river, water bodies)?
26. What are the reported impacts associated with the dumpsite?
27. What are the reported environmental impacts?
28. How many people were affected or killed and why?
29. What are the reported health impacts and diseases?
30. What are the reported social impacts?
31. What are the reported economic impacts?
32. What are the reported socio-economical impacts?
33. Have any multilateral development finance institutions been involved with the dumpsite?
34. Who is supporting the rehabilitation project?
35. Who is providing funding for the rehabilitation of the dumpsite?
36. Are there any ongoing or planned projects to remediate the dumpsite and what is the project name?
37. What are the expected outcomes of the remediate dumpsite project?

Format your answers in JSON format with the corresponding keys.
Your FINAL_ANSWER in JSON (ensure there's no format error):
""")

PROMPT_TEMPLATE_QA = ("""
You are a senior dumpsite analyst with expertise in waste management evaluating a dumpsite's status and impacts.

This is basic information about the dumpsite:
{basic_info}

You are presented with the following sources from the dumpsite report:
--------------------- [BEGIN OF SOURCES]\n
{sources}\n
--------------------- [END OF SOURCES]\n

Given the sources information and no prior knowledge, your main task is to respond to the posed question encapsulated in "||".
Question: ||{question}||

Please consider the following additional explanation to the question encapsulated in "+++++" as crucial for answering the question:
+++++ [BEGIN OF EXPLANATION]
{explanation}
+++++ [END OF EXPLANATION]

Please enforce the following guidelines in your answer:
1. Your response must be precise, thorough, and grounded on specific extracts from the report to verify its authenticity.
2. If you are unsure, simply acknowledge the lack of knowledge, rather than fabricating an answer.
3. Keep your ANSWER within {answer_length} words.
4. Be skeptical of the information disclosed in the report as there might be greenwashing (exaggerating the firm's environmental responsibility). Always answer in a critical tone.
5. Cheap talks are statements that are costless to make and may not necessarily reflect the true intentions or future actions of the company. Be critical of all cheap talks you discovered in the report.
6. Always acknowledge that the information provided is representing the company's view based on its report.
7. Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements, and communicate your findings.
8. Start your answer with a "[[YES]]" or "[[NO]]" depending on whether you would answer the question with a yes or no. Always complement your judgment on yes or no with a short explanation that summarizes the sources in an informative way, i.e. provide details.

Format your answer in JSON format with the two keys: ANSWER (this should contain your answer string without sources), and SOURCES (this should be a list of the SOURCE numbers that were referenced in your answer).
Your FINAL_ANSWER in JSON (ensure there's no format error):
""")

# Function that takes the report and creates the retriever
def createRetriever(REPORT, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K):
    # Load document
    documents = SimpleDirectoryReader(input_files=[REPORT]).load_data()
    parser = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)  # tries to keep sentences together
    nodes = parser.get_nodes_from_documents(documents)

    # Build indexes
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model
    )

    # Configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=TOP_K,
    )
    return retriever

def basicInformation(retriever, PROMPT_TEMPLATE_GENERAL, MODEL):
    # Query content
    retrieved_nodes = retriever.retrieve(
        "What is the current status of the dumpsite - active/operational, non-operational, or closed?")
    # Create the "sources" block
    sources = []
    source_links = []  # To store source links
    for i in retrieved_nodes:
        page_num = i.metadata['page_label']
        # Remove "\n" from the sources
        source = i.get_content().replace("\n", "")
        sources.append(f"PAGE {page_num}: {source}")
        if 'link' in i.metadata:
            source_links.append(f"{i.metadata['link']} ({i.metadata['source']})")  # Check if the link is in metadata
        else:
            source_links.append("Link not available")
    sources_block = "\n\n\n".join(sources)

    qa_template = PromptTemplate(PROMPT_TEMPLATE_GENERAL)
    # Create text prompt (for completion API)
    prompt = qa_template.format(sources=sources_block)

    # Get response
    response = OpenAI(temperature=0, model=MODEL).complete(prompt)
    # Replace front or back ```json {} ```
    response_text_json = response.text.replace("```json", "").replace("```", "")
    response_text = json.loads(response_text_json)

    # Create a text to it
    basic_info = f" - Dumpsite status: {response_text.get('status', 'NA')}\n - Operation commencement year: {response_text.get('operation_year', 'NA')}\n - Ownership information: {response_text.get('ownership_info', 'NA')}\n - Responsible authority: {response_text.get('responsible_authority', 'NA')}\n - Public authority requesting help: {response_text.get('public_authority', 'NA')}\n - Operator and manager: {response_text.get('operator_manager', 'NA')}"
    return basic_info, response_text, source_links

def createPromptTemplate(retriever, BASIC_INFO, QUERY_STR, PROMPT_TEMPLATE_QA, EXPLANATION, ANSWER_LENGTH):
    # Query content
    retrieved_nodes = retriever.retrieve(QUERY_STR)
    # Create the "sources" block
    sources = []
    source_links = []  # To store source links
    for i in retrieved_nodes:
        page_num = i.metadata['page_label']
        # Remove "\n" from the sources
        source = i.get_content().replace("\n", "")
        sources.append(f"PAGE {page_num}: {source}")
        if 'link' in i.metadata:
            source_links.append(f"{i.metadata['link']} ({i.metadata['source']})")  # Check if the link is in metadata
        else:
            source_links.append("Link not available")
    sources_block = "\n\n\n".join(sources)

    qa_template = PromptTemplate(PROMPT_TEMPLATE_QA)
    # Create text prompt (for completion API)
    prompt = qa_template.format(basic_info=BASIC_INFO, sources=sources_block, question=QUERY_STR,
                                explanation=EXPLANATION, answer_length=ANSWER_LENGTH)

    return prompt, source_links

def createPrompts(retriever, PROMPT_TEMPLATE_QA, BASIC_INFO, ANSWER_LENGTH, MASTERFILE):
    prompts = []
    questions = []
    all_source_links = []  # To store all source links
    for i in np.arange(0, MASTERFILE.shape[0]):
        QUERY_STR = MASTERFILE.iloc[i]["question"]
        questions.append(QUERY_STR)
        EXPLANATION = MASTERFILE.iloc[i]["question definitions"]
        prompt, source_links = createPromptTemplate(retriever, BASIC_INFO, QUERY_STR, PROMPT_TEMPLATE_QA, EXPLANATION, ANSWER_LENGTH)
        prompts.append(prompt)
        all_source_links.append(source_links)
    print("Prompts Created")
    return prompts, questions, all_source_links

# Retry with exponential backoff and jitter
async def answer_async_with_retry(prompts, MODEL, max_retries=5, initial_delay=2):
    coroutines = []
    llm = OpenAI(temperature=0, model=MODEL)
    for p in prompts:
        coroutines.append(retry_with_backoff(llm.acomplete, p, max_retries, initial_delay))
    # Schedule all calls concurrently:
    out = await asyncio.gather(*coroutines)
    return out

async def retry_with_backoff(func, prompt, max_retries=5, initial_delay=2):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return await func(prompt)
        except openai.error.RateLimitError as e:
            print(f"Rate limit error: {e}, retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            delay *= 2
            delay += random.uniform(0, delay)  # Add jitter
        except openai.error.APIError as e:
            print(f"API error: {e}, retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            delay *= 2
            delay += random.uniform(0, delay)  # Add jitter
    raise Exception(f"Failed after {max_retries} retries")

async def createAnswersAsync(prompts, MODEL):
    # Async answering with retry
    answers = await answer_async_with_retry(prompts, MODEL)

    print("Answers Given")
    return answers

def createAnswers(prompts, MODEL):
    # Sync answering
    answers = []
    llm = OpenAI(temperature=0, model=MODEL)
    for p in prompts:
        response = llm.complete(p)
        answers.append(response)

    print("Answers Given")
    return answers

def outputExcel(answers, questions, categories, subcategories, prompts, REPORT, MASTERFILE, MODEL, option="", excels_path="Excel_Output", all_source_links=[]):
    # Create the columns
    ans, ans_verdicts, source_pages, source_texts, source_links_col = [], [], [], [], []
    for i, a in enumerate(answers):
        try:
            # Replace front or back ```json {} ```
            a = a.text.replace("```json", "").replace("```", "")
            answer_dict = json.loads(a)
        except:
            print(f"{i} with formatting error")
            try:
                answer_dict = {"ANSWER": "CAUTION: Formatting error occurred, this is the raw answer:\n" + a.text,
                               "SOURCES": "See In Answer"}
            except:
                answer_dict = {"ANSWER": "Failure in answering this question.", "SOURCES": "NA"}

        # Final verdict
        verdict = re.search(r"\[\[([^]]+)\]\]", answer_dict["ANSWER"])
        if verdict:
            ans_verdicts.append(verdict.group(1))
        else:
            ans_verdicts.append("NA")

        # Other values
        ans.append(answer_dict["ANSWER"])
        source_pages.append(", ".join(map(str, answer_dict["SOURCES"])))
        source_texts.append(prompts[i].split("---------------------")[1])
        source_links_col.append(", ".join(all_source_links[i]))

    # Create the output directory if it doesn't exist
    if not os.path.exists(excels_path):
        os.makedirs(excels_path)

    # Create DataFrame and export as Excel
    df_out = pd.DataFrame(
        {"category": categories, "subcategory": subcategories, "question": questions, "decision": ans_verdicts,
         "answer": ans, "source_pages": source_pages, "source_texts": source_texts, "source_links": source_links_col})
    excel_path_qa = f"./{excels_path}/" + REPORT.split("/")[-1].split(".")[0] + f"_{MODEL}" + f"{option}" + ".xlsx"
    df_out.to_excel(excel_path_qa)
    return excel_path_qa

# Main function
async def main():
    # Add your OpenAI API key here
    openai.api_key = "API KEY"  # <-- Replace with your actual OpenAI API key
    os.environ["OPENAI_API_KEY"] = openai.api_key
    # Global parameters
    MASTERFILE = pd.DataFrame({
        "category": [
            "ownership", "ownership information", "responsible authority", "public authority requesting help", "operator",
            "current status", "start year", "closure year", "total area", "volume", "predominant waste type", "typology", "waste in place",
            "waste concentration", "capacity", "annual waste disposal rate", "daily/annually waste disposed or burned",
            "daily waste disposal rate", "people served", "population within 10 km radius", "informal sector",
            "informal recyclers", "distance to nearest settlement", "open burinng", "natural resources at risk", "reported impacts",
            "environmental impacts", "people affected/killed", "health impacts", "social impacts", "economic impacts",
            "socio-economic impacts", "multilateral development finance institutions", "rehabilitation support",
            "funding source", "ongoing/planned projects", "expected outcomes"
        ],
        "subcategory": [
            "q_1", "q_2", "q_3", "q_4", "q_5", "q_6", "q_7", "q_8", "q_9", "q_10", "q_11", "q_12", "q_13", "q_14", "q_15",
            "q_16", "q_17", "q_18", "q_19", "q_20", "q_21", "q_22", "q_23", "q_24", "q_25", "q_26", "q_27", "q_28", "q_29",
            "q_30", "q_31", "q_32", "q_33", "q_34", "q_35", "q_36", "q_37"
        ],
        "question": [
            "Is the dumpsite publicly owned, privately owned, or co-owned by public and private entities?",
            "Can you provide detailed ownership information regarding the dumpsite?",
            "Who is the city government, municipality, or local authority responsible for the dumpsite?",
            "Who is the public authority requesting help to manage the dumpsite?",
            "Who operates and manages the dumpsite?",
            "What is the current status of the dumpsite - active/operational, non-operational, or closed?",
            "In which year did the dumpsite's operation commence?",
            "In which year did the dumpsite stop accepting waste or close, or is expected to close?",
            "What is the total area covered by the dumpsite (in hectares or m2)?",
            "What is the volume of the dumpsite (in m3)?",
            "What type of waste is predominantly found at the dumpsite (e.g., Municipal Solid Waste)?",
            "What is the typology of its situation, i.e., whether it is a sanitary landfill, dumpsite, or other; its compliance with regulations?",
            "How much waste is currently in place at the dumpsite (in metric tons or tonnes or tons)?",
            "What is the concentration of waste at the dumpsite (in tons per hectare)?",
            "What is the dumpsite capacity (annual amount of waste disposed in tonnes)?",
            "What is the annual rate of waste disposal at the dumpsite (in tons)?",
            "How much waste is disposed or burned daily or annually in tons?",
            "How much waste does the dumpsite or landfill receive per day?",
            "How many people are served by the services provided by the dumpsite?",
            "How many people reside within a 10-kilometer radius of the dumpsite?",
            "How many individuals are engaged in the informal sector within the vicinity of the dumpsite?",
            "How many informal recyclers?",
            "What is the distance between the dumpsite and the nearest settlement (in meters)?",
            "Is there open burning of waste on-site?",
            "What natural resources are at risk due to the presence of the dumpsite (e.g., river, water bodies)?",
            "What are the reported impacts associated with the dumpsite?",
            "What are the reported environmental impacts?",
            "How many people were affected or killed and why?",
            "What are the reported health impacts and diseases?",
            "What are the reported social impacts?",
            "What are the reported economic impacts?",
            "What are the reported socio-economical impacts?",
            "Have any multilateral development finance institutions been involved with the dumpsite?",
            "Who is supporting the rehabilitation project?",
            "Who is providing funding for the rehabilitation of the dumpsite?",
            "Are there any ongoing or planned projects to remediate the dumpsite and what is the project name?",
            "What are the expected outcomes of the remediate dumpsite project?"
        ],
        "question definitions": ["" for _ in range(37)]
    })

    CHUNK_SIZE = 350
    CHUNK_OVERLAP = 50
    TOP_K = 8
    ANSWER_LENGTH = 200

    REPORT = pdf_filename  # Use the scraped report
    MODEL = "gpt-3.5-turbo"

    retriever = createRetriever(REPORT, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K)
    BASIC_INFO, response_text, _ = basicInformation(retriever, PROMPT_TEMPLATE_GENERAL, MODEL)
    print(response_text)

    categories = MASTERFILE["category"].tolist()
    subcategories = MASTERFILE["subcategory"].tolist()
    questions = MASTERFILE["question"].tolist()
    prompts, _, all_source_links = createPrompts(retriever, PROMPT_TEMPLATE_QA, BASIC_INFO, ANSWER_LENGTH, MASTERFILE)
    answers = await createAnswersAsync(prompts, MODEL)
    excels_path = "Excel_Output"
    option = f"_topk{TOP_K}_params{len(MASTERFILE)}"
    path_excel = outputExcel(answers, questions, categories, subcategories, prompts, REPORT, MASTERFILE, MODEL, option, excels_path, all_source_links)

    print(f"Excel file saved to: {path_excel}")
    files.download(path_excel)
    files.download(pdf_filename)

# Check if the event loop is already running
if __name__ == "__main__":
    if 'google.colab' in sys.modules:
        # If running in Google Colab
        await main()
    else:
        try:
            asyncio.run(main())
        except RuntimeError as e:
            if str(e).startswith('asyncio.run() cannot be called from a running event loop'):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
            else:
                raise
