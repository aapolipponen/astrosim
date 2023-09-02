def custom_repl(context):
    """
    Custom REPL for interactive star management.
    
    Parameters:
    - context: Dictionary containing the local context in which to execute commands.
    """
    while True:
        try:
            # Read
            cmd = input("StarConsole >>> ")
            
            if cmd.strip() == "exit":
                print("Exiting StarConsole.")
                break

            # Evaluate (for commands that return a value like variable access)
            try:
                result = eval(cmd, context)
                if result is not None:
                    print(result)
            except:
                # If evaluation failed, then try exec (for statements that don't return a value)
                exec(cmd, context)
        
        except Exception as e:
            print(f"Error: {e}")
