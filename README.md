# MoneyPool

Developers:

* Crisci, Kaleb, [kcrisci94](https://github.com/kcrisci94)
* May, Chase, [cmay11](https://github.com/ChaseMay)
* Gildea, Jacob, [jacobGildea33](https://github.com/jacobGildea33)

# Getting Started   
### Setting up docker:
  
* Step 1: Install Docker
* Step 2: Pull Initial Commit files to local computer
* Step 3: Type the command 'docker build .' to set up environment from Dockerfile

### Setting up the Web App   
* Step 4: Type the command 'docker-compose run web /bin/bash' to run the environment that was set up
* Step 5: Once in the environment, type 'python moneypool/manage.py makemigrations'
* Step 6: Once migrations are made, type 'python moneypool/manage.py migrate'
* Step 7: Exit from the environment by typing 'exit'

### Running the Web App   
* Step 8: Run 'sudo docker-compose up'
* Step 9: Open a web browser and enter the url 'localhost:8000'

# Contribution Guide   
* Create Registration/Login functionality
* Create ability to navigate between pages
* Create ability for users to create trips and view these on their profile
* Create ability for users to view specific information pertaining to a created trip
* Create ability for users to find other users and view their profiles/trips
* Create ability for users to become friends with other users and display friends on profiles
* Create ability for users to invite friends to join their trips
* Create ability to join a trip marked as public by a friend, or accept friend's invite to join a trip, and view all these joined trips on their profile
* Create ability to un-join a trip that was joined
* Create ability for trip owners to create suggestions on possible amenities or activities for the trip   
* Create ability for users to see who else is participating in the trip.   

  
