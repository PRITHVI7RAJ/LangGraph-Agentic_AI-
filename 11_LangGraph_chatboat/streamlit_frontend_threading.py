# work - 1
#-> add a sidebar with title + A Start Chat Button + A title named "My Conversations'
#-> generate dynamic thread Id and add it to the session
#-> Display the thread id in sidebar

# work - 2

#-> On Click of new chat open a new chat window
                      #generate a new thread id
                      #save it in session
                      #reset message history
# work - 3                      
#-> create a list to store all thread ids
#-> Load all the thread ids in the sidebar
#-> convert the side bar text to clickable buttbns

# work - 4

#-> on click of a particular thread id load that particular conversation
                     #* extract the thread id and fetch all the message from that thread
                     # * fill the message in  message_history 

# we put Streaming in forented

import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid



# **************************************** utility functions(for new thread id) *************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id' : thread_id}}).values['messages']


# **************************************** Session Setup ******************************
# st.session_state -> dict
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role= 'user'
            else:
                role= 'assistant'
            temp_messages.append({'role':role, 'content':message.text})

        st.session_state['message_history'] = temp_messages

# **************************************** Main UI ************************************
#Loading the  message_history
for message in  st.session_state['message_history']:
    with st.chat_message(message['role']):
       st.text(message['content'])

user_input= st.chat_input('Typing')

if user_input:
    # first add the message to msg history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
       st.text(user_input)

    CONFIG = {'configurable': {'thread_id' : st.session_state['thread_id']}}

    with st.chat_message('assistant'):
       ai_message = st.write_stream(
        message_chunk.text for message_chunk, metadata in chatbot.stream(
            {'messages':[HumanMessage(content= user_input)]},
            config = CONFIG,
            stream_mode= 'messages'
        )

       )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

