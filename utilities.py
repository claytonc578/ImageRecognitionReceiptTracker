def getChoice(numChoices):
    choice = 0
    while(choice <= 0 or choice > numChoices):
        choice = int(input("Choice: "))
        if choice <= 0 or choice > numChoices:
            print("Invalid choice. Please Try again.")

    return choice
