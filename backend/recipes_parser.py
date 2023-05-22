import re 

from langchain import HuggingFaceHub, OpenAI
from langchain import PromptTemplate, LLMChain
from config import settings
from recipes_scraper import RedditPostDB
from tqdm import tqdm

class LLMEncoder:

    is_recipe_template = "Given the following text: {question} \n\nDo you think this is a recipe?, Yes, No, Maybe"
    recipe_name_template = "Given the following recipe: {question} \n\nGive me an appropriate name for this recipe. "
    recipe_summary_template = "Given the following recipe: {question} \n\nSummarize this recipe in a few sentences. "
    questions_template = "Given the following recipe: {question} \n\nAnser the following questions: \n Is it vegan ? (yes,no)\n Is it vegetarian ? (yes,no)\n Is it dairy-free ? (yes,no)\n Is it gluten-free ? (yes,no). \n\n Answer each question individually"

    def __init__(self, llm):
        self.llm = llm


    def __call__(self, text):
        # self.prompt = PromptTemplate(template=self.template)
        # self.llm_chain = LLMChain(prompt=self.prompt, llm=llm)
        return self.llm(text)
    
    def is_recipe(self, text):

        prompt = self.is_recipe_template.format(question=text)
        out = self(prompt)

        if re.search(r'Yes', out):
            return True
    
    def get_recipe_name(self, text):
        prompt = self.recipe_name_template.format(question=text)
        out = self(prompt)
        return out
    
    def get_recipe_summary(self, text):
        prompt = self.recipe_summary_template.format(question=text)
        out = self(prompt)
        return out
    
    def get_questions(self, text):
        prompt = self.questions_template.format(question=text)
        
        out = self(prompt).strip(" \n\t:.").split("\n")
        print(out)
        properties = {"vegan":None, "vegetarian":None, "dairy-free":None, "gluten-free":None}
        for prop, answer in zip(properties, out):
            if re.search(r'yes', answer.lower().strip()):
                properties[prop] = True
            elif re.search(r'no', answer.lower().strip()):
                properties[prop] = False
        return properties
    
    @classmethod
    def from_repo_id(cls, repo_id):
        llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature":0, "max_length":64},  huggingfacehub_api_token=settings.hf_api_token)
        return cls(llm)
    
    @classmethod
    def from_openai(cls):
        llm = OpenAI(openai_api_key=settings.openai_api_token)
        return cls(llm)

if __name__ == '__main__':

    repo_id = "databricks/dolly-v2-3b"
    repo_id = "google/flan-t5-xl" # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options


    llm_encoder = LLMEncoder.from_openai()
    reddit_db = RedditPostDB(connection_string=settings.database_url)
     
    recipes = reddit_db.get_all()
    print(f"Found {len(recipes)} recipes")
    for reddit_post in tqdm(recipes):
        # print(reddit_post)
        if reddit_post.text:
            if llm_encoder.is_recipe(reddit_post.text):
                name = llm_encoder.get_recipe_name(reddit_post.text)
                summary = llm_encoder.get_recipe_summary(reddit_post.text)
                properties = llm_encoder.get_questions(reddit_post.text)
                print("__________________________")
                print(name)
                print(summary)
                print(properties)
                print("__________________________")
    
    reddit_posts = reddit_db.get_all()
    print(len(reddit_posts))



