# bikeshare_data-analysis
Overview
This project was done as part of Udacity Data Analysis nanodegree

Aim
The aim of this project is to test our abilities to use python in interacting with users, import and analyzing data related to a bike sharing app.

Data
Bike sharing is a system that allow users to rent bicycles for a fee.
There are a number of stations in each cities, users can pick-up a bicycle from any of them and return it to any other station.

The data used is provided by Motivate, a bike share system provider for many major cities in the United States
The data was gathered in three major cities in the US. Chicago, New York City and Washington.
They are randomly selected for the first six months of 2017 and are saved in three separate data sets.

After some data wrangling on the original raw data the resulting data sets include 6 columns each

    Start Time (e.g., 2017-01-01 00:07:57)
    End Time (e.g., 2017-01-01 00:20:53)
    Trip Duration (in seconds - e.g., 776)
    Start Station (e.g., Broadway & Barry Ave)
    End Station (e.g., Sedgwick St & North Ave)
    User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:

    Gender
    Birth Year

Process
There are 3 main steps in this project
1- Take user input
2- Import data
3- Analyize the data and display results

The analysis that needed to be done on the selected dataset and timeframe was the following:

#1 Popular times of travel (i.e., occurs most often in the start time)

    most common month
    most common day of week
    most common hour of day

#2 Popular stations and trip

    most common start station
    most common end station
    most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration

    total travel time
    average travel time

#4 User info

    counts of each user type
    counts of each gender (only available for NYC and Chicago)
    earliest, most recent, most common year of birth (only available for NYC and Chicago)



    chicago.csv
    new_york_city.csv
    washington.csv
