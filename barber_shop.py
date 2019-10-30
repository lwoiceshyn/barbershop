import math
import random

# Starting Time
TIME_INITIAL = (9,0)
#Set for different average arrival time
AVG_ARRIVAL_TIME = 10

class Clock(object):
    '''
    Clock class with minute resolution.
    '''
    def __init__(self, hour=0, minute=0):
        if hour <= 23 and hour >= 0:
            self.hour = hour
        else:
            print('Invalid value for hour. Must be (0,23)')
        if minute <= 59 and minute >= 0:
            self.minute = minute
        else:
            print('Invalid value for minute. Must be (0,59)')    
    
    def tick(self):
        '''
        Increments current time by 1 minute.
        '''
        self.minute += 1
        if self.minute == 60:
            self.hour += 1
            if self.hour == 24:
                self.hour = 0
            self.minute = 0
    
    def reverse_tick(self):
        '''
        Increments current time by 1 minute.
        '''
        self.minute -= 1
        if self.minute == -1:
            self.hour -= 1
            if self.hour == -1:
                self.hour = 23
            self.minute = 59
    
    def tick_amount(self, minutes):
        '''
        Increments current time by N minutes.
        '''
        for _ in range(minutes):
            self.tick()
    
    def get_time(self):
        return (self.hour, self.minute)
        
    def __str__(self):
        min_digits = len(str(self.minute))
        hour_digits = len(str(self.hour))
        if hour_digits == 1:
            if min_digits == 1:
                return '0' + str(self.hour) + ":" + '0' + str(self.minute)
            else:
                return '0' + str(self.hour) + ":" + str(self.minute)
    
        else:
            if min_digits == 1:
                return str(self.hour) + ":" + '0' + str(self.minute)
            else:
                return str(self.hour) + ":" + str(self.minute)
            
    @staticmethod
    def time_string(time):
        '''
        Convert external time hour/minute pairs into printable strings.
        '''
        hour = time[0]
        minute = time[1]
        min_digits = len(str(minute))
        hour_digits = len(str(hour))
        if hour_digits == 1:
            if min_digits == 1:
                return '0' + str(hour) + ":" + '0' + str(minute)
            else:
                return '0' + str(hour) + ":" + str(minute)
    
        else:
            if min_digits == 1:
                return str(hour) + ":" + '0' + str(minute)
            else:
                return str(hour) + ":" + str(minute)
            
    @staticmethod
    def time_difference(earlier_time, later_time):
        '''
        Calculates time difference between two times.
        '''
        hour_difference = later_time[0] - earlier_time[0]
        minute_difference = later_time[1] - earlier_time[1]
        
        if hour_difference >= 0:
            if minute_difference >= 0:
                return (hour_difference, minute_difference)
            else:
                return (hour_difference -1, minute_difference + 60)
        else:
            if minute_difference >= 0:
                return (24 + hour_difference, minute_difference)
            else:
                return (24 + hour_difference - 1, minute_difference + 60)
    
    @staticmethod
    def time_to_minutes(time):
        return 60 * time[0] + time[1] 

    @staticmethod
    def add_minutes(time, minutes):
        temp_clock = Clock(*time)
        temp_clock.tick_amount(minutes)
        return temp_clock.get_time()

    class Barber():
    def __init__(self, name):
        '''
        Str -> NoneType
        Constructer for a barber object. Assigns the given name to the barber.
        '''
        self.busy = False
        self.customer_name = None
        self.end_time = None
        self.name = name

    def add_customer(self, start_time, customer_name):
        '''
        Int, Str -> NoneType
        Assigns a new customer to a barber that is not currently busy. Chooses a random time between 20 and 40 minutes
        for the haircut.
        '''
        self.busy = True
        self.customer_name = customer_name
        self.start_time = start_time
        self.end_time = Clock.add_minutes(start_time, random.randint(20, 40))

    def reset(self):
        '''
        NoneType -> NoneType
        Changes the barber's status from Busy to not Busy.
        '''
        self.busy = False

def next_time():
    '''
    NoneType -> NoneType
    Poisson distribution sampling function to determine when the next customer will arrive.
    '''
    return int(round(-math.log(1.0 - random.random()) / (1.0/AVG_ARRIVAL_TIME)))

class Shop():
    '''
    Shop class that contains customers and barbers. Keeps track of customer ID numbers, which barbers are on shift, etc.
    Contains methods for adding/removing customers/barbers, updating barber statuses, etc.
    Instantiates a dictionary to store arrival times in order to check if customer has been waiting over 30 minutes.
    '''

    def __init__(self):
        '''
        Constructor for the shop class. Initializes empty lists to contain the barbers and customers.
        '''
        self.barbers = []
        self.customers = []
        self.customer_id = 1
        self.customer_arrival_times = {}
        self.first_customer = True

    def add_barber(self, barber):
        '''
        Barber -> NoneType
        Appends a barber to the list of barbers.
        '''
        self.barbers.append(barber)

    def remove_barber(self, barber):
        '''
        Barber -> NoneType
        Removes a barber from the list of barbers, only if that barber does not have a customer.
        '''
        if barber.busy == False:
            self.barbers.remove(barber)

    def add_customer(self, current_time):
        '''
        int -> Bool or String
        Creates a new customer string based on the current customer IDcu number. Handles cases where customer arrives after closing time,
        or customer arrives when the shop is at full capacity.
        Stores arrival time in dictionary for future reference.
        '''
        customer = "Customer-" + str(self.find_current_customer_number())

        print(Clock.time_string(current_time), customer, "entered")
        if current_time[0] >= 17:
            print(Clock.time_string(current_time), customer, "left cursing himself")
            return False
        if len(self.customers) < 15:
            self.customers.append(customer)
            self.customer_arrival_times[customer] = current_time
            return customer
        else:
            print(Clock.time_string(current_time), customer, "left impatiently")
            return False

    def remove_customer(self, customer):
        '''
        String -> NoneType
        Removes a customer from the customers list.
        '''
        self.customers.remove(customer)

    def find_current_customer_number(self):
        '''
        NoneType -> Int
        Returns the current customer ID.
        '''
        if self.first_customer == True:
            self.first_customer = False
            return 1

        else:
            self.customer_id += 1
            return self.customer_id

    def check_barbers(self, current_time):
        '''
        Int -> NoneType
        Checks all barbers to see if they are busy. If so, checks if they have reached their end time yet.
        If they have reached it, the haircut is finished, and the customer leaves, and is removed from the customer list.
        '''
        for barber in self.barbers:
            if barber.busy == True:
                if barber.end_time == current_time:
                    customer = barber.customer_name
                    print(Clock.time_string(current_time), barber.name, "ended cutting", customer + "'s hair")
                    print(Clock.time_string(current_time), customer, "left satisfied")
                    barber.reset()
                    try:
                        self.remove_customer(customer)
                    except:
                        pass

        return False

    def check_finished(self):
        '''
        NoneType -> Bool
        Checks all barbers to see if they are busy. If any are still busy, returns False. Else, returns True.
        '''
        for barber in self.barbers:
            if barber.busy == True:
                return False
        return True

    def end_shift(self, current_time, barber):
        '''
        Int, Barber -> NoneType
        Checks a single barber to see if they are still busy. If not, ends their shift.
        '''
        if barber.busy == False:
            print(Clock.time_string(current_time), barber.name, "ended shift")

    def check_available(self, current_time):
        '''
        Int -> NoneType
        Checks all current barbers to see if they are busy. If not, adds the customer who has been waiting longest to the first
        available barber in the list.
        If a customer has been waiting over 30 minutes, they leave unfulfilled.
        '''
        for customer in self.customers:
            time_difference = Clock.time_difference(self.customer_arrival_times[customer], current_time)
            if Clock.time_to_minutes(time_difference) > 30:
                print(Clock.time_string(current_time), customer, "left unfulfilled")
                self.remove_customer(customer)

        for barber in self.barbers:
            if barber.busy == False:
                longest_wait_time = 0
                longest_waiting_customer = None
                for customer in self.customers:
                    wait_time = Clock.time_difference(self.customer_arrival_times[customer], current_time)
                    wait_time = Clock.time_to_minutes(wait_time)
                    if wait_time > longest_wait_time:
                        longest_wait_time = wait_time
                        longest_waiting_customer = customer
                    if wait_time == 0 and len(self.customers) == 1:
                        longest_waiting_customer = customer
                if longest_waiting_customer != None:
                    barber.add_customer(current_time, longest_waiting_customer)
                    print(Clock.time_string(current_time), barber.name, "started cutting " + longest_waiting_customer + "'s hair")                                           
                    self.remove_customer(longest_waiting_customer)
        

class Barber():
    def __init__(self, name):
        '''
        Str -> NoneType
        Constructer for a barber object. Assigns the given name to the barber.
        '''
        self.busy = False
        self.customer_name = None
        self.end_time = None
        self.name = name

    def add_customer(self, start_time, customer_name):
        '''
        Int, Str -> NoneType
        Assigns a new customer to a barber that is not currently busy. Chooses a random time between 20 and 40 minutes
        for the haircut.
        '''
        self.busy = True
        self.customer_name = customer_name
        self.start_time = start_time
        self.end_time = Clock.add_minutes(start_time, random.randint(20, 40))

    def reset(self):
        '''
        NoneType -> NoneType
        Changes the barber's status from Busy to not Busy.
        '''
        self.busy = False

def main():
    '''
    Main Function - Instantiates the necessary objects, runs through a simulation of a day in the barbershop, and prints the required
    outputs to the console.
    '''
    
    #Initiate the Shop and Barber Classes, and Add the Starting Barbers to the Shop
    shop = Shop()
    time = TIME_INITIAL
    customer_time = TIME_INITIAL
    
    clock = Clock(*TIME_INITIAL)

    a = Barber('Alto')
    b = Barber('Basil')
    c = Barber('Camphor')
    d = Barber('Diogenes')
    e = Barber('Eros')
    f = Barber('Fatoush')
    g = Barber('Glorio')
    h = Barber('Heber')

    starting_barbers = [a,b,c,d]
    switching_barbers = [e,f,g,h]

    for barb in starting_barbers:
        shop.add_barber(barb)

    print(clock, "Barber shop opened")
    print(clock, a.name, "started shift")
    print(clock, b.name, "started shift")
    print(clock, c.name, "started shift")
    print(clock, d.name, "started shift")

    #Loop that runs until the closing time for the shop is reached
    while clock.get_time()[0] < 17:
   
        #Swaps the new shift of barbers in, but only removes the morning shift if they aren't currently in a haircut
        if clock.get_time() == (13,0):
            for barb in starting_barbers:
                shop.end_shift(clock.get_time(), barb)
                shop.remove_barber(barb)
            for barb in switching_barbers:
                shop.add_barber(barb)
            print(clock, e.name, "started shift")
            print(clock, f.name, "started shift")
            print(clock, g.name, "started shift")
            print(clock, h.name, "started shift")
                    
        #Checks to see if it's the arrival time for the next customer, and determines the new arrival time customer after that.
        if clock.get_time() == customer_time:
            next_customer_time = 0
            while next_customer_time == 0:
                next_customer_time = next_time()

            customer_time = Clock.add_minutes(clock.get_time(), next_customer_time)
            
            #Adds the newest customer to the shop.
            if clock.get_time() != (9,0):
                customer = shop.add_customer(clock.get_time())

        #Checks if any of the barbers are available for a new customer each iteration, as well as checks if they've finished their haircut.
        shop.check_available(clock.get_time())
        shop.check_barbers(clock.get_time())
        
        #Checks to swap out the morning shift barbers if they went over-time for a customer
        if clock.get_time()[0] >= 13:
            for barb in starting_barbers:
                if barb in shop.barbers:
                    shop.end_shift(clock.get_time(), barb)
                    try:
                        shop.remove_barber(barb)
                    except:
                        pass

        #Increments the time
        clock.tick()

    #Checks to see which barbers can finish their shift once 5:00PM is reached
    for barb in switching_barbers:
                shop.end_shift(clock.get_time(), barb)
                try:
                    shop.remove_barber(barb)
                except:
                    pass

    #Closes shop if all haircuts finished at 5:00PM
    if shop.check_finished():
        print(clock, "Barber shop closed")

    #Loops until all of the remaining haircuts are finished
    while not shop.check_finished():
        if clock.get_time() == customer_time:
            next_customer_time = 0
            while next_customer_time == 0:
                next_customer_time = next_time()
            customer_time = Clock.add_minutes(clock.get_time(), next_customer_time)
            shop.add_customer(clock.get_time())


        shop.check_barbers(clock.get_time())
        for barb in switching_barbers:
            if barb in shop.barbers:
                shop.end_shift(clock.get_time(), barb)
                try:
                    shop.remove_barber(barb)
                except:
                    pass
        clock.tick()

    clock.reverse_tick()
    
    #Closes the barbershop for the day
    print(clock, "Barber shop closed")
    
    #Ends the shift of the last barber
    for barb in switching_barbers:
        if barb in shop.barbers:
                shop.end_shift(clock.get_time(), barb)
                
    #Sends the waiting customers home whose haircuts didn't start in time
    if len(shop.customers) > 0:
        for customer in shop.customers:
            print(clock, customer, "left", "furious")

if __name__ ==  "__main__":
    main()