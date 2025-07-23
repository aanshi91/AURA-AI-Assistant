# from tkinter import *
# from PIL import Image, ImageTk
# import speech_to_text
# import action


# root = Tk()
# root.title("AI Assistant")
# # Removed root.geometry and root.resizable to allow dynamic centering
# root.config(bg="#cdc4e3")

# # Function definitions (unchanged)
# def ask():
#      user_val = speech_to_text.speech_to_text()
#      bot_val = action.Action(user_val)
#      text.insert(END , 'User---->'+ user_val+"\n")
#      if bot_val != None:
#          text.insert(END,"BOT <---"+str(bot_val)+"\n")
#      if bot_val == "ok sir" :
#          root.destroy()

    
# def send():
#     send = entry.get()
#     bot = action.Action(send)
#     text.insert(END , 'User---->'+ send+"\n")
#     if bot != None:
#          text.insert(END,"BOT <---"+str(bot)+"\n")
#     if bot == "ok sir" :
#          root.destroy()



# def delete():
#     text.delete("1.0","end")

# # Create a main frame to hold all content and center it
# # We'll use grid's columnconfigure and rowconfigure to center this frame
# main_frame = Frame(root, bg="#cdc4e3")
# main_frame.grid(row=0, column=0, sticky="nsew") # Make it expand to fill root

# # Configure root rows and columns to center main_frame
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=1)

# # AI Assistant Title Label
# text_label = Label(main_frame, text="AI Assistant", font=("comic Sans ms", 14), bg="purple", fg="white") # Added foreground color for better contrast
# text_label.pack(pady=10) # Using pack for simpler vertical layout within main_frame

# # Image
# try:
#     # Ensure "mic.jpg" is in the same directory as your script, or provide a full path
#     image_path = "mic.jpg" # Replace with the actual path to your image if not in the same directory
#     image = ImageTk.PhotoImage(Image.open(image_path))
#     image_label = Label(main_frame, image=image)
#     image_label.image = image # Keep a reference to prevent garbage collection
#     image_label.pack(pady=10)
# except FileNotFoundError:
#     error_label = Label(main_frame, text="Error: mic.jpg not found. Please ensure the image is in the correct directory.", fg="red")
#     error_label.pack(pady=10)


# # Text Widget
# # Use a sub-frame for the text widget and entry to better control their layout together
# input_frame = Frame(main_frame, bg="#cdc4e3")
# input_frame.pack(pady=10)

# text = Text(input_frame, font=('courier 10 bold'), bg="pink", height=6, width=45) # Set initial height/width
# text.pack(pady=5)

# # Entry Widget
# entry = Entry(input_frame, justify=CENTER, width=50) # Set initial width
# entry.pack(pady=5)

# # Buttons Frame
# button_frame = Frame(main_frame, bg="#cdc4e3")
# button_frame.pack(pady=20) # Add padding below the input elements

# # Button 1 (ASK)
# Button1 = Button(button_frame, text="ASK", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=ask)
# Button1.grid(row=0, column=0, padx=10)

# # Button 3 (DELETE) - Placed in the middle column
# Button3 = Button(button_frame, text="DELETE", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=delete)
# Button3.grid(row=0, column=1, padx=10)

# # Button 2 (SEND)
# Button2 = Button(button_frame, text="SEND", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=send)
# Button2.grid(row=0, column=2, padx=10)


# root.mainloop()



#update code-


from tkinter import *
from PIL import Image, ImageTk
import speech_to_text
import text_to_speech
import action
import database_manager # Import the database manager
import datetime # Needed for reminder check

root = Tk()
root.title("AI Assistant")
root.config(bg="#cdc4e3")

# Function definitions
def ask():
    user_val = speech_to_text.speech_to_text()
    if user_val: # Only proceed if speech was recognized
        bot_val = action.Action(user_val)
        text.insert(END, 'User---->' + user_val + "\n")
        if bot_val is not None:
            text.insert(END, "BOT <---" + str(bot_val) + "\n")
        if bot_val == "ok sir":
            root.destroy()
    else:
        text.insert(END, "BOT <--- Sorry, I didn't catch that. Please try again.\n")

def send():
    send_val = entry.get()
    if send_val: # Only proceed if entry is not empty
        bot_val = action.Action(send_val)
        text.insert(END, 'User---->' + send_val + "\n")
        if bot_val is not None:
            text.insert(END, "BOT <---" + str(bot_val) + "\n")
        if bot_val == "ok sir":
            root.destroy()
        entry.delete(0, END) # Clear the entry box after sending
    else:
        text.insert(END, "BOT <--- Please type something to send.\n")

def delete():
    text.delete("1.0", "end")

def check_reminders():
    """Checks for due reminders and displays them."""
    pending_reminders = database_manager.get_pending_reminders()
    current_time = datetime.datetime.now()

    for reminder_id, message, reminder_time_str in pending_reminders:
        # Convert stored string back to datetime object
        reminder_time = datetime.datetime.fromisoformat(reminder_time_str)
        if current_time >= reminder_time:
            text.insert(END, f"REMINDER: {message} (Due: {reminder_time.strftime('%I:%M %p')})\n", "reminder_tag")
            text_to_speech.text_to_speech(f"Reminder: {message}")
            database_manager.mark_reminder_set(reminder_id) # Mark as shown
    
    # Schedule the next check
    root.after(60000, check_reminders) # Check every 60 seconds (1 minute)

# Create a main frame to hold all content and center it
main_frame = Frame(root, bg="#cdc4e3")
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure root rows and columns to center main_frame
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# AI Assistant Title Label
text_label = Label(main_frame, text="AI Assistant", font=("comic Sans ms", 14), bg="purple", fg="white")
text_label.pack(pady=10)

# Image
try:
    image_path = "mic.jpg"
    image = ImageTk.PhotoImage(Image.open(image_path))
    image_label = Label(main_frame, image=image)
    image_label.image = image
    image_label.pack(pady=10)
except FileNotFoundError:
    error_label = Label(main_frame, text="Error: mic.jpg not found. Please ensure the image is in the correct directory.", fg="red")
    error_label.pack(pady=10)

# Text Widget
input_frame = Frame(main_frame, bg="#cdc4e3")
input_frame.pack(pady=10)

text = Text(input_frame, font=('courier 10 bold'), bg="pink", height=6, width=45) # Increased height/width
text.pack(pady=5)
text.tag_config("reminder_tag", foreground="blue", font=("courier" ,10, "bold", "italic")) # Style for reminders


# Entry Widget
entry = Entry(input_frame, justify=CENTER, width=50) # Increased width
entry.pack(pady=5)

#Buttons Frame
button_frame = Frame(main_frame, bg="#cdc4e3")
button_frame.pack(pady=20) # Add padding below the input elements

# Button 1 (ASK)
Button1 = Button(button_frame, text="ASK", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=ask)
Button1.grid(row=0, column=0, padx=10)

# Button 3 (DELETE) - Placed in the middle column
Button3 = Button(button_frame, text="DELETE", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=delete)
Button3.grid(row=0, column=1, padx=10)

# Button 2 (SEND)
Button2 = Button(button_frame, text="SEND", bg="pink", pady=10, padx=20, borderwidth=3, relief=SOLID, command=send)
Button2.grid(row=0, column=2, padx=10)



# Initial database setup (ensures tables exist when the app starts)
database_manager.create_tables()

# Start checking for reminders
check_reminders()

root.mainloop()

