import os
import time
from datetime import datetime
import pywhatkit


class WhatsAppAutomator:

    def __init__(self, log_file="whatsapp_log.txt"):
        self.log_file = log_file
        print("--- 🚀 Advanced WhatsApp Automation Engine Launched 🚀 ---\n")

    def _log_status(self, recipient, message, status, details=""):
        """Internal helper to write success/error states to a local text file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[{timestamp}] Target: {recipient} | Status: {status} | "
            f"Msg: '{message[:20]}...' | Details: {details}\n"
        )
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def validate_phone(self, phone_str):
        """Ensures the phone number has a country code prefix and basic numeric sanity."""
        cleaned = phone_str.strip().replace(" ", "").replace("-", "")
        if not cleaned.startswith("+"):
            print("❌ Error: Phone number must start with a country code (e.g., +91).")
            return None
        if not cleaned[1:].isdigit() or len(cleaned) < 10:
            print("❌ Error: Invalid numerical structure for phone number.")
            return None
        return cleaned

    def send_instant_message(self, phone_no, message):
        """Sends a text message immediately (with standard 15-second browser load buffer)."""
        valid_phone = self.validate_phone(phone_no)
        if not valid_phone:
            return False

        print(f"⏳ Preparing instant message to {valid_phone}...")
        try:
            # tab_close=True safely closes the browser tab 20 seconds after sending
            pywhatkit.sendwhatmsg_instantly(
                phone_no=valid_phone,
                message=message,
                wait_time=15,
                tab_close=True,
                close_time=20,
            )
            print(f"✅ Success: Instant message sent to {valid_phone}")
            self._log_status(valid_phone, message, "SUCCESS", "Instant Mode")
            return True
        except Exception as e:
            print(f"❌ Failed to send to {valid_phone}. See logs.")
            self._log_status(valid_phone, message, "FAILED", str(e))
            return False

    def send_scheduled_message(self, phone_no, message, hr, min):
        """Schedules a text message for a specific hour and minute (24H format)."""
        valid_phone = self.validate_phone(phone_no)
        if not valid_phone:
            return False

        print(f"📅 Scheduling message to {valid_phone} for {hr:02d}:{min:02d}...")
        try:
            pywhatkit.sendwhatmsg(
                phone_no=valid_phone,
                message=message,
                time_hour=hr,
                time_min=min,
                wait_time=15,
                tab_close=True,
                close_time=20,
            )
            print(f"✅ Success: Scheduled task completed for {valid_phone}")
            self._log_status(
                valid_phone, message, "SUCCESS", f"Scheduled for {hr}:{min}"
            )
            return True
        except Exception as e:
            print(f"❌ Failed scheduled delivery to {valid_phone}.")
            self._log_status(valid_phone, message, "FAILED", str(e))
            return False

    def send_media_message(self, phone_no, file_path, caption=""):
        """Sends images, videos, or documents directly with an optional text caption."""
        valid_phone = self.validate_phone(phone_no)
        if not valid_phone or not os.path.exists(file_path):
            print(f"❌ Error: File path does not exist: {file_path}")
            return False

        print(f"🖼️ Preparing media delivery ({os.path.basename(file_path)}) to {valid_phone}...")
        try:
            pywhatkit.sendwhats_image(
                receiver=valid_phone,
                img_path=file_path,
                caption=caption,
                wait_time=15,
                tab_close=True,
                close_time=20,
            )
            print(f"✅ Success: Media sent to {valid_phone}")
            self._log_status(
                valid_phone, caption, "SUCCESS", f"Media attached: {file_path}"
            )
            return True
        except Exception as e:
            print(f"❌ Failed media delivery to {valid_phone}.")
            self._log_status(valid_phone, caption, "FAILED", str(e))
            return False

    def bulk_send(self, contact_dict, message_template):
        """
        Sends sequential messages to multiple targets.
        contact_dict structure: {"+91XXXXX": "Name", "+91YYYYY": "Name"}
        """
        print(f"📋 Starting bulk broadcast to {len(contact_dict)} contacts...")
        for phone, name in contact_dict.items():
            # Personalize the template string dynamically
            personalized_msg = message_template.replace("{name}", name)

            success = self.send_instant_message(phone, personalized_msg)

            if success:
                # Cool-down delay to prevent WhatsApp automation blockages
                print("⏳ Waiting 10 seconds before queuing next recipient...")
                time.sleep(10)


# --- Execution Example Panel ---
if __name__ == "__main__":
    # Initialize the automator engine
    bot = WhatsAppAutomator()

    # Change this target number to test your applications (+ sign is mandatory)
    test_number = "+91_testing_number"

    print("Choose an option:")
    print("1. Send Instant Message")
    print("2. Send Scheduled Message")
    print("3. Send Media/Image Message")
    print("4. Run Bulk Broadcast Demo")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        bot.send_instant_message(test_number, "Hi Aditya, this is an instant test alert!")

    elif choice == "2":
        # Example setup: grab current time and schedule for 2 minutes from now
        now = datetime.now()
        target_hour = now.hour
        target_minute = now.minute + 2

        # Roll over hour adjustments if minutes clip past the hour boundary
        if target_minute >= 60:
            target_minute -= 60
            target_hour = (target_hour + 1) % 24

        bot.send_scheduled_message(
            test_number,
            "Hi Aditya, this was automatically scheduled!",
            target_hour,
            target_minute,
        )

    elif choice == "3":
        # Specify a mock filename pathway
        path_to_file = "sample_chart.png"

        # Create a blank file for testing purposes if it doesn't exist
        with open(path_to_file, "w") as f:
            f.write("Placeholder image binary data")

        bot.send_media_message(
            test_number,
            file_path=path_to_file,
            caption="Check out this automated file delivery!",
        )

    elif choice == "4":
        # Bulk list matching numbers to specific names
        broadcast_list = {
            "+918240543535": "Aditya",
            "+919999999999": "Alex",
        }
        msg_template = "Hello {name}, this is a customized message broadcast!"

        bot.bulk_send(broadcast_list, msg_template)

    else:
        print("Invalid Selection.")