"""

Multi-tiered LRU CACHE Layer

Let's move to core infrastructure. When a user requests their dashboard data at Ramp, 
making a direct disk database call every single time is far too slow. We use an in-memory cache.

Your task is to design an in-memory Multi-Tiered Least Recently Used (LRU) Cache. 
Your cache engine must enforce a strict maximum capacity limit. 
If a user inserts an item that pushes the cache over capacity, you must automatically evict the Least Recently Used item. 
When an item is updated or read, its priority must instantly refresh to make it the Most Recently Used item."

"""

class Node:

    """
    Block representing DLL.
    Stores the key, actual value payload, and pointers to neighbouring nodes. 

    """

    def __init__(self, key: str, value: any):
        self.key = key
        self.value = value
        self.prev = None # ptr to preceeding item in the timeline chain
        self.next = None # ptr to succeeding item in the timeline chain 

class TieredLRUCache:

    def __init__(self, capacity: int):
        # 1. Store the hard limit configuration capacity boundary 
        self.capacity = capacity

        # 2. Primary lookup index map. Maps: { key -> Node Object Pointer }
        self.cache = {}

        # 3. Sentinal Dummy Head and Tail Node (to avoid null ptr check)
        # Head represents MRU.
        # Tail represents LRU.
        self.head = Node("dummy_head", None)
        self.tail = Node("dummy_tail", None)

        # Wire them together 
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- Mutation Operations ---

    def add_to_front(self, node: Node) -> None:
        """
        Inserts a target node immediately behind the dummy head placeholder,
        marking it as the absolute MOST RECENTLY USED (MRU) element

        """
        # Save the current real first element to be used 
        current_first = self.head.next

        # Splice the new node into position between Head and current_first 
        self.head.next = node
        node.prev = self.head
        node.next = current_first
        current_first.prev = node
    
    def _remove_node(self, node: Node) -> None:
        """
        Exctracts an existing node out from its current location in the 
        linked list chain by re-routing its neihbours' forward and backward pointers around it.

        """

        # Link the neighbour directly to each other, cutting out the target node reference entirely 
        previous_guy = node.prev
        next_guy = node.next

        previous_guy.next = next_guy
        next_guy.prev = previous_guy

    
    def _refresh_priority(self, node: Node) -> None:
        """
        Retrieves a value out from the chache index in O(1) time.
        Refreshes its timeline usage position if it exists. 

        """
        self._remove_node(node)
        self.add_to_front(node)

    def get(self, key: str) -> any:
        """
        Retrieves a value out from the cache index in O(1) time. 
        Refreshes its timeline usage position if it exists.
        """
        
        if key not in self.cache:
            return None # cache miss
        
        # cache hit! extract the node pointer address out from our mapping index 
        target_node = self.cache[key]

        # Update usage chronologically track record 
        self._refresh_priority(target_node)
        return target_node.value 
    
    def put(self, key: Node, value: any) -> None:
        """
        Upserts an element payload. If insertion forces memory size past capacity limits,
        the element located at tail is permanently deleted (LRU).

        """
        # Case A: Key already exists in cache index. Update value and shift to front.
        if key in self.cache:
            existing_node = self.cache[key]
            existing_node.value = value 
            self._refresh_priority(existing_node)
            return 
        
        # Case B: Brand new key arrival. Check capacity limits before insertion 
        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            print(f"   [EVICTION TRIGGERED] Cache at capacity limit! Evicting key: '{lru_node.key}'")

            # Wipe references from both link list chain and our index mapping dict
            self._remove_node(lru_node)
            del self.cache[lru_node.key]
        
        # Construct a brand new isolated Node allocation block 
        new_node = Node(key, value)

        # Add stuctural memory indices and list chains 
        self.cache[key] = new_node
        self.add_to_front(new_node)



if __name__ == "__main__":
    # Initialize an ultra-tight cache that can only hold 2 items maximum
    lru = TieredLRUCache(capacity=2)
    print("--------- Testing Low-Level LRU Cache Infrastructure ---------")

    # Day 0: Insert user dashboard profiles
    lru.put("user_101", "Saksham_Data")
    lru.put("user_102", "Disha_Data")
    
    # Read user_101. This access instantly makes user_101 the MOST recently used,
    # pushing user_102 down to the vulnerable LEAST recently used eviction slot!
    print(f"Reading user_101: {lru.get('user_101')}") 
    assert lru.get("user_101") == "Saksham_Data"

    # Insert a 3rd user profile. This pushes the cache over its capacity of 2!
    # Because user_101 was refreshed recently, user_102 is the old item that gets evicted!
    lru.put("user_103", "Bob_Data")

    # Verify eviction results
    print(f"Querying user_102 (Evicted): {lru.get('user_102')}") # Expected: None
    print(f"Querying user_101 (Preserved): {lru.get('user_101')}") # Expected: Saksham_Data
    
    assert lru.get("user_102") is None
    assert lru.get("user_101") == "Saksham_Data"
    print(" ✅ Cache eviction chronology and index tracking validated successfully.")

    # Overwrite an existing item's value and refresh its priority tier position
    lru.put("user_103", "Updated_Bob_Data")
    assert lru.get("user_103") == "Updated_Bob_Data"

    print("\n🚀 [SYSTEM SUCCESS] Problem 3 cleared! You are building pure infrastructure speed, bro. Drop a line when you're ready for Problem 4!")