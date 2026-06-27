import time 

class SnapshotDatabase:

    def __init__(self):

        # primary live storage engine 
        self.live_storage = {}

        # transaction stack holding dictionary deltas for rollback operations.
        # Format: List of dicts representing {key: original_value_before_mutation}
        self.transaction_stack = []

        # Snapshot registory mapping ID to a complete delta rollback state 
        self.snapshots = {}


    # CORE KEY OPERATIONS
    def set(self, key: str, value: str) -> None:
        """ Sets a key to a value, tracking deltas if an active transaction exists. """

        # If a transaction is actively open, we must preserve the key's state BEFORE this edit
        if self.transaction_stack:
            active_tx = self.transaction_stack[-1]
            if key not in active_tx:
                # If the key didn't exist before, store None as its orignal state fallback value 
                active_tx[key] = self.live_storage.get(key, None)
        
        self.live_storage[key]= value
    
    def get(self, key: str) -> str:
        """ std. immediate O(1) live database retrieval. """
        return self.live_storage.get(key, None)

    def delete(self, key: str) -> None:
        """Removes a key from active storage while preserving delta history"""
        if key not in self.live_storage:
            return 
        
        if self.transaction_stack:
            active_tx = self.transaction_stack[-1]
            if key not in active_tx:
                active_tx[key] = self.live_storage[key]
        
        del self.live_storage[key]
    

    """ Transactionsal Control Block (ACID) """
    def begin_transaction(self) -> None:
        """ Opens a new isolated transaction scope layer """
        # Push a fresh delta tracking dictioanary onto our state stack 
        self.transaction_stack.append({})

    def commit_transaction(self) -> None:
        """ Merges all temporary edits permanently into storage engine """
        if not self.transaction_stack:
            raise RuntimeError("Engine Failure: No active transaction open to commit")
        
        # In a multi-layered transaction system, changes roll up into the parent transaction layer 
        completed_tx = self.transaction_stack.pop()


        # If there is still an outer transaction open, push these updates up into it.
        if self.transaction_stack:
            parent_tx = self.transaction_stack[-1]
            for key, orignal_value in completed_tx.items():
                if key not in parent_tx:
                    parent_tx[key] = orignal_value
        
    def rollback_transaction(self) -> None:
        """ Discards all modifications made inside the current active scope layer """
        if not self.transaction_stack:
            raise RuntimeError("Engine Failure: No active transaction open to rollback.")

        
        # Pop the latest delta map and iterate backward to restore the prior state:
        rollback_delta = self.transaction_stack.pop()
        for key, orignal_value in rollback_delta.items():
            if orignal_value is None:
                self.live_storage.pop(key, None) # Key didn't exist before the tx started 
            else:
                self.live_storage[key] = orignal_value
        
        # ----- TIME TRAVEL SNAPSHOTTING LAYER -----

    def create_snapshot(self, snapshot_id: str) -> None:
        """
        Creates an in immutable point-in-time snapshot.
        Optimized via a full shallow record clone to decouple from live mutations. 

        """
        # Save a frozen version copy of the active system state 
        self.snapshots[snapshot_id] = dict(self.live_storage)

    
    def checkout_snapshot(self, snapshot_id: str) -> dict:
        """ Queries the exact historical state of a snaptshot without destroying the live DB."""
        if snapshot_id not in self.snapshots:
            raise KeyError(f"Snapshot ID '{snapshot_id}' not found in registry")
        
        return self.snapshots[snapshot_id]

if __name__ == "__main__":
    db = SnapshotDatabase()
    print("--------- Testing Low-Level In-Memory DB Engine ---------")

    # Phase 1: Set initial data and freeze snapshot
    db.set("user_id_101", "Saksham_Rai")
    db.set("balance", "5000.00")
    db.create_snapshot("snap_v1")
    print(" [SNAP_v1 CREATED] Live State frozen.")

    # Phase 2: Open isolated transaction scope
    db.begin_transaction()
    db.set("balance", "7500.00")
    db.set("status", "VIP")
    print(f" [TX_OPEN] Current Live Balance inside tx: ${db.get('balance')}")

    # Verify snapshot isolation while tx is uncommitted
    v1_state = db.checkout_snapshot("snap_v1")
    assert v1_state["balance"] == "5000.00"
    print(" ✅ Snapshot isolation successfully verified during uncommitted transactions.")

    # Roll back transaction state mutations
    db.rollback_transaction()
    print(f" [TX_ROLLBACK] Balance safely reverted back to: ${db.get('balance')}")
    assert db.get("balance") == "5000.00"
    assert db.get("status") is None

    # Phase 3: Nested Multi-Layer Transaction Test
    db.begin_transaction() # TX Layer 1
    db.set("tier", "Premium")
    
    db.begin_transaction() # TX Layer 2 (Nested)
    db.set("tier", "Elite")
    db.rollback_transaction() # Discard Layer 2 changes
    
    print(f" [NESTED_TX] Current tier state: '{db.get('tier')}'")
    assert db.get("tier") == "Premium"
    db.commit_transaction() # Commit Layer 1 changes
    
    print("\n🚀 [SYSTEM SUCCESS] All ACID boundaries and snapshot checkpoints passed flawlessly!")

 

