import time
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 20)

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

    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
            if city in ['chicago', 'new york city', 'washington']:
                break
            else:
                print('Please enter a valid city')
        except:
            print('Please enter a valid city')

    # get user input for month (all, january, february, ... , june)

    while True:
        try:
            month = input('Which month? January, February, March, April, May, June or all?'
                          'Please type out the full month name.').lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                print('Please enter a valid month name')
        except:
            print('Please enter a valid month name')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input(
                'Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?? Please type out '
                'the full day name.').lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                break
            else:
                print('Please enter a valid month name')
        except:
            print('Please enter a valid month name')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        month_counts = df['month'].value_counts()
        popular_month_count = month_counts[popular_month]
        print('Most Popular Month:', popular_month)
        print('Number of trips in this month: ', popular_month_count)

    # display the most common day of week
    if day == 'all':
        popular_dow = df['day_of_week'].mode()[0]
        dow_counts = df['day_of_week'].value_counts()
        popular_dow_count = dow_counts[popular_dow]
        print('Most Popular Day of Week:', popular_dow)
        print('Number of trips in this day: ', popular_dow_count)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    hour_counts = df['hour'].value_counts()
    popular_hour_count = hour_counts[popular_hour]
    print('Most Popular Start Hour:', popular_hour)
    print('Number of trips in this hour: ', popular_hour_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station_counts = df['Start Station'].value_counts()
    popular_start_station_count = start_station_counts[popular_start_station]

    print('Most Popular Start Station:', popular_start_station)
    print('Number of trips from this station: ', popular_start_station_count)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station_counts = df['End Station'].value_counts()
    popular_end_station_count = end_station_counts[popular_end_station]

    print('Most Popular End Station:', popular_end_station)
    print('Number of trips to this station: ', popular_end_station_count)

    # display most frequent combination of start station and end station trip
    print('What was the most popular trip from start to end?')
    popular_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print(popular_combination.head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = pd.Timedelta(df['Trip Duration'].sum(), unit='s')
    print('The total travel time done for 2017 through June was: ', total_travel_time)

    # display mean travel time
    average_travel_time = pd.Timedelta(df['Trip Duration'].mean(), unit='s')
    print('The average travel time done for 2017 through June was: ', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('What is the breakdown of users?')
    print(user_types)

    # Display counts of gender
    if city in ['chicago', 'new york city']:
        gender_types = df['Gender'].value_counts()
        print('What is the breakdown of gender?')
        print(gender_types)

    else:
        print('Gender is not provided in Washington')

    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        oldest_birth_year = df['Birth Year'].min()
        youngest_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The oldest year of birth is: ', oldest_birth_year)
        print('The youngest year of birth is: ', youngest_birth_year)
        print('The most common year of birth is: ', most_common_birth_year)

    else:
        print('Birth year is not provided in Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        start_row = 0
        end_row = 5
        while True:
            try:
                view = input('Would you like to view individual trip data? Type \'yes\' or \'no\'.').lower()
                if view == 'yes':
                    data = pd.read_csv(CITY_DATA[city])
                    print(data[start_row:end_row])
                    start_row += 5
                    end_row += 5
                elif view == 'no':
                    break
                else:
                    print('Please enter a valid answer')

            except:
                print('Please enter a valid answer')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
