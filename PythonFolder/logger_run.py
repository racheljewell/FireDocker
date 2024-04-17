from PythonFolder.logger import Logger  

# Test calls to log messages
Logger.log_message(201)  # Logs an informational message
Logger.log_message(400)  # Logs an error with a bad parameter
Logger.log_message(404, extra_info="Docker image not found in repository.")  # Logs a specific error with extra info
Logger.log_message(999)  # Logs a warning for an unknown error code

# Test calls to specific info and error functions
Logger.info("This is a general information message.")
Logger.error("This is a general error message.")

# Now check the app.log file to see the output
print("Logging completed. Check the 'app.log' file to review the log entries.")
