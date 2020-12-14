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

### Running Tests on the Web App   
* Step 10: From the home project directory, type 'docker-compose run web /bin/bash'   
* Step 11: Type 'cd moneypool'   
* Step 12: python manage.py test   
      --Latest number of tests: 36

### Testing Coverage on the Web App
* Step 13: From the home project directory, type 'docker-compose run web /bin/bash'   
* Step 14: Type pip install coverage   
* Step 15: Type 'cd moneypool'   
* Step 16: Type 'coverage run --source='.' manage.py test myapp'   
* Step 17: Type 'coverage report -m   
      --Latest Test shows 75% overall coverage with 72% coverage in views.py

### Testing LCOM4 Values for Models
* Step 18: From the home project directory, type 'docker-compose run web /bin/bash'   
* Step 19: Type pip install lcom
* Step 20: Type lcom moneypool/myapp/models.py   
      --Latest Test shows an Average LCOM4 value of 1

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
* Wrote several unit tests to test both the functions and dynamic urls. 
* Incorportated testing using Django's built in tests in manage.py
* Incorportated coverage testing using python's built in coverage function
* Incorporated LCOM4 testing using python's built in lcom command

  
