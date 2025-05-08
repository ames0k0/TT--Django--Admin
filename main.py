def say_hello(name):
    """
    A function that returns a greeting message with the provided name.
    
    Args:
        name (str): The name of the person to greet
        
    Returns:
        str: A greeting message
    """
    return f"Hello, {name}!"

# Example usage
if __name__ == "__main__":
    user_name = input("Please enter your name: ")
    greeting = say_hello(user_name)
    print(greeting)
