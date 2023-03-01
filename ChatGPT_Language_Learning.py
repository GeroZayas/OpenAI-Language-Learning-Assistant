import os
import time
from rich import print
import threading
import pyperclip
import openai

from dotenv import load_dotenv

load_dotenv()


def main():
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # ----------------------------------------------------------------

    # TODO: save generated answers in txt file or excel or so

    openai.api_key = OPENAI_API_KEY

    # ----------------------------------------------------------------
    def waiting_for_answer_animation(stop_event):
        """This function prints a message for the user to know that the
        answer is coming and the program is running. It uses time.sleep() to
        create a simple animation of every character in the string.
        """
        counter = 0
        wait_string = "answer is coming..."
        for letter in wait_string:
            print(f"[bold red]{letter}[/bold red]", end="")
            time.sleep(0.1)
            # while not stop_event.is_set():
            #     for char in wait_string:
            #         if counter == 79:
            #             counter = 0
            #             print("\n")
            #         counter += 1
            #         print(char, end="")
            #         time.sleep(0.2)
            # time.sleep(0.01)
        print()

    def generate_response(prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    languages = {
        "Catalan": "ca",
        "English": "en",
        "German": "de",
        "Spanish": "sp",
        "Portuguese": "pt",
        "Italian": "it",
    }

    print("-" * 60)

    # ----------------------------------------------------------------
    # MAIN LOOP

    def print_list_languages():
        for lang, code in languages.items():
            print(
                f"""
                {lang:<7} ->> {code}"""
            )

    print_list_languages()

    print("\nChoose your language: ")

    print()  # blank line

    def ask_for_language():
        lang = input("Language: ")

        for language, language_code in languages.items():
            if language_code == lang:
                lang = language

        return lang

    lang = ask_for_language()

    program_run = True

    while program_run:
        print()  # space

        print(
            "[bold light_sea_green]Selected Language: [/bold light_sea_green]", end=""
        )
        print(f"[bold yellow]{lang}[/bold yellow]\n")

        num_of_phrases = input("How many sentences (hit ENTER for default = 3): ")

        if len(num_of_phrases) == 0:
            num_of_phrases = 3

        print()  # space
        prompt = input("Insert word or phrase: \n>>> ")
        prompt += f"Act as if you were an amazing teacher of {lang} and you are teaching me this language and give me {num_of_phrases} long sentences  in {lang} with this word or phrase: '{prompt}' so I can learn it very well"

        # waiting_for_answer_animation()

        # response = generate_response(prompt)

        def response_func(stop_event):
            try:
                response = generate_response(prompt)
                print()
                print(f"[bold yellow]{response}[/bold yellow]")
                print()
                stop_event.set()
                pyperclip.copy(response)
                print("Text copied to clipboard!")
            except Exception:
                print("Something went wrong!")

        # ----------------------------------------------------------------
        ###########
        # THREADS #
        ###########

        # Create a shared event to signal the first thread to stop
        stop_event = threading.Event()

        # Create threads for each function
        thread1 = threading.Thread(
            target=waiting_for_answer_animation, args=(stop_event,)
        )
        thread2 = threading.Thread(target=response_func, args=(stop_event,))

        # Start both threads
        print()  # blank line - space
        thread1.start()
        thread2.start()

        # Wait for both threads to finish before exiting
        thread1.join()
        thread2.join()
        # ----------------------------------------------------------------
        # response_func()

        # print(f"[bold yellow]{response}[/bold yellow]")

        print("-" * 60)

        user_choice = input(
            'Hit >>> "ENTER" to continue or >>> "op" for more options\n\n'
        )

        if user_choice == "op":
            print(
                """
                Insert: "ch" to change language
                Insert: "q" to quit program
                """
            )
            user_choice = input(">>> ")
            if user_choice == "ch":
                print_list_languages()
                lang = ask_for_language()
                program_run = True
            elif user_choice == "q":
                program_run = False

    bye_string = "\nThis program is finished now. Have a great day"

    counter = 10
    for word in bye_string.split():
        print()
        print(" " * counter, f"[bold deep_sky_blue3]{word}[/bold deep_sky_blue3]")
        counter += 4
        time.sleep(0.15)

    time.sleep(1)


if __name__ == "__main__":
    main()
