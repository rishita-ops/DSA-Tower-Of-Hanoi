num_disks = int(input("Enter the number of disks: "))

total_moves = 2**num_disks - 1

print(f"\nTotal moves required: {total_moves}\n")

for move in range(1, total_moves + 1):
    disk = 1
    temp_move = move
    while temp_move % 2 == 0:
        disk += 1
        temp_move //= 2
        
    source_idx = (move & (move - 1)) % 3
    dest_idx = ((move | (move - 1)) + 1) % 3
    
    rods = ["A", "B", "C"]
    
    if num_disks % 2 == 0:
        if rods[source_idx] == "B":
            from_rod = "C"
        elif rods[source_idx] == "C":
            from_rod = "B"
        else:
            from_rod = "A"
            
        if rods[dest_idx] == "B":
            to_rod = "C"
        elif rods[dest_idx] == "C":
            to_rod = "B"
        else:
            to_rod = "A"
    else:
        from_rod = rods[source_idx]
        to_rod = rods[dest_idx]
        
    print(f"Move #{move}: Move disk {disk} from Rod {from_rod} to Rod {to_rod}")

print("\nAll disks have been successfully moved!")
