# import text_to_speech
# import speech_to_text
# import datetime
# import webbrowser
# # import weather



# def Action(data):
#      user_data = data.lower()

#      #user_data = speech_to_text.speech_to_text()

#      if"what is your name" in user_data :
#         text_to_speech.text_to_speech("My name is virtual assistant")
    

#      elif "hello" in user_data or "hye" in user_data:
#         text_to_speech.text_to_speech("hey, sir How i can help you")
    

#      elif "good morning" in user_data:
#         text_to_speech.text_to_speech("good morning sir")

#      elif "time now"in user_data:
#          current_time = datetime.datetime.now()
#          Time = (str)(current_time) + "Hour :", (str)(current_time.minute) + "Minute"
#          text_to_speech.text_to_speech(Time)

#      elif "shutdown" in user_data:
#          text_to_speech.text_to_speech("ok sir")
     
#      elif "play music" in user_data :
#          webbrowser.open("https://gaana.com/")
#          text_to_speech("gaana.com is now ready for you")
     
#      elif "youtube" in user_data :
#          webbrowser.open("https://youtube.com/")
#          text_to_speech.text_to_speech("youtube.com is now ready for you")

#      elif "open google" in user_data :
#          webbrowser.open("https://google.com/")
#          text_to_speech.text_to_speech("google.com is now ready for you")

#      elif "weather" in user_data:
#         #  ans= weather.weather()
#         webbrowser.open("https://in.search.yahoo.com/search;_ylt=Awr1VS.vo39oIQIAugu7HAx.;_ylc=X1MDMjExNDcyMzAwMwRfcgMyBGZyA21jYWZlZQRmcjIDc2ItdG9wBGdwcmlkA0Y0MkNhNF9RUU9hbnVNUFNqc1h0RkEEbl9yc2x0AzAEbl9zdWdnAzEEb3JpZ2luA2luLnNlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzE4BHF1ZXJ5A3dlYXRoZXIlMjBvZiUyMGF5b2RoeWEEdF9zdG1wAzE3NTMxOTU0NTU-?p=weather+of+ayodhya&fr=mcafee&type=E210IN714G0&fr2=sb-top")
#         text_to_speech.text_to_speech("weather of ayodhya is now ready for you.")

#      else :
#          text_to_speech.text_to_speech("I'm not able to understand")


#update code

import text_to_speech
import speech_to_text
import datetime
import webbrowser
import database_manager # Import the new database module
import re # For more advanced parsing, especially for reminders

def Action(data):
    user_data = data.lower()

    if "what is your name" in user_data:
        text_to_speech.text_to_speech("My name is virtual assistant")
        return "My name is virtual assistant"

    elif "hello" in user_data or "hye" in user_data:
        text_to_speech.text_to_speech("hey, sir How i can help you")
        return "hey, sir How i can help you"

    elif "good morning" in user_data:
        text_to_speech.text_to_speech("good morning sir")
        return "good morning sir"

    elif "time now" in user_data:
        current_time = datetime.datetime.now()
        Time_str = current_time.strftime("%I:%M %p") # Format as HH:MM AM/PM
        text_to_speech.text_to_speech(f"The current time is {Time_str}")
        return f"The current time is {Time_str}"

    elif "shutdown" in user_data or "ok sir" in user_data:
        text_to_speech.text_to_speech("ok sir, shutting down")
        return "ok sir" # This will trigger root.destroy() in gui.py

    elif "play music" in user_data:
        webbrowser.open("https://gaana.com/")
        text_to_speech.text_to_speech("gaana.com is now ready for you")
        return "gaana.com is now ready for you"

    elif "youtube" in user_data:
        webbrowser.open("https://www.youtube.com/")
        text_to_speech.text_to_speech("YouTube is now ready for you")
        return "YouTube is now ready for you"

    elif "open google" in user_data:
        webbrowser.open("https://google.com/")
        text_to_speech.text_to_speech("Google is now ready for you")
        return "Google is now ready for you"

    elif "weather" in user_data:
        webbrowser.open("https://in.search.yahoo.com/search?p=weather+of+ayodhya")
        text_to_speech.text_to_speech("Weather of Ayodhya is now ready for you.")
        return "Weather of Ayodhya is now ready for you."

    # --- New Database-related commands ---

    elif "add to do" in user_data or "add a task" in user_data:
        task_match = re.search(r'(add to do|add a task)\s+(.*)', user_data)
        if task_match:
            task = task_match.group(2).strip()
            if database_manager.add_todo(task):
                text_to_speech.text_to_speech(f"I've added '{task}' to your to-do list.")
                return f"Added '{task}' to your to-do list."
            else:
                text_to_speech.text_to_speech("Sorry, I couldn't add that to your to-do list.")
                return "Sorry, I couldn't add that to your to-do list."
        else:
            text_to_speech.text_to_speech("What task would you like to add?")
            return "What task would you like to add?"

    elif "what are my to dos" in user_data or "list my tasks" in user_data:
        todos = database_manager.get_all_todos()
        if todos:
            response = "Here are your to-do items:\n"
            speech_response = "Here are your to-do items. "
            for i, todo in enumerate(todos):
                status = "completed" if todo[2] else "pending"
                response += f"{i+1}. {todo[1]} ({status})\n"
                speech_response += f"Number {i+1}, {todo[1]}, status {status}. "
            text_to_speech.text_to_speech(speech_response)
            return response
        else:
            text_to_speech.text_to_speech("You don't have any to-do items.")
            return "You don't have any to-do items."

    elif "mark to do complete" in user_data or "complete task" in user_data:
        id_match = re.search(r'(mark to do complete|complete task)\s+(\d+)', user_data)
        if id_match:
            todo_id = int(id_match.group(2))
            if database_manager.mark_todo_complete(todo_id):
                text_to_speech.text_to_speech(f"To-do item {todo_id} marked as complete.")
                return f"To-do item {todo_id} marked as complete."
            else:
                text_to_speech.text_to_speech("Could not find that to-do item or it's already complete.")
                return "Could not find that to-do item or it's already complete."
        else:
            text_to_speech.text_to_speech("Which to-do item do you want to mark complete? Please say the number.")
            return "Which to-do item do you want to mark complete? Please say the number."

    elif "take a note" in user_data or "write a note" in user_data:
        note_match = re.search(r'(take a note|write a note)\s+(.*)', user_data)
        if note_match:
            note_content = note_match.group(2).strip()
            if database_manager.add_note(note_content):
                text_to_speech.text_to_speech("I've saved your note.")
                return "Note saved."
            else:
                text_to_speech.text_to_speech("Sorry, I couldn't save your note.")
                return "Sorry, I couldn't save your note."
        else:
            text_to_speech.text_to_speech("What would you like me to write down?")
            return "What would you like me to write down?"

    elif "read my last note" in user_data or "what was my last note" in user_data:
        last_note = database_manager.get_last_note()
        if last_note:
            text_to_speech.text_to_speech(f"Your last note was: {last_note}")
            return f"Your last note was: {last_note}"
        else:
            text_to_speech.text_to_speech("You haven't taken any notes yet.")
            return "You haven't taken any notes yet."

    elif "set a reminder" in user_data or "remind me to" in user_data:
        # Example command: "Set a reminder to call mom at 5 PM tomorrow"
        # This parsing can be complex, and might need a dedicated NLP library for robustness.
        # For simplicity, let's assume a basic structure: "remind me to [message] at [time] [date]"
        # or "remind me to [message] in [duration]"

        reminder_match = re.search(r'remind me to (.*?) (at|in) (.*)', user_data)
        if reminder_match:
            message = reminder_match.group(1).strip()
            time_phrase = reminder_match.group(3).strip()
            
            # Simple time parsing (needs significant improvement for real-world use)
            reminder_datetime = None
            try:
                if "tomorrow" in time_phrase:
                    target_date = datetime.date.today() + datetime.timedelta(days=1)
                    time_part = re.search(r'(\d{1,2}(:\d{2})?\s*(am|pm)?)', time_phrase)
                    if time_part:
                        time_str = time_part.group(1).replace(" ", "")
                        reminder_datetime = datetime.datetime.strptime(f"{target_date} {time_str}", "%Y-%m-%d %I%M%p")
                    else:
                        reminder_datetime = datetime.datetime.combine(target_date, datetime.time(9, 0)) # Default to 9 AM tomorrow
                elif "today" in time_phrase or "at" in time_phrase:
                    target_date = datetime.date.today()
                    time_part = re.search(r'(\d{1,2}(:\d{2})?\s*(am|pm)?)', time_phrase)
                    if time_part:
                        time_str = time_part.group(1).replace(" ", "")
                        reminder_datetime = datetime.datetime.strptime(f"{target_date} {time_str}", "%Y-%m-%d %I%M%p")
                    else: # If no specific time, just set for now
                         reminder_datetime = datetime.datetime.now()
                elif "in" in time_phrase:
                    duration_match = re.search(r'(\d+)\s*(minute|hour|day)s?', time_phrase)
                    if duration_match:
                        value = int(duration_match.group(1))
                        unit = duration_match.group(2)
                        if unit == "minute":
                            reminder_datetime = datetime.datetime.now() + datetime.timedelta(minutes=value)
                        elif unit == "hour":
                            reminder_datetime = datetime.datetime.now() + datetime.timedelta(hours=value)
                        elif unit == "day":
                            reminder_datetime = datetime.datetime.now() + datetime.timedelta(days=value)

            except ValueError:
                text_to_speech.text_to_speech("I couldn't understand the time for the reminder. Please try again.")
                return "I couldn't understand the time for the reminder. Please try again."

            if reminder_datetime:
                # Store time in ISO format for easy comparison
                reminder_time_str = reminder_datetime.isoformat(sep=' ', timespec='seconds')
                if database_manager.add_reminder(message, reminder_time_str):
                    text_to_speech.text_to_speech(f"Okay, I'll remind you to {message} at {reminder_datetime.strftime('%I:%M %p on %A, %B %d')}")
                    return f"Reminder set for: {message} at {reminder_datetime.strftime('%I:%M %p on %A, %B %d')}"
                else:
                    text_to_speech.text_to_speech("Sorry, I couldn't set that reminder.")
                    return "Sorry, I couldn't set that reminder."
            else:
                text_to_speech.text_to_speech("I need more information to set the reminder. Please specify a time.")
                return "I need more information to set the reminder. Please specify a time."
        else:
            text_to_speech.text_to_speech("What would you like me to remind you about and when?")
            return "What would you like me to remind you about and when?"

    else:
        text_to_speech.text_to_speech("I'm not able to understand")
        return "I'm not able to understand"