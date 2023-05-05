import pandas as pd
import openai
from openai.embeddings_utils import distances_from_embeddings
import numpy as np
from dotenv import load_dotenv
import os


# Load from .env
load_dotenv()


class MessageParser():
    """
    This class is used to parse a message and create a context for the message
    """
    
    def __init__(self):
        self.df = pd.read_csv('../processed/embeddings.csv', index_col=0)
        self.df['embeddings'] = self.df['embeddings'].apply(eval).apply(np.array)
        openai.api_key = os.environ.get("OPENAI_API_KEY")        
        
    def create_context(self,
        question, df, max_len=1800, size="ada"
    ):
        """
        Create a context for a question by finding the most similar context from the dataframe
        """

        # Get the embeddings for the question
        q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

        # Get the distances from the embeddings
        df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


        returns = []
        cur_len = 0

        # Sort by distance and add the text to the context until the context is too long
        for i, row in df.sort_values('distances', ascending=True).iterrows():
            
            # Add the length of the text to the current length
            cur_len += row['n_tokens'] + 4
            
            # If the context is too long, break
            if cur_len > max_len:
                break
            
            # Else add it to the text that is being returned
            returns.append(row["text"])

        # Return the context
        return "\n\n###\n\n".join(returns)


    def answer_question(
        self,
        df,
        model="text-davinci-003",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=1800,
        size="ada",
        debug=False,
        max_tokens=150,
        stop_sequence=None
    ):
        """
        Answer a question based on the most similar context from the dataframe texts
        """
        context = self.create_context(
            question,
            df,
            max_len=max_len,
            size=size,
        )
        # If debug, print the raw model response
        if debug:
            print("Context:\n" + context)
            print("\n\n")

        try:
            # Create a completions using the question and context
            response = openai.Completion.create(
                prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"Sorry, my creator doesn't allow me to answer this!\". \n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=stop_sequence,
                model=model,
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            print(e)
            return ""
        
    def promptOpenAi(self,message):
        return self.answer_question(self.df, question=message, debug=False, max_tokens=150, stop_sequence=None)