import mysql.connector as mysql
# Connecting to the MySQL database
db = mysql.connect(
    host = 'db4free.net',
    user = 'patrickquan',
    passwd = 'zuwzix-setfi4-fEvzug',
    database = 'whenandwhere'
)

# cursor used to query the database
cursor = db.cursor()
userId = -1
# creating the required tables
# cursor.execute('CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))')
# cursor.execute('CREATE TABLE events (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, sqlDate DATE, strDate VARCHAR(255), location VARCHAR(255), attending INT, hostId INT)')
# cursor.execute('CREATE TABLE usersAndEvents (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, userId INT, eventId INT)')

def login(user):
    global userId
    #Searching through the database to see if the user already exists
    cursor.execute('SELECT * FROM users') #index 0 = id, index 1 = name
    allUsers = cursor.fetchall()
    userExists = False
    for i in allUsers:
        if(i[1] == user):
            userExists = True
            userId = i[0]

    #if the user does not exist then add them into the database
    if(not userExists):
        # Adding a new user into the database
        # Executing the query
        cursor.execute('INSERT INTO users (name) VALUES (\'' + user + '\')')
        # Commiting the final output
        db.commit()

        # Storing the newly created userId
        userId = cursor.lastrowid
        print('Hello ' + user + '.')
    else:
        print('Welcome back ' + user + '.')


def option(choice):
    if choice == 0:
        return True
    elif choice == 1:
        allEvents()
    elif choice == 2:
        searchEvents()
    elif choice == 3:
        viewEvents()
    elif choice == 4:
        createEvent()
    elif choice == 5:
        deleteEvent()
    else:
        print('Invalid Option')
    return

#Returning all of the events in the database
def allEvents():
    count = 1
    eventIds = []
    #Selecting all events which have not occured yet
    cursor.execute('SELECT * FROM events WHERE sqlDate >= CURDATE() ')
    events = cursor.fetchall()
    print('\n\n\tWhen \t\tWhere \t\tConfirmed \tHost')
    print('\t---- \t\t----- \t\t--------- \t----')
    for i in events:
        # Getting the hostname from the users table
        cursor.execute('SELECT name FROM users WHERE id = ' + str(i[5]))
        hostName = cursor.fetchall()

        # Correlating the position of the event with the correct id so the proper entry is updated
        eventIds.append(i[0])
        print(str(count) + '.\t' + i[2] + '\t' + i[3] + '\t' + str(i[4]) + '\t\t' + hostName[0][0])

        count += 1

    option = int(input('Please select an event you would like to attend, or enter 0 to go back: '))
    if(option == 0):
        return False
    else:
        # SQL Query required to insert the user id and event id pair
        query = 'INSERT INTO usersAndEvents (userId, eventId) VALUES (%s, %s)'
        values = (userId, eventIds[option - 1])
        cursor.execute(query, values)
        db.commit()

        # Updating the attending column by 1 for the specific event
        query = 'UPDATE events SET attending = attending + 1 WHERE id = ' + str(eventIds[option - 1])
        cursor.execute(query)
        db.commit()

        return False


def searchEvents():
    count = 1
    eventIds = []
    foundEvents = []

    query = input('Enter When or Where: ')
    cursor.execute('SELECT * FROM events WHERE sqlDate >= CURDATE()')
    events = cursor.fetchall()

    for event in events:
        for i in event:
            if(query == i):
                foundEvents.append(event)
    if(len(foundEvents) != 0):
        print('\n\n\tWhen \t\tWhere \t\tConfirmed \tHost')
        print('\t---- \t\t----- \t\t--------- \t----')
        for i in foundEvents:
            # Getting the hostname from the users table
            cursor.execute('SELECT name FROM users WHERE id = ' + str(i[5]))
            hostName = cursor.fetchall()

            # Correlating the position of the event with the correct id so the proper entry is updated
            eventIds.append(i[0])
            print(str(count) + '.\t' + i[2] + '\t' + i[3] + '\t' + str(i[4]) + '\t\t' + hostName[0][0])

            count += 1

            option = int(input('Please select an event you would like to attend, or enter 0 to go back: '))
            if(option == 0):
                return False
            else:
                # SQL Query required to insert the user id and event id pair
                query = 'INSERT INTO usersAndEvents (userId, eventId) VALUES (%s, %s)'
                values = (userId, eventIds[option - 1])
                cursor.execute(query, values)
                db.commit()

                # Updating the attending column by 1 for the specific event
                query = 'UPDATE events SET attending = attending + 1 WHERE id = ' + str(eventIds[option - 1])
                cursor.execute(query)
                db.commit()
    else:
        print('No events found.')

    return False

def viewEvents():
    count = 1
    eventIds = []

    #Selecting all events created by the logged in user
    cursor.execute('SELECT * FROM events WHERE hostId = ' + str(userId))
    events = cursor.fetchall()
    print('\n\n\tWhen \t\tWhere \t\tConfirmed \tHost')
    print('\t---- \t\t----- \t\t--------- \t----')
    for i in events:
        # Getting the hostname from the users table
        cursor.execute('SELECT name FROM users WHERE id = ' + str(i[5]))
        hostName = cursor.fetchall()

        # Correlating the position of the event with the correct id so the proper entry is updated
        eventIds.append(i[0])
        print(str(count) + '.\t' + i[2] + '\t' + i[3] + '\t' + str(i[4]) + '\t\t' + hostName[0][0])

        count += 1

    option = int(input('Please select an event to see all confirmed, or enter 0 to go back: '))

    if(option == 0):
        return False
    else:
        # SQL Query to return all the user ids associated with the specific event
        cursor.execute('SELECT userId FROM usersAndEvents WHERE eventId = ' + str(eventIds[option - 1]))
        confirmedIds = cursor.fetchall()

        print('Confirmed: ', end = '')
        for i in confirmedIds:
            cursor.execute('SELECT name FROM users WHERE id = ' + str(i[0]))
            confirmedName = cursor.fetchall()
            print(confirmedName[0][0] + ' | ', end = '')
        return False

def createEvent():
    # Getting the relevant information to add into the database
    date = input('When (YYYY-MM-DD): ')
    location = input('Where: ')

    # SQL Query required to insert the new event into the events table
    query = 'INSERT INTO events (sqlDate, strDate, location, attending, hostId) VALUES (%s, %s, %s, 1, %s)'
    values = (date, date, location, userId)

    # Adding the event into the events table and commiting to the database
    cursor.execute(query, values)
    db.commit()

    # Getting the id of the newly created event and matching it to the user id
    newId = cursor.lastrowid

    # SQL Query required to insert the user id and event id pair
    query = 'INSERT INTO usersAndEvents (userId, eventId) VALUES (%s, %s)'
    values = (userId, newId)
    cursor.execute(query, values)
    db.commit()

    print(cursor.rowcount, 'Event created')

    return False

def deleteEvent():
    count = 1
    eventIds = []

    #Selecting all events created by the logged in user
    cursor.execute('SELECT * FROM events WHERE hostId = ' + str(userId))
    events = cursor.fetchall()
    print('\n\n\tWhen \t\tWhere \t\tConfirmed \tHost')
    print('\t---- \t\t----- \t\t--------- \t----')
    for i in events:
        # Getting the hostname from the users table
        cursor.execute('SELECT name FROM users WHERE id = ' + str(i[5]))
        hostName = cursor.fetchall()

        # Correlating the position of the event with the correct id so the proper entry is updated
        eventIds.append(i[0])
        print(str(count) + '.\t' + i[2] + '\t' + i[3] + '\t' + str(i[4]) + '\t\t' + hostName[0][0])

        count += 1

    option = int(input('Please select an event to delete, or enter 0 to go back: '))

    if(option == 0):
        return False
    else:
        # SQL Query to delete the event and remove the associated entries in the usersAndEvents table
        cursor.execute('DELETE FROM events WHERE id = ' + str(eventIds[option - 1]))
        db.commit()

        cursor.execute('DELETE FROM usersAndEvents WHERE eventId = ' + str(eventIds[option - 1]))
        db.commit()
        return False
