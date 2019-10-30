# barbershop
This repository showcases a coding challenge I did with a two-hour time limit. The entire solution I came up with is in the barber_shop.py file.

## Problem Overview

### Goal
The task is to simulate a men's barber shop.

### Rules
The barber shop is open for 8 hours, from 9am to 5pm. You don't want your program to take that long to run, so you'll need to somehow simulate real time.

When the shop opens, there are 4 barbers who start their shift:
Alto, Basil, Camphor, and Diogenes.

On average, a new customer enters once every ten minutes. Their arrivals are random. Customers are named successively starting at Customer-1. The shop can only hold 15 total customers; if a customer arrives when the shop is full, they leave impatiently.

Otherwise, the client waits for a barber. A barber can only cut one person's hair at a time, and takes between 20 and 40 minutes to do so. After a barber is done with a customer, the customer leaves satisfied.

A customer will wait up to 30 minutes for a free barber; if time's up and none can be found, the customer leaves unfulfilled.

Barbers work 4 hour shifts, so the first shift of barbers is allowed to go home at 1pm. They end their shift as soon as they can, unless they busy with a client. In that case, they wait until they finish that client, and then end their shift.

At 1pm, the second shift of barbers starts: Eros, Fatoush, Glorio, and Heber. They also work a 4 hour shift, and can go home after 5pm. Like the morning shift, if they're busy with a customer, they need to finish up before leaving.

A customer who enters after 5pm is turned away, and leaves cursing himself.

When all the barbers and customers have gone home, the shop closes. If there are any customers left waiting for a barber, they are kicked out, and leave furious.

### Output
Your program should print the below events in chronological order.  [Time] is barbershop-time in the format HH:MM, not real time.

[Time] Barber shop [opened/closed]
[Time] [Barber] [started/ended] shift
[Time] [Customer] entered
[Time] [Customer] left [impatiently/satisfied/unfulfilled/cursing himself/furious]
[Time] [Barber] [started/ended] cutting [Customer]'s hair

