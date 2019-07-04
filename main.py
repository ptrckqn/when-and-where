import sql

# Getting the users full name and logging them in/signing them up
user = input('Login: ')
sql.login(user)
quit = False

while(not quit):
    #Printing the options available for the user to select
    print('\n\nWhen&Where \n----------\n1. View All Events \n2. Search Through Events \n3. View My Events \n4. Create A New Event \n5. Delete An Event \n0. Logout')
    choice = int(input('Please Select An Option: '))

    quit = sql.option(choice)

print('Goodbye.')
