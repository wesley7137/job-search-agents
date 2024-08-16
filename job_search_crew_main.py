from crewai import Crew
from textwrap import dedent
from job_search_agents import JobSearchAgents
from job_search_tasks import JobSearchTasks
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from llm import llm_openai, llm_ollama, llm_anthropic

load_dotenv()

os.environ["BROWSERLESS_API_KEY"] = os.getenv("BROWSERLESS_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class JobSearchCrew:
    def __init__(self, job_title=None, location=None, candidate_skills=None, candidate_experience=None, resume_file_path=None):
        self.job_title = job_title
        self.location = location
        self.candidate_skills = candidate_skills
        self.candidate_experience = candidate_experience
        self.resume_file_path = resume_file_path
        
    def run(self):
        agents = JobSearchAgents()
        tasks = JobSearchTasks()

        job_search_manager = agents.job_search_manager()
        web_scraper = agents.web_scraper()
        data_extraction_specialist = agents.data_extraction_specialist()
        nlp_analyst = agents.nlp_analyst()
        ranking_specialist = agents.ranking_specialist()

        scrape_task = tasks.scrape_job_listings(web_scraper, self.job_title, self.location, self.candidate_skills)
        extract_task = tasks.extract_and_structure_job_data(data_extraction_specialist, raw_data_path="raw_data.json", output_csv_path="structured_data.csv")
        analyze_task = tasks.analyze_job_descriptions(nlp_analyst, self.candidate_skills, self.candidate_experience, structured_data_path="structured_data.csv")
        rank_task = tasks.rank_opportunities(ranking_specialist, structured_data_path="structured_data.csv", ranking_criteria="skill match, experience level")
        final_report_task = tasks.compile_final_report(job_search_manager)

        crew = Crew(
            agents=[
                job_search_manager,
                web_scraper,
                data_extraction_specialist,
                nlp_analyst,
                ranking_specialist
            ],
            tasks=[
                scrape_task,
                extract_task,
                analyze_task,
                rank_task,
                final_report_task
            ],
            verbose=True,
            process="hierarchical",
            manager_llm=llm_ollama
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to Job Search Crew")
    print('-------------------------------')
    job_title = input(dedent("""
        What job title are you looking for?
    """))
    location = input(dedent("""
        In which location?
    """))
    candidate_skills = input(dedent("""
        List your top skills (comma-separated):
    """)).split(',')
    candidate_experience = input(dedent("""
        Briefly describe your relevant experience:
    """))
    resume_file_path = input(dedent("""
        Enter the path to your resume file:
    """))

    job_search_crew = JobSearchCrew(job_title, location, candidate_skills, candidate_experience, resume_file_path)
    result = job_search_crew.run()
    print("\n\n########################")
    print("## Here is the Job Search Report")
    print("########################\n")
    print(result)
