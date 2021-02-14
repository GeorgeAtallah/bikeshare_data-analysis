import time
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from os import system

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['January','February','March','April','May','June']
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please tell me which city you want to explore? 'Chicago' or 'New York City' or 'Washington'. ").lower()
        if city in CITY_DATA:
            print('You selected {}.'.format(city))
            break
        else:
            print('The value you entered is not valid.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please select a month from ('January','February','March','April','May','June') to filter by or press enter for no month filter. ").title()
        if month in months:
            print('You chose to filter by {}.'.format(month))
            break
        elif month=="":
            print("You don't want to filter by a certain month, data for all months will be displayed")
            break
        else:
            print('The value you entered is not valid.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the day you want to filter by (Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday) or press enter for no filter. ').title()
        if day in days:
            print('You chose to display data for {}s.'.format(day))
            break
        elif day == "":
            print("You don't want to filter data by a certain day, data for all days will be displayed")
            break
        else:
            print('The value you entered is not valid.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nReading file and applying filter...\n')
    start_time = time.time()
    
    #Error handling in case file was not found
    try:
        df = pd.read_csv(CITY_DATA[city])
    except Exception as ex:
        print('*'*40)
        print("Oops!", ex.__class__, "occurred.")
        print("Sorry! For some reason the file for {} can't be opened".format(city))
        print('*'*40)
        sys.exit("Exiting script. please check correct file exists in path and try again.") 
        
    df.drop(columns='Unnamed: 0', inplace = True)
    #df['Start Time']= pd.to_datetime(df['Start Time'],format="%d/%m/%Y %H:%M")
    df['Start Time']= pd.to_datetime(df['Start Time'],infer_datetime_format=True)
    #df['End Time']= pd.to_datetime(df['End Time'],format="%d/%m/%Y %H:%M")
    df['End Time']= pd.to_datetime(df['End Time'],infer_datetime_format=True)
    if month != "":
        df = df[df['Start Time'].dt.month == (months.index(month)+1)]
    if day != "":
        df = df[df['Start Time'].dt.dayofweek == (days.index(day))]
    #create columns for start day of week
    df['Start Day'] = df['Start Time'].dt.dayofweek.astype(int)
    #create columns for start month of year
    df['Start Month'] = df['Start Time'].dt.month.astype(int)
    #create columns for hour of day
    df['Start Hour'] = df['Start Time'].dt.hour.astype(int)
    #create column that combines start and end station in one string
    df['Route'] = df['Start Station'].astype(str) +" => "+ df['End Station'].astype(str)
    #replace nan with zero
    df = df.replace('NaN', 0)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df



def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #create empty strings for each value
    month_string,day_string,hour_string = "","",""
    
    # create string for the most common month(s)
    if month != "": #in case month was already selected in filter
        month_string = "Month is: " + month
    else :
        month_string = "The most common months are:"
        mcm= df['Start Month'].mode()
        if len(mcm)==0: #in case no mode for month
            month_string = "All months are equally frequent"
        elif len(mcm)==1:
            month_string = "The most common month is: {}".format(months[mcm[0]-1])
        else:
            for i in range(0,len(mcm)):
                if i == 0:
                    month_string += " " + months[mcm[i]-1]
                elif i == len(mcm)-1:
                    month_string += " and" + months[mcm[i]-1]
                else:
                    month_string += ", " + months[mcm[i]-1]
                
    # create string the most common day of week
    if day != "":
        day_string = "day is: " + day
    else :
        day_string = "The most common days are:"
        mcd= df['Start Day'].mode()
        if len(mcd) == 0: #in case no mode for day
            day_string = "All days are equally frequent"
        elif len(mcd)==1:
           day_string = "The most common day is: {}".format(days[mcd[0]-1])
        else:
            for i in range(0,len(mcd)):
                if i == 0:
                    day_string += " " + days[mcd[i]-1]
                elif i == len(mcd)-1:
                    day_string += " and" + days[mcd[i]-1]
                else:
                    day_string += ", " + days[mcd[i]-1]
                
            
    # create string the most common start hour
    mch = df['Start Hour'].mode()
    if len(mch) == 0: #in case no mode for hour
        hour_string = "All hours are equally frequent"
    elif len(mch) == 1:
        hour_string = "The most common trip start hour is: " + str(mch[0])+"h"
    else:
        hour_string = "The most common trip start hours are:"
        for i in range(0,len(mch)):
            if i == 0:
                hour_string += " " + str(mch[i])+"h"
            elif i == len(mch)-1:
                hour_string += " and" + str(mch[i])+"h"
            else:
                hour_string += ", " + str(mch[i])+"h"
    
    print("{}\n{}\n{}".format(month_string,day_string,hour_string))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    start_time = time.time()
    #create empty strings for each value
    start_station,end_station,route = "","",""
    
    # display most commonly used start station
    mcss = df['Start Station'].mode()
    if len(mcss) == 0: #in case no mode for start station
        start_station = "All stations are equally frequent as start station"
    elif len(mcss) == 1:
        start_station = "The most common start station is: " + str(mcss[0])
    else:
        start_station = "The most common start stations are:"
        for i in range(0,len(mcss)):
            if i == 0 :
                start_station += " " + str(mcss[i])
            elif i == len(mcss)-1 :
                start_station += " and" + str(mcss[i])
            else :
                start_station += ", " + str(mcss[i])

    # display most commonly used end station
    mcse = df['End Station'].mode()
    if len(mcss) == 0: #in case no mode for end station
        end_station = "All stations are equally frequent as end stations"
    elif len(mcss) == 1:
        end_station = "The most common end station is: " + str(mcse[0])
    else:
        end_station = "The most common end stations are:"
        for i in range(0,len(mcse)):
            if i == 0 :
                end_station += " " + str(mcse[i])
            elif i == len(mcss)-1 :
                end_station += " and" + str(mcse[i])
            else :
                end_station += ", " + str(mcse[i])

    # display most frequent combination of start station and end station trip
    mcr = df['Route'].mode()
    if len(mcr) == 0: #in case no mode for route
        route = "All routes are equally frequent"
    elif len(mcr) == 1:
        route = "The most common route is: " + str(mcr[0])
    else:
        route = "The most common routes are:"
        for i in range(0,len(mcr)):
            if i == 0 :
                route += " " + str(mcr[i])
            elif i == len(mcss)-1 :
                route += " and" + str(mcr[i])
            else :
                route += ", " + str(mcr[i])
    
    print("{}\n{}\n{}".format(start_station,end_station,route))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: {}".format(pd.to_timedelta(df['Trip Duration'].sum(),unit='s')))

    # display mean travel time
    meantt = pd.to_timedelta(df['Trip Duration'].mean(),unit='s')
    print("Mean trip time: {} (HH:MM:SS)".format(meantt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].unique()
    if len(user_types)==1:
        user_types_string = "The only user types is: {}.".format(user_types[0])
    else:
        user_types_string = "We found {} types of users:".format(len(user_types))
        for i in range(0,len(user_types)):
            if i == 0:
                user_types_string += " {}".format(user_types[i])
            elif i == len(user_types)-1:
                user_types_string += " and {}.".format(user_types[i])
            else:
                user_types_string += ", {}".format(user_types[i])
    print(user_types_string)
    print('-'*10)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        user_genders = df['Gender'].value_counts()
        #print(user_genders)
        
        print("User count by gender ")
        print(user_genders.to_string())
    else: #in case gender data are not included
        print("Data for {} doesn't include user gender ".format(city))
    print('-'*10)
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        user_birth_year = df['Birth Year'].mode()
        year_string = "\nOldest user was born in {} and is {} years old\nYougest user was born in {} and is {} years old\n".format(int(df['Birth Year'].min()),datetime.now().year-int(df['Birth Year'].min()),int(df['Birth Year'].max()),datetime.now().year-int(df['Birth Year'].max()))
        if len(user_birth_year) == 0:
            year_string += "All birth years are equally common"
        else:
            for i in range(0,len(user_birth_year)):
                if i == 0:
                    year_string += "The most common birth year is {}".format(int(user_birth_year[0]))
                else :
                    if i == 0:
                        year_string += "The most common birth years are {}".format(int(user_birth_year[i]))
                    elif i == len(user_genders):
                        year_string += " and {}.".format(int(user_birth_year[i]))
                    else:
                        year_string += ", {}".format(int(user_birth_year[i]))
        print(year_string)
    else: #in case birth year data are not included
        print("Data for {} doesn't include user birth year".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def read_raw_data(df):
    """
        Prompts the user if they want to read raw data
        displays 5 rows at a time of filtered raw data
        then prompts the user if they want to see 5 more rows
        only the filter is done since unfiltered data will not be useful to the user
        Start Time and End Time changed format in load data function so only their format is changed
        
        Input:
                original DataFrame after new columns were added
                
    """
    read_raw = input('Do you want to check the raw data? Enter yes to read 5 rows .')
    if read_raw.lower() == 'yes':
        #drop columns that were added in load data function
        df.drop(['Start Day','Start Month','Start Hour','Route'] , axis='columns', inplace=True)
        #reindex the df to start from 0 for first row
        df.index = pd.RangeIndex(len(df.index))
        #index to drop and keep track of rows to read
        drop_index = np.array([0,1,2,3,4])
        while read_raw == 'yes':   
            if df.shape[0] > 5 :
                print(df.head())
                df.drop(index = drop_index,axis = 0,inplace = True)
                print("{} rows remaining".format(df.shape[0]))
                drop_index += 5
                read_raw = input('Do you want to read the next 5 rows ? Enter yes to read next 5 rows .')
            elif df.shape[0] == 5 :
                print(df.head())
                df.drop(index = drop_index,axis = 0,inplace = True)
                print("{} rows remaining".format(df.shape[0]))
                drop_index += 5
                read_raw = input('Do you want to read the last 5 rows ? Enter yes to read last 5 rows .')
                break
            else:
                print(df.head(drop_index[4]-df.shape[0]))
                read_raw = input("That's all the rows we have")
                break

def main():
    pd.set_option('display.max_columns', None) #don't limit columns display in terminal
    clear = lambda: system('clear')
    while True:
        clear() #clear screen before starting
        city, month, day = get_filters()
        start_time = time.time()
        df= load_data(city, month, day)
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        print("\nComplete script ran in %s seconds." % (time.time() - start_time))
        print('-'*40)
        read_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
