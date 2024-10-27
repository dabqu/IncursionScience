import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from rooms import rooms

# List of all Tier 0 and Tier 1 room names for initial setup
t0_t1_rooms = [room.name for room in rooms.values() if room.tier == 0 or room.tier == 1]
t1_rooms = [room.name for room in rooms.values() if room.tier == 1]

def main():
    root = tk.Tk()
    root.title("Path of Exile Incursion Tracker")

    # Initialize variables
    entry_count = 0
    incursion_count = 0  # For tracking the number of incursions
    log_entries = []
    temple_state = {}  # Key: position (1 to 12), Value: Room instance
    position_to_room_name = {}  # Key: position, Value: room_name
    last_affected_position = None  # To keep track of the last affected room's position

    # Placeholder variables for the new widgets
    incursion_label = None
    room_entry = None
    upgrade_entry = None
    change_entry = None
    change_entry1 = None
    change_entry2 = None
    upgrade_button = None
    change_button = None
    change_button1 = None
    change_button2 = None
    atlas_upgrade_button = None
    upgrade_label = None
    change_label = None
    change_label1 = None
    change_label2 = None

    # Create a label and the autocomplete entry for initial setup
    label = tk.Label(root, text="Enter Initial Room Name:")
    label.pack(pady=5)

    room_names = t0_t1_rooms  # Include T0 and T1 rooms for initial setup
    entry = AutocompleteEntry(room_names, root, width=50)
    entry.pack(pady=5)
    entry.focus_set()  # Set focus to the initial room name field

    # Create a text widget to display output
    output_text = tk.Text(root, height=20, width=60, state='disabled', takefocus=0)
    output_text.pack(pady=5)

    # Add a bottom frame to add margin at the bottom
    bottom_frame = tk.Frame(root, height=20)
    bottom_frame.pack(side=tk.BOTTOM)

    # Tooltip instance
    tooltip = ToolTip(root)

    # Function to update controls based on selected room
    def update_controls(event):
        selected_room_name = room_entry.get()
        position = get_position_by_room_name(selected_room_name)
        clear_option_fields()
        remove_option_controls()
        if position:
            current_room = temple_state[position]
            if current_room.tier == 0:
                # Display Change Option 1 and Change Option 2
                create_change_controls_t0()
            else:
                # Display Upgrade Option and Change Option
                create_upgrade_controls(current_room)
                create_change_controls()
        else:
            remove_option_controls()

    # Function to create Upgrade Option controls
    def create_upgrade_controls(current_room):
        nonlocal upgrade_label, upgrade_entry, upgrade_button
        # Upgrade Option Entry
        upgrade_label = tk.Label(root, text="Upgrade Option:")
        upgrade_label.pack()
        upgrade_entry = tk.Entry(root, width=50)
        upgrade_entry.pack()
        if current_room.upgrades_to:
            upgrade_entry.insert(0, current_room.upgrades_to)
        # Bind tooltip to upgrade_entry
        upgrade_entry.bind("<Enter>", lambda e: show_tooltip(upgrade_entry))
        upgrade_entry.bind("<Leave>", lambda e: tooltip.hide_tooltip())
        upgrade_entry.bind("<KeyRelease>", lambda e: update_tooltip(upgrade_entry))
        # Upgrade Button
        upgrade_button = tk.Button(root, text="Upgrade", command=on_upgrade_click)
        upgrade_button.pack(pady=5)
        upgrade_button.bind('<Return>', lambda event: upgrade_button.invoke())

    # Function to create Change Option control for T1-T3 rooms
    def create_change_controls():
        nonlocal change_label, change_entry, change_button
        change_label = tk.Label(root, text="Change Option:")
        change_label.pack()
        change_entry = AutocompleteEntry(t1_rooms, root, width=50)
        change_entry.pack()
        # Bind tooltip to change_entry
        change_entry.bind("<Enter>", lambda e: show_tooltip(change_entry))
        change_entry.bind("<Leave>", lambda e: tooltip.hide_tooltip())
        change_entry.bind("<KeyRelease>", lambda e: update_tooltip(change_entry))
        # Change Button
        change_button = tk.Button(root, text="Change", command=on_change_click)
        change_button.pack(pady=5)
        change_button.bind('<Return>', lambda event: change_button.invoke())

    # Function to create Change Option controls for T0 rooms
    def create_change_controls_t0():
        nonlocal change_label1, change_entry1, change_label2, change_entry2, change_button1, change_button2
        change_label1 = tk.Label(root, text="Change Option 1:")
        change_label1.pack()
        change_entry1 = AutocompleteEntry(t1_rooms, root, width=50)
        change_entry1.pack()
        # Bind tooltip to change_entry1
        change_entry1.bind("<Enter>", lambda e: show_tooltip(change_entry1))
        change_entry1.bind("<Leave>", lambda e: tooltip.hide_tooltip())
        change_entry1.bind("<KeyRelease>", lambda e: update_tooltip(change_entry1))

        change_label2 = tk.Label(root, text="Change Option 2:")
        change_label2.pack()
        change_entry2 = AutocompleteEntry(t1_rooms, root, width=50)
        change_entry2.pack()
        # Bind tooltip to change_entry2
        change_entry2.bind("<Enter>", lambda e: show_tooltip(change_entry2))
        change_entry2.bind("<Leave>", lambda e: tooltip.hide_tooltip())
        change_entry2.bind("<KeyRelease>", lambda e: update_tooltip(change_entry2))

        # Change Buttons
        change_button1 = tk.Button(root, text="Change to Option 1", command=on_change_click_t0_option1)
        change_button1.pack(pady=5)
        change_button1.bind('<Return>', lambda event: change_button1.invoke())

        change_button2 = tk.Button(root, text="Change to Option 2", command=on_change_click_t0_option2)
        change_button2.pack(pady=5)
        change_button2.bind('<Return>', lambda event: change_button2.invoke())

    # Function to remove all option controls
    def remove_option_controls():
        # Remove Upgrade Option controls
        remove_upgrade_controls()
        # Remove Change Option controls
        remove_change_controls()
        # Remove Change Option controls for T0
        remove_change_controls_t0()

    def remove_upgrade_controls():
        nonlocal upgrade_label, upgrade_entry, upgrade_button
        if upgrade_label:
            upgrade_label.destroy()
            upgrade_label = None
        if upgrade_entry:
            upgrade_entry.destroy()
            upgrade_entry = None
        if upgrade_button:
            upgrade_button.destroy()
            upgrade_button = None

    def remove_change_controls():
        nonlocal change_label, change_entry, change_button
        if change_label:
            change_label.destroy()
            change_label = None
        if change_entry:
            change_entry.destroy()
            change_entry = None
        if change_button:
            change_button.destroy()
            change_button = None

    def remove_change_controls_t0():
        nonlocal change_label1, change_entry1, change_label2, change_entry2, change_button1, change_button2
        if change_label1:
            change_label1.destroy()
            change_label1 = None
        if change_entry1:
            change_entry1.destroy()
            change_entry1 = None
        if change_label2:
            change_label2.destroy()
            change_label2 = None
        if change_entry2:
            change_entry2.destroy()
            change_entry2 = None
        if change_button1:
            change_button1.destroy()
            change_button1 = None
        if change_button2:
            change_button2.destroy()
            change_button2 = None

    # Function to clear option fields when room selection changes
    def clear_option_fields():
        if upgrade_entry:
            upgrade_entry.delete(0, tk.END)
        if change_entry:
            change_entry.delete(0, tk.END)
        if change_entry1:
            change_entry1.delete(0, tk.END)
        if change_entry2:
            change_entry2.delete(0, tk.END)

    # Function to get position by room name
    def get_position_by_room_name(room_name):
        for pos, name in position_to_room_name.items():
            if name == room_name:
                return pos
        return None

    # Define the function to be called when the button is pressed
    def on_button_click():
        nonlocal entry_count
        room_name = entry.get()
        # Clear the entry field
        entry.delete(0, tk.END)

        if entry_count < 11:
            # Initial setup phase
            if room_name in t0_t1_rooms:
                entry_count += 1
                position = entry_count
                room_instance = rooms[room_name]
                temple_state[position] = room_instance
                position_to_room_name[position] = room_name
                log_entry = f"Initial Room {position}: {room_name}"
                insert_log(log_entry)
                log_entries.append(log_entry)
                if entry_count == 11:
                    insert_log("\nInitial setup completed. You can now handle incursions.\n")
                    # After initial setup, modify the GUI for incursion handling
                    setup_incursion_gui()
            else:
                insert_log(f"Invalid room: {room_name}")
                messagebox.showwarning("Invalid Room", f"'{room_name}' is not a valid room.")
        else:
            pass  # Should not happen

    # Function to set up the GUI for incursion handling
    def setup_incursion_gui():
        nonlocal incursion_label, room_entry, atlas_upgrade_button

        # Remove initial setup widgets
        label.pack_forget()
        entry.pack_forget()
        button.pack_forget()

        # Atlas Upgrade Button at the top
        atlas_upgrade_button = tk.Button(root, text="Atlas Upgraded", command=on_atlas_upgrade_click, state='disabled')
        atlas_upgrade_button.pack(pady=5)
        atlas_upgrade_button.bind('<Return>', lambda event: atlas_upgrade_button.invoke())

        # Incursion Handling Label
        incursion_label = tk.Label(root, text="Handle Incursion")
        incursion_label.pack(pady=5)

        # Room Entry
        room_label = tk.Label(root, text="Select Room:")
        room_label.pack()
        current_room_names = [name for name in position_to_room_name.values()]
        room_entry = AutocompleteEntry(current_room_names, root, width=50)
        room_entry.pack()
        room_entry.focus_set()  # Set focus to the "Select Room" field

        # Bind events
        room_entry.bind('<KeyRelease>', update_controls)

    # Function to handle upgrade action
    def on_upgrade_click():
        nonlocal log_entries, last_affected_position, incursion_count
        selected_room_name = room_entry.get()
        position = get_position_by_room_name(selected_room_name)
        if position and upgrade_entry and change_entry:
            current_room = temple_state[position]
            old_room_name = current_room.name

            upgrade_option = upgrade_entry.get()
            change_option = change_entry.get()

            actions_taken = []

            # Both Upgrade Option and Change Option must be valid
            if not upgrade_option or upgrade_option not in rooms:
                messagebox.showwarning("Invalid Upgrade Option", f"Invalid or empty Upgrade Option: '{upgrade_option}'")
                return
            if not change_option or change_option not in rooms:
                messagebox.showwarning("Invalid Change Option", f"Invalid or empty Change Option: '{change_option}'")
                return

            # Proceed with the action
            incursion_count += 1  # Increment incursion count

            # Perform Upgrade only
            upgraded_room = rooms[upgrade_option]
            temple_state[position] = upgraded_room
            position_to_room_name[position] = upgraded_room.name
            actions_taken.append(f"Upgraded {old_room_name} to {upgraded_room.name} (Tier {upgraded_room.tier}).")
            last_affected_position = position

            # Log the alternative Change Option
            actions_taken.append(f"Alternative Change Option was: {change_option}")

            # Update output and log
            result = "\n".join(actions_taken)
            incursion_header = f"Incursion {incursion_count}/12:"
            insert_log(f"{incursion_header}\n{result}\n")
            log_entries.append(f"{incursion_header}\n{result}")

            # Update room names in autocomplete entries
            current_room_names = [name for name in position_to_room_name.values()]
            room_entry.set_completion_list(current_room_names)

            # Clear entries and set focus back to room_entry
            room_entry.delete(0, tk.END)
            clear_option_fields()
            room_entry.focus_set()

            # Determine if Atlas Upgrade button should be enabled
            if last_affected_position is not None and temple_state[last_affected_position].upgrades_to:
                atlas_upgrade_button.config(state='normal')
            else:
                atlas_upgrade_button.config(state='disabled')

            # Remove option controls
            remove_option_controls()
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid room and provide both Upgrade and Change Options.")

    # Function to handle change action for T1-T3 rooms
    def on_change_click():
        nonlocal log_entries, last_affected_position, incursion_count
        selected_room_name = room_entry.get()
        position = get_position_by_room_name(selected_room_name)
        if position and upgrade_entry and change_entry:
            current_room = temple_state[position]
            old_room_name = current_room.name

            upgrade_option = upgrade_entry.get()
            change_option = change_entry.get()

            actions_taken = []

            # Both Upgrade Option and Change Option must be valid
            if not upgrade_option or upgrade_option not in rooms:
                messagebox.showwarning("Invalid Upgrade Option", f"Invalid or empty Upgrade Option: '{upgrade_option}'")
                return
            if not change_option or change_option not in rooms:
                messagebox.showwarning("Invalid Change Option", f"Invalid or empty Change Option: '{change_option}'")
                return

            # Proceed with the action
            incursion_count += 1  # Increment incursion count

            # Perform Change only
            changed_room = rooms[change_option]
            temple_state[position] = changed_room
            position_to_room_name[position] = changed_room.name
            actions_taken.append(f"Changed {old_room_name} to {changed_room.name} (Tier {changed_room.tier}).")
            last_affected_position = position

            # Log the alternative Upgrade Option
            actions_taken.append(f"Alternative Upgrade Option was: {upgrade_option}")

            # Update room names in autocomplete entries
            current_room_names = [name for name in position_to_room_name.values()]
            room_entry.set_completion_list(current_room_names)

            # Determine if Atlas Upgrade button should be enabled
            if changed_room.upgrades_to:
                atlas_upgrade_button.config(state='normal')
            else:
                atlas_upgrade_button.config(state='disabled')

            # Update output and log
            result = "\n".join(actions_taken)
            incursion_header = f"Incursion {incursion_count}/12:"
            insert_log(f"{incursion_header}\n{result}\n")
            log_entries.append(f"{incursion_header}\n{result}")

            # Clear entries and set focus back to room_entry
            room_entry.delete(0, tk.END)
            clear_option_fields()
            room_entry.focus_set()

            # Remove option controls
            remove_option_controls()
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid room and provide both Upgrade and Change Options.")

    # Functions to handle change actions for T0 rooms (Option 1 and Option 2)
    def on_change_click_t0_option1():
        on_change_click_t0(selected_option=1)

    def on_change_click_t0_option2():
        on_change_click_t0(selected_option=2)

    def on_change_click_t0(selected_option):
        nonlocal log_entries, last_affected_position, incursion_count
        selected_room_name = room_entry.get()
        position = get_position_by_room_name(selected_room_name)
        if position and change_entry1 and change_entry2:
            current_room = temple_state[position]
            old_room_name = current_room.name

            change_option1 = change_entry1.get()
            change_option2 = change_entry2.get()

            actions_taken = []

            # Both Change Options must be valid
            if not change_option1 or change_option1 not in rooms:
                messagebox.showwarning("Invalid Change Option", f"Invalid or empty Change Option 1: '{change_option1}'")
                return
            if not change_option2 or change_option2 not in rooms:
                messagebox.showwarning("Invalid Change Option", f"Invalid or empty Change Option 2: '{change_option2}'")
                return

            # Proceed with the action
            incursion_count += 1  # Increment incursion count

            # Determine which option was selected
            if selected_option == 1:
                chosen_option = change_option1
                alternative_option = change_option2
            else:
                chosen_option = change_option2
                alternative_option = change_option1

            # Perform Change with the chosen option
            changed_room = rooms[chosen_option]
            temple_state[position] = changed_room
            position_to_room_name[position] = changed_room.name
            actions_taken.append(f"Changed {old_room_name} to {changed_room.name} (Tier {changed_room.tier}).")
            last_affected_position = position

            # Log the alternative Change Option
            actions_taken.append(f"Alternative Change Option was: {alternative_option}")

            # Update output and log
            result = "\n".join(actions_taken)
            incursion_header = f"Incursion {incursion_count}/12:"
            insert_log(f"{incursion_header}\n{result}\n")
            log_entries.append(f"{incursion_header}\n{result}")

            # Update room names in autocomplete entries
            current_room_names = [name for name in position_to_room_name.values()]
            room_entry.set_completion_list(current_room_names)

            # Determine if Atlas Upgrade button should be enabled
            if changed_room.upgrades_to:
                atlas_upgrade_button.config(state='normal')
            else:
                atlas_upgrade_button.config(state='disabled')

            # Clear entries and set focus back to room_entry
            room_entry.delete(0, tk.END)
            clear_option_fields()
            room_entry.focus_set()

            # Remove option controls
            remove_option_controls()
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid room and provide both Change Options.")

    # Function to handle Atlas Upgraded action
    def on_atlas_upgrade_click():
        nonlocal log_entries, last_affected_position
        if last_affected_position is not None:
            current_room = temple_state[last_affected_position]
            old_room_name = current_room.name

            if current_room.upgrades_to:
                upgraded_room = rooms[current_room.upgrades_to]
                temple_state[last_affected_position] = upgraded_room
                position_to_room_name[last_affected_position] = upgraded_room.name
                result = f"Atlas Upgraded: {old_room_name} upgraded to {upgraded_room.name} (Tier {upgraded_room.tier})."
                insert_log(result + "\n")
                log_entries.append(f"Atlas Upgrade in Room {last_affected_position}:\n{result}")

                # Update room names in autocomplete entries
                current_room_names = [name for name in position_to_room_name.values()]
                room_entry.set_completion_list(current_room_names)

                # Update last affected position
                last_affected_position = last_affected_position

                # Determine if Atlas Upgrade button should remain enabled
                if temple_state[last_affected_position].upgrades_to:
                    atlas_upgrade_button.config(state='normal')
                else:
                    atlas_upgrade_button.config(state='disabled')
            else:
                result = f"Atlas Upgrade: {current_room.name} cannot be upgraded further."
                insert_log(result + "\n")
                log_entries.append(f"Atlas Upgrade in Room {last_affected_position}:\n{result}")
                atlas_upgrade_button.config(state='disabled')
        else:
            messagebox.showwarning("No Recent Action", "No recent action to apply Atlas Upgrade.")

    # Function to insert text into the log (read-only Text widget)
    def insert_log(text):
        output_text.config(state='normal')
        output_text.insert(tk.END, text + "\n")
        output_text.see(tk.END)  # Scroll to the bottom
        output_text.config(state='disabled')

    # Tooltip functions
    def show_tooltip(entry_widget):
        room_name = entry_widget.get()
        if room_name in rooms:
            room = rooms[room_name]
            rewards_text = f"Rewards:\n- " + "\n- ".join(room.rewards) if room.rewards else "No specific rewards."
            tooltip.show_tooltip(entry_widget, rewards_text)
        else:
            tooltip.hide_tooltip()

    def update_tooltip(entry_widget):
        # Update tooltip content based on current text
        show_tooltip(entry_widget)

    # Bind the Enter key to the entry widget
    def on_entry_return(event):
        if entry_count < 11:
            if not entry.listbox:
                on_button_click()
        else:
            pass  # No action needed; buttons handle actions now

    entry.bind('<Return>', on_entry_return)

    # Create the button
    button = tk.Button(root, text="Add Room", command=on_button_click)
    button.pack(pady=5)

    # Bind Enter key to the button when focused
    button.bind('<Return>', lambda event: button.invoke())

    # Function to write the log and close the application
    def on_closing():
        if log_entries:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/incursion_log_{current_time}.txt"
            with open(filename, 'w') as f:
                for entry in log_entries:
                    f.write(entry + "\n")
            print(f"Log saved to {filename}")
        root.destroy()

    # Bind the closing event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# Tooltip class
class ToolTip:
    def __init__(self, root):
        self.tipwindow = None
        self.root = root

    def show_tooltip(self, widget, text):
        "Display text in tooltip window"
        if self.tipwindow:
            self.tipwindow.destroy()
        x = widget.winfo_rootx() + widget.winfo_width() + 10  # Add some padding
        y = widget.winfo_rooty()
        self.tipwindow = tw = tk.Toplevel(widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# AutocompleteEntry class for the Entry widget with autocomplete
class AutocompleteEntry(tk.Entry):
    def __init__(self, autocomplete_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_list = sorted(autocomplete_list, key=str.lower)
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace("w", self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Tab>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-A>", self.select_all)
        self.listbox = None

    def set_completion_list(self, completion_list):
        self.autocomplete_list = sorted(completion_list, key=str.lower)

    def changed(self, name, index, mode):
        pattern = self.var.get()
        if pattern == '':
            if self.listbox:
                self.listbox.destroy()
                self.listbox = None
        else:
            matching_words = [w for w in self.autocomplete_list if w.lower().startswith(pattern.lower())]
            if matching_words:
                height = min(len(matching_words), 6)  # Limit the height to 6 items
                if not self.listbox:
                    self.listbox = tk.Listbox(width=self["width"])
                    self.listbox.bind("<Double-Button-1>", self.selection)
                    self.listbox.bind("<Return>", self.selection)
                    # Calculate position to avoid going off-screen
                    x = self.winfo_x()
                    y = self.winfo_y() + self.winfo_height()
                    self.listbox.place(x=x, y=y)
                    self.listbox.lift()
                self.listbox.delete(0, tk.END)
                for word in matching_words:
                    self.listbox.insert(tk.END, word)
                # Adjust the height of the listbox
                self.listbox.config(height=height)
            else:
                if self.listbox:
                    self.listbox.destroy()
                    self.listbox = None

    def selection(self, event):
        if self.listbox:
            selection = self.listbox.get(tk.ACTIVE)
            self.var.set(selection)
            self.listbox.destroy()
            self.listbox = None
            self.icursor(tk.END)
            return 'break'  # Prevent further event handling

    def move_up(self, event):
        if self.listbox:
            index = self.listbox.curselection()
            if index:
                index = index[0]
                if index > 0:
                    self.listbox.selection_clear(first=index)
                    index -= 1
                    self.listbox.selection_set(first=index)
                    self.listbox.activate(index)
            return 'break'

    def move_down(self, event):
        if self.listbox:
            index = self.listbox.curselection()
            if index:
                index = index[0]
                if index < self.listbox.size() - 1:
                    self.listbox.selection_clear(first=index)
                    index += 1
                    self.listbox.selection_set(first=index)
                    self.listbox.activate(index)
            else:
                self.listbox.selection_set(first=0)
                self.listbox.activate(0)
            return 'break'

    def select_all(self, event):
        self.select_range(0, tk.END)
        return 'break'

if __name__ == "__main__":
    main()
