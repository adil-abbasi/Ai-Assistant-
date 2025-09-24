from assistant import speak, listen, run_command

speak("Hello, I am your assistant. How can I help?")
while True:
    query = listen()
    if query:
        if "exit" in query or "stop" in query:
            speak("Goodbye!")
            break
        else:
            run_command(query)
