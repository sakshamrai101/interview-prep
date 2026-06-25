# HOTEL RESERVATION (Concurrency & Control)

"""
Questions to ask:
- What is the scale of the problem? ("Are we designing for a small motel with 100 rooms or booking.com with millions of rooms)
- How are rooms represented ? ("Do people book specific room number like 302 or a 'room-type' like 'Deluxe King' from a pool of inventory?")
- What is the read/write ratio ? ("eg. are millions of people just browsing rooms vs. thousands making actual bookings. This shows we are already thinkning about scale later")
"""

"""

We will use ACID transactions for database updates. 
- Pretty much the std for finance and banking systems -> a single business action often requires multiple updates to db:

    A: Deduct 100$ from account A
    B: Add 100$ to account B 

    Here if server crashes exactly halfway through, the 100$ is lost. 
    To prevent this, database use TRANSACTIONS, governed by acid properties to gurantee that your data remains accurate. 

    1. A: Atomicity ("All or Nothing"): Entire transaction is treated as a single, indivisible unit of work. Either ALL steps succeed.
    or the entire thing is aborted ("rolled back") 

    2. C: Consistency: A transaction can only bring the database from one valid state to another, maintaining all schema rules, constraints and data types. For example,
    a balance cannot contain a text string and drop below a set minimum balance constraint.

    3. I - Isolation (The concurrency guard): This ensures concurrent transactions (1000s of people booking hotel rooms at the same time) do not cross wires or read modifed data
    from each other, until they are fully finished. It makes concurrent executions behave as if they are fully finished. It makes concurrent transactions behave as though they are running sequentially.

    4. D - Durability: Once transaction is committed, it is written permanently to a non-volatile storage (hard drive, ssd). Even if the entire data center loses power a millisecond later, 
    the data is completely safe and won't be lost. 
- 
"""

# How a db guarantees Atomicity and Isolation 
# BEGIN TRANSACTION;

# 1. Check inventory with a pessimistic lock (Isolation)
# SELECT total_inventory FROM room_types WHERE id = 'deluxe_king' FOR UPDATE;

# 2. Insert the record if available. 
# INSERT INTO bookings (user_id, room_type_id, status) VALUES (101, 'deluxe_king', 'CONFIRMED');

# If any step fails or inventory is 0, we roll back.
# If everything succeeds, we save it. 
# COMMIT;

import threading
import datetime 

class RampHotelSystem:

    def __init__(self):

        # Maps room_type_id -> no. of such rooms 
        self.room_inventory = {
            "deluxe_king": 3,
            "standard_twin" : 5
        }

        # Simple list of dictionary records representing active bookings
        self.bookings = []
    
    def get_available_inventory(self, room_type_id, check_in, check_out):
        """
        Helper method to calculate how many rooms of a specific type are remaining 
        for a given date range. 

        """

        # We start with maximum physical capacity of the hotel 
        total_rooms = self.room_inventory.get(room_type_id, 0)

        # Count how many bookings overlap with this new request 
        overlapping_booking = 0
        for b in self.bookings:
            if b["room_type_id"] == room_type_id and b["status"] == "CONFIRMED":
                # Check for date overlap condition:
                # A booking overlaps if it starts before the new check_out 
                # AND ends after the new check_in
                if b["check_in"] < check_out  and b["check_out"] > check_in:
                    overlapping_booking +=1
        
        return total_rooms - overlapping_booking
    
    def book_room_naive(self, user_id, room_type_id, check_in_str, check_out_str):
        """
        Phase 2: Std. implementation.
        Parses data strings, verifies inventory, and appends a booking record. 

        """
        # Defensive parsing of data strings into datetime objects 
        try:
            check_in = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.datetime.strptime(check_out_str,'%Y-%m-%d').date()
        except ValueError:
            print(f"[API ERROR] Invalid date format. Use YYYY-MM-DD")
            return {"status": "REJECTED", "message": "Invalid date strings"}
        
        if check_in >= check_out:
            return {"status": "REJECTED", "messsage": "Invalid date strings"}
        
        # Check remaining capacity 
        available_rooms = self.get_available_inventory(room_type_id, check_in, check_out)
        print(f"[INFO] Checking inventory for {room_type_id}: {available_rooms} rooms available.")

        if available_rooms > 0:
            # Create the booking record:
            new_booking = {
                "booking_id": f"bk_{len(self.bookings) + 1}",
                "user_id": user_id,
                "room_type_id": room_type_id,
                "check_in": check_in,
                "check_out": check_out,
                "status": "CONFIRMED"
            }

            self.bookings.append(new_booking)
            print(f"[SUCCESS] Booking {new_booking['booking_id']} confirmed for User {user_id}.")
            return {"status": "CONFIRMED", "booking_id": new_booking["booking_id"]}

        
        print(f"[REJECTED] No inventory left for {room_type_id}.")
        return {"status": "REJECTED", "message": "Sold out"}

if __name__ == "__main__":
    hotel = RampHotelSystem()
    
    print("--- FIRST USER REQUEST: SINGLE ROOM LEFT ---")
    # Hotel only has 3 'deluxe_king' rooms total
    res1 = hotel.book_room_naive(101, "deluxe_king", "2026-07-01", "2026-07-05")
    res2 = hotel.book_room_naive(102, "deluxe_king", "2026-07-01", "2026-07-05")
    res3 = hotel.book_room_naive(103, "deluxe_king", "2026-07-01", "2026-07-05")
    
    print(f"Booking 1: {res1['status']}")
    print(f"Booking 2: {res2['status']}")
    print(f"Booking 3: {res3['status']}")
    
    print("\n--- FORCING THE FOURTH BOOKING (SOLD OUT BOUNDARY) ---")
    # This should be rejected safely because all 3 physical rooms are booked for these dates
    res4 = hotel.book_room_naive(104, "deluxe_king", "2026-07-01", "2026-07-05")
    print(f"Booking 4 Result: {res4['status']} | Message: {res4.get('message', 'N/A')}")


