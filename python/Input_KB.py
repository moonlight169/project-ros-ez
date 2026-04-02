def Input_kb():
    while True:
        try:
            user_input = input("Enter a command : ")
            if user_input.lower() == 'exit':
                print("Exiting the program.")
                break
            else:
                pass
        except KeyboardInterrupt:
            print("\nBYE NAJA.")
            break

if __name__ == "__main__":
    Input_kb()