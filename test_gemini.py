import asyncio
from app.core.kernel import create_kernel
from semantic_kernel.contents import ChatHistory


async def main():
    kernel = create_kernel()

    chat_service = kernel.get_service()

    history = ChatHistory()
    history.add_user_message("Reply with: Gemini connection successful")

    response = await chat_service.get_chat_message_contents(
        chat_history=history,
        settings=chat_service.get_prompt_execution_settings_class()()
    )

    print(response[0])


if __name__ == "__main__":
    asyncio.run(main())