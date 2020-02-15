import time
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
    usr_name = input('Before we get started, what is your name?: ').capitalize()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(f"\nThank you {usr_name}! What city are you interested in getting bikeshare data for?\n"
                     f"Please type in the one of the following: Chicago, New York City, or Washington\n"
                     f"City Name: ").lower().replace(" ",
                                                     "_")
        if city == "chicago" or city == "new_york_city" or city == "washington":
            break
        else:
            print("Please type in the correct city.")

    # get user input for month (all, january, february, ... , june)
    months = [
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december'
    ]
    while True:
        month = input("\nWhich month are you interested in?: ").lower()
        if month in months or month == "all":
            break
        else:
            print("Please spell out the correct month (ex: January) or type all for the whole year.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = [
        'sunday',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday'
    ]
    while True:
        day = input("\nPlease type in the day of the week you are interested in or type all: ").lower()
        if day in day_of_week or day == 'all':
            break
        else:
            print("Please enter the correct day or type all.")

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

    df = pd.read_csv(city + '.csv')

    # The following with covert the Start Time and End Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

    # I need to create columns for Month, Day and Start Hour
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # I need to filter the data for month and for day
    month_filtered = (df['Month'] == month.capitalize())
    day_filtered = (df['Day'] == day.capitalize())

    # I need to apply the filters to the dataframes
    if month != 'all' and day != 'all':
        return df[month_filtered & day_filtered]
    else:
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month:", df['Month'].mode()[0])
    # display the most common day of week
    print("\nThe most common day of the week:", df['Day'].mode()[0])
    # display the most common start hour
    print("\nThe most common start hour is:", df['Start Hour'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nThe most commonly used end station is', df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    # In order to display the most frequent combination of start and end station trip, i will need to groupby
    group_stations = df.groupby(['Start Station', 'End Station'])
    value_sorted = group_stations.size().sort_values(ascending=False).head(1)
    print('\nThe most frequent combination of start station and end station trip is: \n',
          value_sorted.to_string())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is', df['Trip Duration'].sum())
    # display mean travel time
    print('\nThe average travel time is', df['Trip Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The count of user types is\n', user_type.to_string())
    # Display counts of gender
    # Gender is only available for New York City and Chicago
    # and I need a conditional to make sure gender and birth year is not displayed when
    # user selects Washington
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print('\nThe gender count for ' + city.replace('_', " ").capitalize() + ' is\n', gender.to_string())
        # Display earliest, most recent, and most common year of birth
        print('\nThe oldest user in ' + city.replace('_', " ").capitalize() + ' was born in',
              df['Birth Year'].mode()[0].astype(int))
        print('\nThe youngest user in ' + city.replace('_', " ").capitalize() + ' was born in',
              df['Birth Year'].max().astype(int))
        print('\nThe most common birth year in ' + city.replace('_', " ").capitalize() + ' is',
              df['Birth Year'].mean().astype(int))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    '''
    This function will allow the user to display 5 rows of the filtered data and will call the next 5
    rows of data everytime the user response with a "yes".
    :param df: filtered dataframes
    :return: 5 rows of raw data and 5 more every time user says yes
    '''
    first_slice = 0
    while True:
        user_request = input('Would you like to see the 5 lines of the raw data? (Yes / No): ').lower()

        if user_request == 'yes':
            print(df.iloc[first_slice:first_slice + 5])
            first_slice += 5
        elif user_request == 'no':
            break
        else:
            print('Sorry, I do not understand.\n Please type in either "Yes" or "No"')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input('Press enter to continue..')  # I want the user to be able to read the data before continuing.
        station_stats(df)
        input('Press enter to continue..')
        trip_duration_stats(df)
        input('Press enter to continue..')
        user_stats(df, city)
        input('Press enter to continue..')
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
