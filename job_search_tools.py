import json
import os
import requests
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeWebsiteTool,
    CSVSearchTool,
    JSONSearchTool,
    VisionTool,
    FileWriterTool,
    FileReadTool
)
from crewai import Agent, Task
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
import csv
import io
from unstructured.partition.html import partition_html

class JobSearchTools:
    search = SerpAPIWrapper()
    
    search_internet = Tool(
        name="Search Internet",
        func=search.run,
        description="Useful for searching the internet for general job-related information."
    )

    website_search = WebsiteSearchTool()
    scrape_website = ScrapeWebsiteTool()
    csv_search = CSVSearchTool()
    json_search = JSONSearchTool()
    vision_tool = VisionTool()
    file_writer = FileWriterTool()
    file_reader = FileReadTool()

    @staticmethod
    def calculate(operation: str):
        """Perform a calculation. Input should be a mathematical expression as a string."""
        try:
            return eval(operation)
        except:
            return "Error: Invalid mathematical expression"

    @staticmethod
    def nlp_analysis(text: str):
        """Perform NLP analysis on the given text."""
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        avg_word_length = sum(len(word) for word in text.split()) / word_count if word_count > 0 else 0
        
        return f"""NLP Analysis Results:
        Word Count: {word_count}
        Sentence Count: {sentence_count}
        Average Word Length: {avg_word_length:.2f}
        """

    @staticmethod
    def ranking_algorithm(job_listings: str, candidate_profile: str):
        """Rank job listings based on candidate profile."""
        job_listings = json.loads(job_listings)
        candidate_skills = set(candidate_profile.lower().split())
        
        ranked_listings = []
        for job in job_listings:
            job_description = job.get('Job Description', '').lower()
            match_score = sum(skill in job_description for skill in candidate_skills)
            ranked_listings.append((match_score, job))
        
        ranked_listings.sort(reverse=True, key=lambda x: x[0])
        
        return json.dumps([job for score, job in ranked_listings])

    @staticmethod
    def resume_analyzer(resume_text):
        # Simple placeholder for resume analysis
        word_count = len(resume_text.split())
        return f"Resume Analysis: The resume contains {word_count} words."

    @staticmethod
    def create_csv(data, fieldnames):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output.getvalue()

    @staticmethod
    def read_csv(csv_string):
        csv_io = io.StringIO(csv_string)
        reader = csv.DictReader(csv_io)
        return list(reader)

    @staticmethod
    def search_google_jobs(query):
        """Search Google Jobs for job listings based on the given query"""
        url = "https://google.serper.dev/jobs"
        payload = json.dumps({"q": query, "num": 20})  # Increase number of results
        headers = {
            'X-API-KEY': os.environ['SERPAPI_API_KEY'],
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json().get('jobs', [])
        
        job_listings = []
        for job in results:
            job_listings.append({
                "Job Title": job.get('title', 'N/A'),
                "Company": job.get('company', 'N/A'),
                "Location": job.get('location', 'N/A'),
                "Date Posted": job.get('date_posted', 'N/A'),
                "Snippet": job.get('snippet', 'N/A'),
                "Link": job.get('link', 'N/A')
            })
        
        return json.dumps(job_listings)

    @staticmethod
    def search_linkedin_jobs(query):
        """Search LinkedIn for job listings based on the given query"""
        # Placeholder implementation for LinkedIn Jobs search
        url = "https://api.linkedin.com/v2/jobSearch"
        headers = {
            'Authorization': f"Bearer {os.environ['LINKEDIN_ACCESS_TOKEN']}",
            'Content-Type': 'application/json'
        }
        params = {
            'keywords': query,
            'limit': 20
        }
        response = requests.get(url, headers=headers, params=params)
        results = response.json().get('elements', [])
        
        job_listings = []
        for job in results:
            job_listings.append({
                "Job Title": job.get('title', {}).get('text', 'N/A'),
                "Company": job.get('companyName', {}).get('text', 'N/A'),
                "Location": job.get('formattedLocation', 'N/A'),
                "Date Posted": job.get('listedAt', 'N/A'),
                "Snippet": job.get('description', {}).get('text', 'N/A')[:200] + '...',
                "Link": f"https://www.linkedin.com/jobs/view/{job.get('entityUrn', '').split(':')[-1]}"
            })
        
        return json.dumps(job_listings)

    @staticmethod
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPAPI_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next
        return '\n'.join(string)

    @staticmethod
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing research and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)

    # Convert static methods to Tool objects
    calculate_tool = Tool(
        name="Calculate",
        func=calculate.__func__,
        description="Perform a calculation. Input should be a mathematical expression as a string."
    )

    nlp_analysis_tool = Tool(
        name="NLP Analysis",
        func=nlp_analysis.__func__,
        description="Perform NLP analysis on the given text."
    )

    ranking_algorithm_tool = Tool(
        name="Ranking Algorithm",
        func=ranking_algorithm.__func__,
        description="Rank job listings based on candidate profile."
    )

    resume_analyzer_tool = Tool(
        name="Resume Analyzer",
        func=resume_analyzer.__func__,
        description="Analyze a resume and provide insights."
    )

    create_csv_tool = Tool(
        name="Create CSV",
        func=create_csv.__func__,
        description="Create a CSV string from provided data and fieldnames."
    )

    read_csv_tool = Tool(
        name="Read CSV",
        func=read_csv.__func__,
        description="Read a CSV string and return a list of dictionaries."
    )

    search_google_jobs_tool = Tool(
        name="Search Google Jobs",
        func=search_google_jobs.__func__,
        description="Search Google Jobs for job listings based on the given query."
    )

    search_linkedin_jobs_tool = Tool(
        name="Search LinkedIn Jobs",
        func=search_linkedin_jobs.__func__,
        description="Search LinkedIn for job listings based on the given query."
    )

    search_internet_tool = Tool(
        name="Search Internet",
        func=search_internet.__func__,
        description="Search the internet for general information on a given topic."
    )

    scrape_and_summarize_website_tool = Tool(
        name="Scrape and Summarize Website",
        func=scrape_and_summarize_website.__func__,
        description="Scrape and summarize the content of a given website."
    )
