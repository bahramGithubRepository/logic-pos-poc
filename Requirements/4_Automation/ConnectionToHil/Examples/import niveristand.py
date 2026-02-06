try:
    import niveristand
    from niveristand.legacy.NIVeriStand import Workspace2 
    
    
except ImportError:
    print("niveristand is not installed. Please install it with 'pip install niveristand'.")
    exit(1)

# Path to your VeriStand project file (.nivsproj)
project_path = r"C:\Users\es22025\Documents\VeriStand Projects\Sinewave Delay\Sinewave Delay.nivsproj"


# Connect to VeriStand Workspace
ws = Workspace2()

# Open the VeriStand project
ws.ConnectToProject(project_path)

# Deploy the project
ws.DeployProject()

# Example: Set a channel value
channel_path = '/Targets/Controller/Simulation Models/Models/delay_sinewave/Excecution/Model'
value_to_set = 42.0

# Set the channel value
#ws.SetSingleChannelValue(channel_path, value_to_set)

# Read the channel value
read_value = ws.GetSingleChannelValue(channel_path)

# Example: Set a variable (User Channel, Parameter, etc.)
#variable_path = '/Targets/Controller/User Channels/YourUserChannel'
#new_value = 123.45
#ws.SetSingleChannelValue(variable_path, new_value)

#print(f"Set {channel_path} to {value_to_set}")
print(f"Read {channel_path}: {read_value}")
#print(f"Set {variable_path} to {new_value}")
