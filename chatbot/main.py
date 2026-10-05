from chatbot import Chatbot


def main():
    """
    Start the Azeem Emporium chatbot.
    """

    bot = Chatbot()

    print("=" * 60)
    print("AZEEM EMPORIUM CUSTOMER CHATBOT")
    print("=" * 60)

    print(bot.get_welcome_message())

    while bot.running:

        user_message = input("\nYou: ")

        response = bot.process_message(
            user_message
        )

        print(f"\n{bot.__class__.__name__}:")
        print(response)


if __name__ == "__main__":
    main()