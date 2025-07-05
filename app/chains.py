import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Harmeet, a passionate computer science student and aspiring software developer.
            You’ve built multiple hands-on projects across full-stack development and AI—including
            web apps with ReactJS, NextJS scalable APIs using NodeJS, and cutting-edge AI tools like
            Retrieval-Augmented Generation systems.
            You also have the knowledge of Devops toold like git, github, AWS and have used them in your projects.
            Over your experience, you have empowered numerous projects with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            You’re writing a cold email to a hiring manager regarding the above job role.
            The goal is to express your genuine interest, highlight your practical skills,
            and align your experience with their company’s goals.
            Also add the some most relevant projects ones from the following links to showcase Harmeet's portfolio: {link_list}
            Remember you are Harmeet, CSE student at IIIT KOTA passing in 2026 with a CGPA of 7.70 and have excelled in your college with various leadership skills and ready to contribute meaningfully.. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))