import csv
import os
import platform

def clear_terminal():
    system_name = platform.system()
    if system_name == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class F1Manager:
    def __init__(self):
        self.file_name = "drivers.csv"
        self.headers = [
            "Racing Number", "Name", "Team", "Age", "Nationality",
            "Podiums", "GP Entered", "World Championships",
            "Career Points", "Current Season Points"
        ]
        self.drivers = []
        self.load_drivers_from_csv()
        
#0.1 Load Drivers
    def load_drivers_from_csv(self):
        if not os.path.exists(self.file_name):
            print(f"Warning: {self.file_name} not found. A new one will be created when you Add a Driver.")
            return

        with open(self.file_name, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    row['Racing Number'] = int(row['Racing Number'])
                    row['Age'] = int(row['Age'])
                    row['Podiums'] = int(row['Podiums'])
                    row['GP Entered'] = int(row['GP Entered'])
                    row['World Championships'] = int(row['World Championships'])
                    row['Career Points'] = float(row['Career Points'])
                    row['Current Season Points'] = float(row['Current Season Points'])
                    
                    self.drivers.append(row)
                except (ValueError, KeyError):
                    continue 
#0.2 Save Drivers
    def save_drivers_to_csv(self):
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            for driver in sorted(self.drivers, key=lambda x: x['Racing Number']):
                writer.writerow(driver)
        print("\n[ SYSTEM STATUS ] All changes have been saved to the file.")
                
#1. Show All Drivers
    def display_all_drivers(self):
        if not self.drivers:
            print("\nNo drivers found or file error.")
            return

        print("\n" + "="*80)
        print(f"{'No.':<5} {'Name':<20} {'Team':<18} {'Nat.':<15} {'Age':<5} {'Pts':<12}")
        print("="*80)

        for d in self.drivers:
            print(f"{d['Racing Number']:<5} "
                  f"{d['Name']:<20} "
                  f"{d['Team']:<18} "
                  f"{d['Nationality']:<15} "
                  f"{d['Age']:<5} "
                  f"{d['Current Season Points']:<12}")
        print("="*80)
        
        total = len(self.drivers)
        print(f"[ SYSTEM STATUS ] Total Drivers Listed: {total} Drivers")
        print("=" * 80 + "\n")
        
#2. Add Driver
    def add_new_driver(self):
        print("\n--- ADD NEW DRIVER ---")
        try:
            r_num = int(input("1. Racing Number: "))
            name = input("2. Driver Name: ").strip()
            team = input("3. Team Name: ").strip()
            age = int(input("4. Age: "))
            nat = input("5. Nationality: ").strip()
            podiums = int(input("6. Total Podiums: "))
            gp_ent = int(input("7. GP Entered: "))
            wc = int(input("8. World Championships: "))
            career_pts = float(input("9. Career Points: "))
            season_pts = float(input("10. Current Season Points: "))

            new_driver = {
                "Racing Number": r_num,
                "Name": name,
                "Team": team,
                "Age": age,
                "Nationality": nat,
                "Podiums": podiums,
                "GP Entered": gp_ent,
                "World Championships": wc,
                "Career Points": career_pts,
                "Current Season Points": season_pts
            }
            
            print(f"\nAdded New Driver: #{r_num} {name}!")
            
        except ValueError:
            print("\nERROR: Please enter numbers for Age, Points, etc.")
             
#3. Search Driver   
    def search_driver(self):
        print("\n--- SEARCH DRIVER ---")
        query = input("Enter Name or Team: ").lower()
        found = False
        for d in self.drivers:
            if query in d['Name'].lower() or query in d['Team'].lower():
                print("")
                print(f"Found: #{d['Racing Number']} {d['Name']} ({d['Team']}) - Points: {d['Current Season Points']}")
                found = True
        if not found:
            print("No match found.")

#4. Driver Standing
    def driver_standing(self):
        print("\n--- TOP 5 DRIVER STANDING ---")
        print("")
        self.drivers.sort(key=lambda x: x["Current Season Points"], reverse=True)
        top_5 = self.drivers[:5]

        for rank, driver in enumerate(top_5, 1):
            print(f"{rank}. #{driver['Racing Number']:<5} {driver['Name']} ({driver['Team']}) - {driver['Current Season Points']} Pts")
      
#5. Main Menu
def main():
    app = F1Manager()
    while True:
        
        print("\n--- FORMULA1 DRIVERS MANAGER ---")
        print("1. Show All Drivers")
        print("2. Add Driver")
        print("3. Search Driver")
        print("4. Driver Standing")
        print("5. Save And Exit")
        print("-" * 32)
        
        c = input("Choice: ")
        if c == '1': app.display_all_drivers()
        elif c == '2': app.add_new_driver()
        elif c == '3': app.search_driver()
        elif c == '4': app.driver_standing()
        elif c == '5': 
            app.save_drivers_to_csv()
            clear_terminal()
            print ("All changes have been saved to the file.")
            print ("Program Closed!")
            break
        else:
            print("\n" + "Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
