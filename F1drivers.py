import csv
import os
import platform
import sys 
import time

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
        
#load Drivers
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

#Save
    def save_drivers_to_csv(self):
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            for driver in sorted(self.drivers, key=lambda x: x['Racing Number']):
                writer.writerow(driver)
        print("\n[ SYSYTEM UPDATED ]")

#Save And Exit
    def save_and_exit(self):
        print("\n" + "="*50)
        print("CLOSING THE PROGRAM & SAVING DATA")
        print("="*50)

        total_steps = 30
        
        for i in range(total_steps + 1):
            time.sleep(0.02)
            
            percent = (i / total_steps) * 100
            
            filled_length = int(total_steps * i // total_steps)
            bar = '█' * filled_length + '-' * (total_steps - filled_length)
            
            sys.stdout.write(f'\rProgress: |{bar}| {int(percent)}%')
            sys.stdout.flush()
        
        print("\n\nData saved successfully.")
        time.sleep(2) 
        clear_terminal()
        print("Program Closed.")
                       
#Show All Drivers
    def display_all_drivers(self):
        if not self.drivers:
            print("\nNo drivers found or file error.")
            return

        print("\n" + "="*120)
        print(f"{'No.':<5} {'Name':<20} {'Team':<15} {'Age':<5} {'Nat.':<15} {'Podiums':<8} {'GP Ent':<8} {'WC':<5} {'Career Pts':<12} {'Season Pts':<12}")
        print("="*120)

        for d in sorted(self.drivers, key=lambda x: (x.get('Team', '').lower(), x.get('Racing Number', 0))):
            print(f"{d['Racing Number']:<5} "
                  f"{d['Name']:<20} "
                  f"{d['Team']:<15} "
                  f"{d['Age']:<5} "
                  f"{d['Nationality']:<15} "
                  f"{d['Podiums']:<8} "
                  f"{d['GP Entered']:<8} "
                  f"{d['World Championships']:<5} "
                  f"{d['Career Points']:<12.1f} "
                  f"{d['Current Season Points']:<12.1f}")
        print("="*120)

        total = len(self.drivers)
        print(f"[ SYSTEM STATUS ] Total Drivers Listed: {total} Drivers")
        print("=" * 120 + "\n")
        
#Add Driver
    def add_new_driver(self):
        print("\n--- ADD NEW DRIVER ---")
        try:
            r_num = int(input("1. Racing Number: "))
            if any(d['Racing Number'] == r_num for d in self.drivers):
                print(f"\nERROR: Racing Number {r_num} already exists.")
                return
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

            self.drivers.append(new_driver)
            self.save_drivers_to_csv()
            print(f"\nAdded New Driver: #{r_num} {name}! (saved)")
            
        except ValueError:
            print("\nERROR: Please enter numbers for Age, Points, etc.")
            
#Delete Driver
    def delete_driver(self):
        print('\n--- DELETE DRIVER ---')
        try:
            r_num = input('Enter Racing Number of driver to delete (or leave blank to cancel): ').strip()
            if not r_num:
                print('Delete cancelled.')
                return
            r_num = int(r_num)
        except ValueError:
            print('Invalid racing number.')
            return

        # find driver
        for i, d in enumerate(self.drivers):
            if d.get('Racing Number') == r_num:
                print(f"Found: #{d['Racing Number']} {d['Name']} ({d['Team']})")
                confirm = input('Confirm deletion(Y/N): ').strip()
                if confirm.upper() == 'Y':
                    self.drivers.pop(i)
                    self.save_drivers_to_csv()
                    print(f'Driver #{r_num} deleted and changes saved.')
                elif confirm.upper() == 'N':
                    print('Deletion cancelled.')
                else:
                    print('Deletion cancelled.')
                return

        print(f'No driver found with Racing Number {r_num}.')  
                   
#Search Driver   
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

#Edit Driver
    def edit_driver(self):
        print("\n--- EDIT DRIVER DATA ---")
        try:
            target_id = int(input("Enter Racing Number of the driver to edit: "))
        except ValueError:
            print("Error: Racing Number must be a number.")
            return

        target_driver = None
        for d in self.drivers:
            if d['Racing Number'] == target_id:
                target_driver = d
                break
        
        if not target_driver:
            print(f"Driver #{target_id} not found.")
            return
        
        print(f"\nEditing: {target_driver['Name']} (Currently in {target_driver['Team']})")
        print("1. Team")
        print("2. Current Season Points")
        print("3. Age")
        print("4. Total Podiums")
        print("5. World Championships")
        print("6. Cancel")

        choice = input("Enter your choice (1-6): ")

        fields = {
            '1': ('Team', str, 'Team'),
            '2': ('Current Season Points', float, 'Current Season Points'),
            '3': ('Age', int, 'Age'),
            '4': ('Total Podiums', int, 'Podiums'),
            '5': ('World Championships', int, 'World Championships')
        }

        if choice == '6':
            print("Edit cancelled.")
            return
        
        if choice not in fields:
            print("Invalid selection.")
            return

        try:
            field_name, field_type, key = fields[choice]
            current_val = target_driver[key]
            
            if field_type == str:
                new_val = input(f"Enter new {field_name} (Current: {current_val}): ").strip()
            else:
                new_val = field_type(input(f"Enter new {field_name} (Current: {current_val}): "))
            
            target_driver[key] = new_val
            self.save_drivers_to_csv()
            print(f"Success! {field_name} for {target_driver['Name']} has been updated.")

        except ValueError:
            print("Error: Invalid input format.")
            
#Driver Standing
    def driver_standing(self):
        print("\n--- TOP 5 DRIVER STANDING ---")
        print("")
        self.drivers.sort(key=lambda x: x["Current Season Points"], reverse=True)
        top_5 = self.drivers[:5]

        for rank, driver in enumerate(top_5, 1):
            print(f"{rank}. #{driver['Racing Number']:<5} {driver['Name']} ({driver['Team']}) - {driver['Current Season Points']} Pts")

#Driver Manager Menu    
    def driver_manager_menu(self):
        while True:
            print("\n--- ADD/Edit/Delete DRIVERS ---")
            print("1. Add Driver")
            print("2. Delete Driver")
            print("3. Edit Driver")
            print("4. Return to Main Menu")
            print("-" * 32)
        
            c = input("Choice: ")
            if c == '1':
                self.add_new_driver()
            elif c == '2':
                self.delete_driver()
            elif c == '3':
                self.edit_driver()
            elif c == '4':
                return
            else:
                print("\n" + "Invalid choice. Please select a valid option.")

#Main Menu
def main():
    app = F1Manager()
    while True:
        print("\n--- FORMULA1 DRIVERS MANAGER ---")
        print("1. Show All Drivers")
        print("2. Driver Manager Menu")
        print("3. Search Driver")
        print("4. Driver Standing")
        print("5. Save And Exit")
        print("-" * 32)
        
        c = input("Choice: ")
        if c == '1':
            app.display_all_drivers()
        elif c == '2':
            app.driver_manager_menu()
        elif c == '3':
            app.search_driver()
        elif c == '4':
            app.driver_standing()
        elif c == '5':
            app.save_drivers_to_csv()
            app.save_and_exit()
            break
        else:
            print("\n" + "Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()