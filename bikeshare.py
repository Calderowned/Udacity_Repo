import time
import pandas as pd
import numpy as np

#These are the links I could wrangle up that helped me write the program, but I know I used a lot more resources.
#Essentially I scoured the whole pandas library looking for a lot of my solutions
#https://www.programiz.com/python-programming/methods/built-in/divmod
#https://stackoverflow.com/questions/11858472/string-concatenation-of-two-pandas-columns
#https://pandas.pydata.org/docs/reference/api/pandas.Series.str.cat.html
#https://www.w3schools.com/python/ref_func_round.asp
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_list = ['chicago','new york city', 'washington']
    city = ''
    while city not in cities_list:
        city_input = input("Would you like to see data for Chicago, New York City, or Washington DC? ")
        city = city_input.lower()
        if city not in cities_list:
            print("Please input a valid city")
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month_list = ['january','february','march',
                  'april','may','june', 'all']
    month = ''
    while month not in month_list:
        month_input = input("Would you like data from January, February, March, April, May, June, or all? ")
        month = month_input.lower()
        if month not in month_list:
            print("Please choose a valid month")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['monday','tuesday','wednesday',
                 'thursday','friday','all']
    day = ''
    while day not in days_list:
        day_input = input("What day of the week would you like data for, or would you like it for all? ")
        day = day_input.lower()
        if day not in days_list:
            print("Please choose a valid day of the week")

    


    
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day): #loads data from the CSV file into the application
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month!= 'all':
        months = ['january','february','march',
                  'april','may','june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month is:", popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day is:", popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("the most popular hour is:", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Riders usually start at:", common_start)

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Riders usually end at:", common_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start - Stop'] = df['Start Station'].str.cat(df['End Station'], sep=' - ') #concatenates the start station and end station data frames
    start_stop = df['Start - Stop'].mode()[0] #finds the most common start/end stations for the given criteria
    print("The most common trip is:", start_stop)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum() #sums the total travel time
    total_travel_time = round(total_travel_time,2)
    print("Total Travel Time:", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() #finds the average total travel time
    mean_travel_time = round(mean_travel_time, 2)
    print("Total Average Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts() #counts the unique values for user type in the dataframe
    print("User Types for this criteria\n" + str(user_types))
    # TO DO: Display counts of gender
    try:
        genders = df['Gender'].value_counts() #counts the unique values for gender in the dataframe
        print("\nGenders for this criteria\n" + str(genders))
    except:
        print("Nothing to report") #since only NYC has the gender column this bit will catch any error that comes as a result of a NaN in the other two cities for gender

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birthday = df['Birth Year'].min() #finds the min, max, and most common birthdays in the dataframe
        most_recent_birthday = df['Birth Year'].max()
        popular_birthday = df['Birth Year'].mode()[0]
        print("\nThe Earliest Birthday is:", earliest_birthday)
        print("The Most Recent Birthday is:", most_recent_birthday)
        print("The Most Un-original Birthday is:", popular_birthday)
    except:
        print("No birthday data available") #exception catch since it looks like only NYC has birthdays
        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    header = df.head() #prints the header for the csv file
    print(header)
    next_five = 0
    while True:
        yes_or_no = input("\n\n Do you want to print 5 more rows of data?\n Yes or No? ") #takes user input
        yes_or_no = yes_or_no.lower()
        if yes_or_no == 'no':
            break
        next_five += 5 #adds 5 to next_five
        print(df.iloc[next_five:next_five+5]) #finds the position of the next five lines and then prints them (the first intance would be df.iloc[5:10] and every time
                                              #the user wants 5 more lines of raw data it increments the count by 5 so the next instance would be [10:15] and so on
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_request = input("Would you like to see the raw data? Yes or No? ") #a quick little check to see if the user wants raw data output
        raw_data_request = raw_data_request.lower()
        if raw_data_request == 'yes': #if the user says yes, it calls the raw_data function
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
