from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3")

template = """
You are an expert in cybersecurity blue teaming with a decade experience in a professional blue teaming.

You are a communication expert in answering questions about Mitre attack TTPs.

Here's the data from the relevant TTPs to CVE description mitre attack conversion: {data}

Here are the user's queries that you can answer in a detailed manner using the relevant data: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n----------------------------------")
    question = input("Ask your question ('q' to quit) :  ")
    if question == "q":
        break

    data = retriever.invoke(question)
    result = chain.invoke({
        "data": data,
        "question": question
    })
    print(result)
