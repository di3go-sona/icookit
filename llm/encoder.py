from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from api_secrets import *

def load_hf_model(repo_id):
    print(f"Loading model from HFHub repo_id: {repo_id}")
    llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature":0, "max_length":64},  huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)
    print(f"Loaded model: {llm}")
    return llm


repo_id = "databricks/dolly-v2-3b"
repo_id = "google/flan-t5-xl" # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options

llm = load_hf_model(repo_id)


template = """Question: {question}

Answer: For instance """
question = "Suggest me a vegan recipe "

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

out = llm_chain.run(question,)
print(out, end='')
print(out)
# print()
# while True:
#     out = llm(out).strip()
#     print(f" {out}", end='')
