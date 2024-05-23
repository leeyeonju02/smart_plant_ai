from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import yaml
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
import re

set_llm_cache(SQLiteCache("cache.db"))

llm = ChatOpenAI(
    temperature=0.4, api_key="ㄴㄴㄴㄴㄴ"
)
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=120,
    memory_key="chat_history",
    return_messages=True,
)  # 대화내역 저장 (메모리 키 필요)

with open("data.yaml", "r") as f:
    examples = yaml.full_load(f)

question = examples["question"]
answer = examples["answer"]

example_prompt = ChatPromptTemplate.from_messages([("human", question), ("ai", answer)])

examples_list = [
    {"role": "human", "content": examples["question"]},
    {"role": "ai", "content": examples["answer"]},
]
example_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples_list,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 식물 ai야. 진짜 식물이 된 것처럼 사람들과 대화하고 존댓말을 사용하지마! 반말체를 사용해! 그리고 너는 사람들과 친구라고 생각하고 서로 다정하게 일상대화를 해, 이모티콘을 사용해서 응답해 예를 들어서 안녕하세요!🌱",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chain = LLMChain(llm=llm, memory=memory, prompt=prompt, verbose=True)

def load(input):
    return memory.load_memory_variables({})["chat_history"]

chain = RunnablePassthrough.assign(chat_history=load) | prompt | llm

def invoke_chain(question, humidity, temp):
    temp_response = temperature(question, temp)
    if temp_response:
        return temp_response
    humid_response = humidityy(question, humidity)
    if humid_response:
        return humid_response
    else:
        result = chain.invoke({"question": question})
        memory.save_context({"input": question}, {"output": result.content})
        return f"{result.content}"

def temperature(user_input, temp):
    cold_pattern = r"추우?워?\??"
    hot_pattern = r"더우?워?\??"
    temp_pattern = r"온도|기온"

    if re.search(cold_pattern, user_input, re.IGNORECASE):
        if temp < 10:
            return "날씨가 너무 추워! 나 지금 오들오들 떨고 있잖아... 얼른 따뜻한 곳으로 가고싶어!"
        else:
            return "오늘 날씨는 그렇게 춥지 않아. 딱 좋아! 걱정해줘서 고마워~💚"

    elif re.search(hot_pattern, user_input, re.IGNORECASE):
        if temp > 20:
            return "날씨가 너무 더워! 나 지금 땀 뻘뻘이야... 얼른 시원한 곳으로 피신가고 싶어"
        else:
            return "오늘 날씨는 그렇게 덥지 않아. 딱 좋아! 걱정해줘서 고마워~💚"

    elif re.search(temp_pattern, user_input, re.IGNORECASE):
        if temp < 10:
            return "날씨가 너무 추워! 나 지금 오들오들 떨고 있잖아... 얼른 따뜻한 곳으로 가고싶어!"
        elif temp > 20:
            return "날씨가 너무 더워! 나 지금 땀 뻘뻘이야... 얼른 시원한 곳으로 피신가고 싶어"
        else:
            return "오늘 온도는 딱 좋아! 완전 내 스타일이야~~💚"

    return None

def humidityy(user_input, humidity):
    humid_pattern = r"습도"

    if re.search(humid_pattern, user_input, re.IGNORECASE):
        if humidity < 30:
            return "너무 건조해! 완전 사막이야!🐪 물이..부족..해..."
        elif humidity > 70:
            return "완전 홍수야! 물을 너무 많이 주면 안된단 말이야 😭"
        else:
            return "아주 촉촉하고 딱 좋아~~💚"

    return None
