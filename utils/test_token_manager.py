"""
Console tester for TokenManager

Run:
    python test_token_manager.py
"""

from TokenManager import TokenManager


def main():
    print("=== TokenManager Console Test ===")

    # Choose model
    model = input("Enter model name (default = gpt-4.1): ").strip()
    if not model:
        model = "gpt-4.1"

    tm = TokenManager(model=model)

    while True:
        print("\nChoose an option:")
        print("1 - Count tokens in plain text")
        print("2 - Count tokens in chat messages")
        print("3 - Exit")

        choice = input("Selection: ").strip()

        # ---------------------------
        # Plain text token counting
        # ---------------------------
        if choice == "1":
            text = input("\nEnter text:\n")
            count = tm.count_text_tokens(text)
            print(f"\nToken count: {count}")

        # ---------------------------
        # Chat token counting
        # ---------------------------
        elif choice == "2":
            messages = []

            print("\nEnter chat messages.")
            print("Type 'done' as role when finished.\n")

            while True:
                role = input("Role (system/user/assistant or done): ").strip()

                if role.lower() == "done":
                    break

                content = input("Content: ")

                messages.append({
                    "role": role,
                    "content": content
                })

            count = tm.count_chat_tokens(messages)

            print("\nMessages entered:")
            for msg in messages:
                print(f"{msg['role']}: {msg['content']}")

            print(f"\nEstimated token count: {count}")

        # ---------------------------
        # Exit
        # ---------------------------
        elif choice == "3":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
