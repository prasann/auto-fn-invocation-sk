import asyncio
import logging
import os

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from azure.core.credentials import AzureKeyCredential
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.core_plugins import WebSearchEnginePlugin
from azure.search.documents import SearchClient
from semantic_kernel.contents.chat_message_content import ChatMessageContent

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from dotenv import load_dotenv

from refrigerator_plugin import RefrigeratorInfoPlugin

async def main():
    # Load environment variables
    load_dotenv()
    
    # create the kernel
    service_id = "iva"
    kernel = Kernel()
    
    # set the logger to DEBUG to view the logs.
    logging.basicConfig(level=logging.DEBUG)
    
    chat_completion_service = AzureChatCompletion(service_id=service_id)
    kernel.add_service(chat_completion_service)
    
    # add bing plugin to the kernel
    connector = BingConnector()
    kernel.add_plugin(WebSearchEnginePlugin(connector), "BingIt")
    
    #add appliances plugin to the kernel
    search_client = SearchClient(os.getenv("AZURE_AI_SEARCH_ENDPOINT"), 
                                 os.getenv("AZURE_AI_SEARCH_INDEX_NAME"), 
                                 AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_API_KEY")))
    kernel.add_plugin(RefrigeratorInfoPlugin(search_client), "RefrigeratorInfo")

    # enable automatic function calling
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(auto_invoke=True)

    # create a history of the conversation
    history = ChatHistory()

    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")
        if userInput == "exit":
            break

        # add user input to the history
        history.add_user_message(userInput)

        # get the response from the AI with automatic function calling
        result: ChatMessageContent = (await chat_completion_service.get_chat_message_contents(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ))[0]
            
        # print the results
        print("Assistant > " + str(result))

        # add the message from the agent to the chat history
        history.add_message(result)
    
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())