# Iceberg Design

First, we implemented lots of checking mechanisms to make sure that a user
entered text in each field, such as for username, password, etc.
Then, we also had checks to see if an email or username was already
taken.

Our app has a feature of adding friends because that's the main
thing that makes our app useful. There were other considerations too:
We decided to implement a friends feature to limit the number of
student's locations a user can see. There were two main reasons:
privacy and readability. An app that can allow you to see anyone's
table number, not just people you were friends with, could make
users uncomfortable. By limiting the scope of users' knowledge,
we protect other users' privacy. Additionally, there are hundreds
of people in Annenberg at once. Even if a fraction of the people used
Iceberg, users would have a difficult time scrolling through to find
people they are interested in sitting with.

We also wanted to delete a user's table number after half an hour.
People typically eat for less time than that, so we would not want
a user looking for a friend who had already left. To add a time
constraint, we got the current time and compared it to the time the
user arrived. After converting the times to six digit integers
(2 for hour, 2 for minute, 2 for second), we took the difference.
Then, we needed a little math. If the hour was the same, we looked
for a difference greater than 30 minutes to erase the table. But if the
hour was different, we looked for a difference greater than 70 minutes,
since time skips from 11:59 to 12:00, which would be 115900 to 120000, a
difference of 41 "minutes" instead of 1 real minute in our clock numbering'
system. Thus, we used 70 "minutes", 40 minutes greater than the normal
30 minutes.

We also implemented two levels of email verification, the first one being
checking (using a regular expression) that the email inputted by the user
ends with @college.harvard.edu. We also send the email for verification thus
insuring that the email is valid (we use SMTP protocol to do that, we have the
DNS toolkit in our Checks folder. We check whether the user tries to register
using the same email in register and don't allow doble registration. All of our
checks are run on the server to insure that the user can't go around them
by disabling the JavaScript.

Databases. We made 3 databases: users, friends, and ver. The 'users' database is
responsible for storing the permanent info about the registered users
as well as the timestamp and the table number. We have the 'friends' data-
base that is responsible for storing the friendship connections
between the users. It stores the friend-pairs between users, and it is
implemented in this way because SQL databases don't have a way of
storing a list inside one column. Our last, 'ver' database is used a
temporary database for email verification, before registering a new user
(putting his data into the 'users' database). We store there all of the
data and then, after verifying the email, we delete from the database.

Our web-app also has a feature of changing the password. Users typically
would want this flexibility in case their password is no longer private.

We have a folder named 'Checks' that contains all of the code we were
testing out before using it in the project. It mailnly consists of
the test code for email verfication. It also contains the DNS toolkit
that we've used for our project for email verification. .