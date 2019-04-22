# Iceberg

Iceberg is a web application that helps Harvard students locate
where their friends are sitting in Annenberg. Users start by
registering with their full name, email, username, password, and
password confirmation. Then, if their email is a college.harvard.edu
email, they will receive an email with a
randomly generated verification code. They must enter the correct
code in order to use the app, confirming that the user is in fact
a Harvard student. Now they can start using the app!

When users log in, they can see a table with a list of their friends'
usernames, full names, table number, and the time they arrived. They
can also enter their own table number so friends can find them.
There is also the option to add friends by username. This will allow
each friend to see the other's location.

### Usage

1. Download the iceberg folder
2. Unzip the folder
3. Log into your Cloud9 IDE account, possibly the CS50 IDE through Harvard
4. Drag the downloaded folder into your workspace, or upload it
5. Enter the following commnad in your terminal window:
```cd```
```cd iceberg```
```flask run```
6. Click the link generated in your terminal window.

## Example

![gif1](http://g.recordit.co/nDnJNilp7M.gif)
![gif2](http://g.recordit.co/jAo8NuX9Nu.gif)

## Built With

* [CS50 Finance](https://cs50.harvard.edu/2018/fall/psets/8/) - Creating the framework
* [Email Alerts](https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp) - Sending verification email to user

## Authors

* **Max Bahdanovich**
* **Andrea Zhang**

## Acknowledgments

* Many thanks to CS50 and its Finance problem set, which this project
* was modeled off of. We are also very grateful for the StackOverflow
* community that has provided as with the code (at least the idea for
* and a couple of possible implementations) for writing the email
* verification part of our application (here's the link:
* https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp)
