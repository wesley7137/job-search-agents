from textwrap import dedent
import csv

class JobSearchTasks:
    def scrape_job_listings(self, agent, job_title, location):
        return Task(
            description=dedent(f"""
                Conduct a comprehensive search and scraping operation to gather job listings for the position of {job_title} 
                in {location}. Your task includes:
                1. Identifying and prioritizing the most relevant job boards, company websites, and professional networks.
                2. Scraping job listings, ensuring to capture all relevant details including:
                   - Job Title
                   - Company/Employer
                   - Industry (if available)
                   - Location
                   - Salary (if available)
                   - Job Description
                   - Date Posted
                   - Application Link
                3. Handling any anti-scraping measures ethically and efficiently.
                4. Collecting as much raw data as possible for further processing.
                5. Ensuring the data is up-to-date and from reliable sources.
                6. Saving the raw scraped data in a temporary storage for subsequent tasks.

                Your final answer MUST be a detailed report including:
                - The number of job listings found
                - A summary of the sources used
                - Any challenges encountered during the scraping process
                - An overview of the job market for {job_title} in {location}
                - The raw scraped data in a format ready for further processing

                {self.__tip_section()}
            """),
            agent=agent
        )

    def extract_and_structure_job_data(self, agent, raw_data_path, output_csv_path):
        return Task(
            description=dedent(f"""
                Extract and structure relevant job information from the scraped data. Your task includes:
                1. Reading the raw scraped data from the file located at {raw_data_path}.
                2. Extracting the following information for each job listing:
                   - Job Title
                   - Location
                   - Salary (if available)
                   - Company/Employer
                   - Industry (if available)
                   - Job Description
                   - Date Posted
                   - Application Link
                3. Cleaning and standardizing the extracted data (e.g., consistent date formats, salary ranges, and industry classifications).
                4. Handling missing information appropriately (e.g., marking as "Not Available" or using placeholders).
                5. Identifying and removing any duplicate listings.
                6. Structuring the extracted data into a CSV format.

                Additionally, you are to generate a CSV file at {output_csv_path} with the following columns:
                "Job Title", "Location", "Salary", "Company", "Industry", "Job Description", "Posted Date", "Link"

                Your final answer MUST be:
                - The generated CSV file ready for analysis or reporting.
                - A brief report including:
                    - The number of job listings successfully processed
                    - Any challenges encountered during the extraction process
                    - Statistics on data completeness (e.g., percentage of listings with salary information)
                    - Any interesting patterns or insights noticed during the extraction process

                {self.__tip_section()}
            """),
            agent=agent
        )

    def analyze_job_descriptions(self, agent, candidate_skills, candidate_experience, structured_data_path):
        return Task(
            description=dedent(f"""
                Analyze the job descriptions obtained from the structured data at {structured_data_path} and match them against the candidate's 
                profile. Your task includes:
                1. Applying advanced NLP techniques to extract key requirements, responsibilities, and preferences from 
                   each job description.
                2. Creating a comprehensive skill matrix from the job descriptions.
                3. Analyzing the candidate's skills ({', '.join(candidate_skills)}) and experience ({candidate_experience}) 
                   against this matrix.
                4. Identifying the degree of match for each job listing.
                5. Recognizing any skill gaps or areas where the candidate exceeds expectations.
                6. Calculating a compatibility score for each job based on the candidate's profile and job requirements.

                Your final answer MUST be a detailed report including:
                - An overview of the key skills and requirements in demand for this job category
                - A match percentage and compatibility score for each job listing against the candidate's profile
                - Identified skill gaps and recommendations for skill development
                - A list of job listings where the candidate is a strong match (>80% compatibility)
                - Insights on industry trends based on the analyzed job descriptions

                {self.__tip_section()}
            """),
            agent=agent
        )

    def rank_opportunities(self, agent, structured_data_path, ranking_criteria):
        return Task(
            description=dedent(f"""
                Develop and apply a sophisticated ranking algorithm to prioritize job opportunities based on the candidate's 
                profile and the analyzed job descriptions at {structured_data_path}. Your task includes:
                1. Creating a multi-factor ranking algorithm considering elements such as skill match, experience level, 
                   company reputation, growth potential, and any stated preferences.
                2. Applying this algorithm to the list of job opportunities.
                3. Considering both quantitative (e.g., compatibility score) and qualitative factors (e.g., company culture fit).
                4. Accounting for the candidate's career goals and long-term growth potential.
                5. Providing a confidence score for each ranking.

                Your final answer MUST be a comprehensive report including:
                - A detailed explanation of your ranking methodology
                - A ranked list of job opportunities with scores and brief justifications
                - An analysis of the top 5 opportunities, highlighting why they are particularly suitable
                - Any potential red flags or areas of concern for the top-ranked opportunities
                - Recommendations for how the candidate might improve their chances for the top-ranked positions

                {self.__tip_section()}
            """),
            agent=agent
        )

    def optimize_resume(self, agent, resume_file_path, top_job_listings):
        return Task(
            description=dedent(f"""
                Optimize and tailor the candidate's resume for the top-ranked job opportunities. Your task includes:
                1. Analyzing the resume located at {resume_file_path}.
                2. Identifying key strengths and unique selling points in the candidate's profile.
                3. Tailoring the resume for each of the top 3 ranked job opportunities from {top_job_listings}.
                4. Ensuring the resume is ATS-friendly while also appealing to human recruiters.
                5. Incorporating relevant keywords and phrases from the job descriptions.
                6. Quantifying achievements and impacts where possible.

                Your final answer MUST include:
                - An analysis of the original resume, highlighting strengths and areas for improvement
                - Three versions of the optimized resume, each tailored for one of the top 3 opportunities
                - A summary of the changes made for each version and the rationale behind them
                - Recommendations for additional sections or information that could strengthen the resume
                - Tips for the candidate on how to further customize the resume for future applications

                {self.__tip_section()}
            """),
            agent=agent
        )

    def compile_final_report(self, agent):
        return Task(
            description=dedent(f"""
                As the Job Search Manager, compile a comprehensive final report summarizing the entire job search process 
                and providing strategic recommendations. Your task includes:
                1. Reviewing and synthesizing the outputs from all previous tasks.
                2. Providing an executive summary of the job search results.
                3. Detailing the most promising job opportunities and why they are a good fit.
                4. Outlining a strategic action plan for the candidate's job application process.
                5. Offering insights into the current job market and industry trends relevant to the candidate's field.

                Your final answer MUST be a well-structured, comprehensive report including:
                - An executive summary of the job search process and key findings
                - A detailed analysis of the top 5 job opportunities, including company overviews, role descriptions, 
                  and why they are good matches
                - A SWOT analysis of the candidate's profile in relation to the current job market
                - A step-by-step action plan for applying to the identified opportunities, including customization 
                  strategies for each application
                - Long-term career development recommendations based on observed market trends and skill demands
                - Any additional insights or recommendations that could give the candidate a competitive edge

                Ensure the report is well-formatted, easy to read, and provides actionable insights for the job seeker.

                {self.__tip_section()}
            """),
            agent=agent
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
