import time
import string
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    city = input('Please state the city you would filter with\chicago , new york city or washington :    ').lower()
    while city not in CITY_DATA:
        print('Invalid city input ')
        city = input(
            'Please state the city you would filter with\chicago , new york city or washington :      ').lower()
    # get user input for month (all, january, february, ... , june)
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input('Please state the month you like to filter from January to June or all for all months :    ').lower()
    while month not in month_list and month != 'all':
        print('invalid entry')
        month = input(
            'Please state the month you like to filter from January to June or all for all months :    ').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Please state the day of the week you like to filter by  or all for the whole week :    ').lower()
    while day not in day_list and day != 'all':
        print('invalid day entry')
        day = input('Please state the day of the week you like to filter by  or all for the whole week :    ').lower()

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Week Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != "all":
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month) + 1
        df = df[df['Month'] == month]
    if day != 'all':
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['Week Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The most common month is ', month_list[common_month - 1])
    # print('The most common month is ', df['Month'].mode()[0])

    # display the most common day of week

    print('The most common day of week is', df['Week Day'].mode()[0])
    # display the most common start hour
    print('The most common start hour is', df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is', df['Start Station'].mode()[0])

    # display most commonly used end station

    print('The most common End station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip

    print('The most frequent combination of start station and end station trip is : \n ',
          df.groupby(['Start Station', 'End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # print('The total travel time is ' ,df['Trip Duration'].sum())
    total_travel_time = float((df['Trip Duration'].sum()))
    days = total_travel_time // (24 * 3600)
    total_travel_time = total_travel_time % (24 * 3600)
    hours = total_travel_time // 3600
    total_travel_time %= 3600
    minutes = total_travel_time // 60
    total_travel_time %= 60
    seconds = round(total_travel_time, 2)
    print('The total travel time is {} Days , {}  hours , {}  minutes & {} seconds '.format(days, hours, minutes,
                                                                                            seconds))
    # display mean travel time
    # print('The mean travel time is ' ,df['Trip Duration'].mean())
    mean_travel_time = float(df['Trip Duration'].mean())
    m_days = mean_travel_time // (24 * 3600)
    mean_travel_time = mean_travel_time % (24 * 3600)
    m_hours = mean_travel_time // 3600
    mean_travel_time %= 3600
    m_minutes = mean_travel_time // 60
    mean_travel_time %= 60
    m_seconds = round(mean_travel_time, 2)

    print('The mean travel time is {} Days , {}  hours , {}  minutes & {} seconds '.format(m_days, m_hours, m_minutes,
                                                                                           m_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nthe user types are as follow\n',
          df['User Type'].value_counts())

    if city == 'washington':
        print('sorry gender and year of birth are not applicable for washington')

    # Display counts of gender
    if city != 'washington':
        print('The counts of genders are  as follow\n', df['Gender'].value_counts())

        print('most recent year of birth :  ', df['Birth Year'].max().astype(int))

        print('most earliest year of birth :  ', df['Birth Year'].min().astype(int))

        print('most common year of birth :  ', df['Birth Year'].mode()[0].astype(int))
    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_row_data(df):
    """asking the user if he likes to display raw data five rows in a time"""
    ask_preview = input('Would you like to display first five rows , press "Y" for yes and "N" for no  '
                        ':   ').lower()
    answer = ['y', 'n']
    if ask_preview not in answer:
        while True:
            print('invalid answer')
            ask_preview = input('Would you like to display first five rows , press "Y" for yes and "N" for no  '
                                ':   ').lower()
            if ask_preview == 'n' or ask_preview == 'y':
                break
    if ask_preview in answer and ask_preview == 'y':
        row_num = 0
        while True:
            print(df.iloc[row_num:row_num + 5])
            row_num += 5
            ask_preview = input('Would you like to display first five rows , press "Y" for yes and "N" for no  '
                                ':   ').lower()
            if ask_preview == 'n':
                break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
