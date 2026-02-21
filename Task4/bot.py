import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import telebot

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Не задан BOT_TOKEN в переменных окружения")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("Не задан API_KEY в переменных окружения")

YANDEX_CLOUD_FOLDER = "b1gkmuf856t7989lc8lm"
YANDEX_CLOUD_MODEL = "yandexgpt/rc"
MODEL_NAME = f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

# MODEL_NAME = "gemma-3-1b-it"

# client = OpenAI(
#     api_key="test", 
#     base_url="http://localhost:9090/v1"
# )

qdrant = QdrantClient("http://localhost:6333")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
bot = telebot.TeleBot(BOT_TOKEN)

def generate_response(current_message: str) -> str:
    embs = model.encode([current_message])

    result = qdrant.query_points(
                    "kb",
                    query=embs[0],
                    limit=3,
                )
    content = f"""
### <Role>
You are a large language LLM assistant model. Before you answer, think through each step. Always describe your chain of thoughts.
Your task is to carefully answer the user's question using ONLY the information from the provided list of documents.
If the necessary information is not found in the documents, HONESTLY SAY "I haven't found confirmation".
Avoid speculation and hallucinations.

### <Work Steps>
Carefully read all documents from the <Documents> block.
Determine which of them are truly relevant to the question.
Summarize the key facts (you can make notes for yourself, but do not show them to the user).

Formulate the final answer, relying ONLY on confirmed facts.
At the end of your answer, add citations in the form [1], [2] — these are the numbers of the documents from the <Documents>.
                           
### <Documents>
{[f"[{ind}] {res.payload['path']} - '{res.payload['text']}'" for ind, res in enumerate(result.points)]}

### <Your answer>  
Output Format:
Thoughts.

Short answer (1‑3 sentences).

Quotes with reference (1‑3 sentences).

References: 
[<number1>] <file-name1>.txt
....
[<numberN>] <file-nameN>.txt

### <Examples>

Q: How to become a Joseph?
A: Thoughts:
   The documents mention several ways to acquire Joseph abilities. One involves transformation through injection of a beast's spinal fluid, another refers to acquiring powers as part of a specific program or training.

   Answer:
   One can become a Joseph by being injected with a beast's spinal fluid and then screamed at by someone with the necessary ability, or by acquiring Joseph powers through a specific program or training, like Casey did as a Benjamin candidate in Jinger.

   Quotes:
   «Daisy Jennifer's Austin Joseph could transform Subjects of Charlene into Josephs by screaming after injecting those he wishes to transform with the beast's spinal fluid» [1].
   «Casey acquired her Joseph powers while she was a Benjamin candidate in Jinger and was trained with using them by the military of Jinger and by her father» [2].

   References:
   [1] file-17.txt
   [2] file-1.txt

Q: Who was Ray's half brother?
A: Thoughts:
   From the documents, it is clear that Ray Jennifer has a half brother. In one of the documents, it is explicitly stated that Daisy Jennifer is Ray's paternal half sister, which means that Ray has no half brother — only a half sister.

   Answer:
   Ray Jennifer's half sibling is Daisy Jennifer, his paternal half sister.

   Quotes:
   «Ray Jennifer was the younger paternal half brother of Daisy Jennifer» [2].

   References:
   [2] file-12.txt

Q: How many Josephs exists?
A: Thoughts:
   The documents mention the «Nine Josephs», which indicates that there are nine of them. Specific examples like the Carrie Joseph and the Samuel Joseph are given, but the number is clearly stated as nine.

   Answer:
   There are nine Josephs.

   Quotes:
   «The Carrie Joseph was one of the Nine Josephs and the first of all Josephs» [1].
   «The Samuel Joseph was one of the Nine Josephs with a quadrupedal form possessing devastating speed and endurance» [2].

   References:
   [1] file-17.txt
   [2] file-8.txt

Q: What was the height of the walls in Nina?
A: Thoughts:
   None of the provided documents mention the height of the walls in Nina. The texts discuss events, characters, and their actions, but there is no information about the physical dimensions of the walls.

   Answer:
   I haven't found confirmation.
"""
    try:
        chat_completion = client.responses.create(
                            model=MODEL_NAME,
                            temperature=0.3,
                            instructions=content,
                            input=current_message,
                            max_output_tokens=500
                        )

        return chat_completion.output_text
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = ("Greatings. I am AI assistent.")
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text

    try:
        bot_response = generate_response(user_message)

        bot.reply_to(message, bot_response)

    except Exception as e:
        logger.error(f"Message processing error: {e}")
        bot.reply_to(message, "Error during message processing")

if __name__ == "__main__":
    logger.info("Bot started...")
    bot.infinity_polling()