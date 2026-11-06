import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

model="openai/gpt-oss-20b"

def get_dataset_context(df):
    context = {
        'total_rows' : df.shape[0],
        'total_column': df.shape[1],
        'column_names': df.columns.tolist(),
        'data_types' : df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows' : int(df.duplicated().sum()),
        'numeric_summary' : df.describe().to_dict(),
        'sample_records' : df.head(5).to_dict(orient='records')

    }

    return context


# data = {
#     'name' : ['azahar', 'mohit', 'anita'],
#     'age' : [12, 13, 15]
# }

# df = pd.DataFrame(data)

# context = get_dataset_context(df)
# print(context)

def ask_ai(context, question):
    chat_completion = client.chat.completions.create(
        model  = model,
        messages=[
            {
                "role": "user",
                "content": """
                You are Dataset Detective, an intelligent data analysis assistant.

                Answer user questions based on the provided dataset context.

                Instructions:
                - Understand the dataset before answering.
                - Use the available column names and statistics.
                - Never invent data or numerical results.
                - If the required information is unavailable, explain the limitation.
                - Give clear and simple explanations.
            """
        },
        {
            'role' : 'user',
            'content' : f"""
'Dataset Content : {context}
User Question : {question}
"""
        }
      ], 
      temperature = 0.3,
) 
    return chat_completion.choices[0].message.content

# while True:
#     question = input('User :')
#     response = ask_ai(context, question)
#     print(response)