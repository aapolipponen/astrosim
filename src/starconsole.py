import sys
import os

# Try to import readline for command history (enables up/down arrow navigation)
_history_file = '.starconsole_history'
_readline_initialized = False

def init_readline():
    """Initialize readline for command history."""
    global _readline_initialized
    if _readline_initialized:
        return
    
    try:
        import readline
        # Set up readline for history
        readline.set_history_length(1000)
        
        # Try to load existing history
        try:
            if os.path.exists(_history_file):
                readline.read_history_file(_history_file)
        except Exception:
            pass
        
        _readline_initialized = True
    except ImportError:
        # readline not available (e.g., on Windows)
        pass

def save_history():
    """Save command history to file."""
    try:
        import readline
        readline.write_history_file(_history_file)
    except Exception:
        pass

def get_input_with_history(prompt):
    """Get input with command history support using readline."""
    init_readline()
    
    # Get input (readline automatically handles up/down arrows if available)
    cmd = input(prompt)
    
    # Save history after each command
    save_history()
    
    return cmd

def custom_repl(context):
    """
    Custom REPL for interactive star management.
    
    Parameters:
    - context: Dictionary containing the local context in which to execute commands.
    """
    print("\n=== StarConsole ===")
    print("Welcome to the interactive simulation console!")
    print("Type 'help' for available commands, or 'exit' to close the console.")
    print("Use Up/Down arrows to navigate command history.")
    print("You can also use any Python code to interact with the simulation.\n")
    
    while True:
        try:
            # Read with history support
            cmd = get_input_with_history("StarConsole >>> ")
            
            if cmd.strip() == "exit":
                print("Exiting StarConsole.")
                break
            
            if cmd.strip() == "help":
                print_help()
                continue
            
            if cmd.strip() == "list_bodies":
                list_bodies(context.get('bodies', []))
                continue
            
            if cmd.strip().startswith("focus "):
                body_name = cmd.strip()[6:].strip()
                focus_body(context, body_name)
                continue
            
            if cmd.strip().startswith("pause"):
                context['paused'] = True
                print("Simulation paused. Use 'unpause' or set paused=False to resume.")
                continue
            
            if cmd.strip().startswith("unpause") or cmd.strip().startswith("resume"):
                context['paused'] = False
                print("Simulation resumed.")
                continue
            
            if cmd.strip().startswith("timestep ") or cmd.strip().startswith("set_timestep "):
                try:
                    parts = cmd.split()
                    value = float(parts[-1])
                    context['timestep_seconds'] = value
                    # Force immediate update
                    if 'timestep_updated' in context:
                        context['timestep_updated'] = True
                    print(f"Timestep set to {value} seconds")
                except (ValueError, IndexError) as e:
                    print(f"Usage: timestep <value_in_seconds>")
                    print(f"Error: {e}")
                continue
            
            if cmd.strip().startswith("zoom ") or cmd.strip().startswith("set_zoom "):
                try:
                    parts = cmd.split()
                    value = float(parts[-1])
                    context['SCALE_DIST'] = value
                    print(f"Zoom/Scale set to {value}")
                except (ValueError, IndexError) as e:
                    print(f"Usage: zoom <value>")
                    print(f"Error: {e}")
                continue
            
            if cmd.strip().startswith("gravity ") or cmd.strip().startswith("set_gravity "):
                try:
                    parts = cmd.split()
                    if len(parts) > 1:
                        value = parts[-1].lower()
                        if value in ['on', 'true', '1', 'enable']:
                            context['gravity_enabled'] = True
                            print("Gravity enabled")
                        elif value in ['off', 'false', '0', 'disable']:
                            context['gravity_enabled'] = False
                            print("Gravity disabled")
                        else:
                            print("Usage: gravity <on|off>")
                    else:
                        # Toggle gravity
                        current = context.get('gravity_enabled', True)
                        context['gravity_enabled'] = not current
                        status = "enabled" if context['gravity_enabled'] else "disabled"
                        print(f"Gravity {status}")
                except Exception as e:
                    print(f"Usage: gravity <on|off> or just 'gravity' to toggle")
                    print(f"Error: {e}")
                continue

            # Toggle flags: FULL_ORBITS, fade_trails, draw_trail_for_empty, display_names
            if cmd.strip().startswith("full_orbits"):
                try:
                    parts = cmd.split()
                    if len(parts) == 1:
                        context['FULL_ORBITS'] = not context.get('FULL_ORBITS', False)
                    else:
                        val = parts[-1].lower()
                        context['FULL_ORBITS'] = val in ['on','true','1','enable']
                    print(f"FULL_ORBITS: {context['FULL_ORBITS']}")
                except Exception as e:
                    print(f"Usage: full_orbits [on|off]")
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("fade_trails"):
                try:
                    parts = cmd.split()
                    if len(parts) == 1:
                        context['fade_trails'] = not context.get('fade_trails', False)
                    else:
                        val = parts[-1].lower()
                        context['fade_trails'] = val in ['on','true','1','enable']
                    print(f"fade_trails: {context['fade_trails']}")
                except Exception as e:
                    print(f"Usage: fade_trails [on|off]")
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("draw_empty") or cmd.strip().startswith("draw_trail_for_empty"):
                try:
                    parts = cmd.split()
                    if len(parts) == 1:
                        context['draw_trail_for_empty'] = not context.get('draw_trail_for_empty', False)
                    else:
                        val = parts[-1].lower()
                        context['draw_trail_for_empty'] = val in ['on','true','1','enable']
                    print(f"draw_trail_for_empty: {context['draw_trail_for_empty']}")
                except Exception as e:
                    print(f"Usage: draw_empty [on|off]")
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("display_names"):
                try:
                    parts = cmd.split()
                    if len(parts) == 1:
                        context['display_names'] = not context.get('display_names', True)
                    else:
                        val = parts[-1].lower()
                        context['display_names'] = val in ['on','true','1','enable']
                    print(f"display_names: {context['display_names']}")
                except Exception as e:
                    print(f"Usage: display_names [on|off]")
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("gravity_field"):
                try:
                    parts = cmd.split()
                    if len(parts) == 1:
                        context['gravity_field'] = not context.get('gravity_field', False)
                    else:
                        val = parts[-1].lower()
                        context['gravity_field'] = val in ['on','true','1','enable']
                    status = "enabled" if context['gravity_field'] else "disabled"
                    print(f"Gravity field visualization: {status}")
                except Exception as e:
                    print(f"Usage: gravity_field [on|off]")
                    print(f"Error: {e}")
                continue

            if cmd.strip() == "clear_trails" or cmd.strip() == "clear_trail":
                try:
                    from display import clear_body_trails
                    clear_body_trails()
                    print("All trails cleared.")
                except Exception as e:
                    print(f"Error clearing trails: {e}")
                continue

            if cmd.strip() == "status":
                show_status(context)
                continue

            if cmd.strip().startswith("distance "):
                try:
                    parts = cmd.split()
                    if len(parts) < 3:
                        print("Usage: distance <body1> <body2>")
                    else:
                        body1_name = parts[1]
                        body2_name = parts[2]
                        bodies_list = context.get('bodies', [])
                        body1 = find_body_by_name(bodies_list, body1_name)
                        body2 = find_body_by_name(bodies_list, body2_name)
                        if body1 and body2:
                            from constants import AU
                            dist = calculate_distance_3d(body1.pos, body2.pos)
                            print(f"Distance between {body1.name} and {body2.name}: {dist:.2e} m ({dist/AU:.4f} AU)")
                        else:
                            if not body1:
                                print(f"Body '{body1_name}' not found.")
                            if not body2:
                                print(f"Body '{body2_name}' not found.")
                except Exception as e:
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("lagrange_points ") or cmd.strip().startswith("lagrange "):
                try:
                    parts = cmd.split()
                    if len(parts) < 3:
                        print("Usage: lagrange_points <body1> <body2>")
                        print("       Calculates L1, L2, L3, L4, L5 Lagrange points")
                    else:
                        body1_name = parts[1]
                        body2_name = parts[2]
                        bodies_list = context.get('bodies', [])
                        body1 = find_body_by_name(bodies_list, body1_name)
                        body2 = find_body_by_name(bodies_list, body2_name)
                        if body1 and body2:
                            calculate_lagrange_points(body1, body2)
                        else:
                            if not body1:
                                print(f"Body '{body1_name}' not found.")
                            if not body2:
                                print(f"Body '{body2_name}' not found.")
                except Exception as e:
                    print(f"Error: {e}")
                continue

            if cmd.strip().startswith("filter "):
                try:
                    parts = cmd.split()
                    if len(parts) < 2:
                        print("Usage: filter <type>")
                        print("       Types: planet, moon, star, probe, or 'all' to show all")
                    else:
                        filter_type = parts[1].lower()
                        bodies_list = context.get('bodies', [])
                        if filter_type == 'all':
                            list_bodies(bodies_list)
                        else:
                            filtered = [b for b in bodies_list if b.type and b.type.lower() == filter_type]
                            if filtered:
                                list_bodies(filtered)
                            else:
                                print(f"No bodies found with type '{filter_type}'")
                                print("Available types:", set(b.type for b in bodies_list if b.type))
                except Exception as e:
                    print(f"Error: {e}")
                continue

            # Evaluate (for commands that return a value like variable access)
            try:
                result = eval(cmd, context)
                if result is not None:
                    print(result)
            except SyntaxError:
                # If evaluation failed, then try exec (for statements that don't return a value)
                exec(cmd, context)
            except Exception as e:
                # If eval failed with non-SyntaxError, try exec
                try:
                    exec(cmd, context)
                except Exception as e2:
                    print(f"Error: {e2}")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to close the console.")
        except EOFError:
            print("\nExiting StarConsole.")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print help information for available commands."""
    help_text = """
Available Commands:
  help                  - Show this help message
  exit                  - Exit the console
  list_bodies           - List all bodies in the simulation
  focus <name>          - Focus the camera on a specific body
  pause                 - Pause the simulation
  unpause/resume        - Resume the simulation
  timestep <value>      - Set simulation timestep in seconds
  zoom <value>          - Set zoom/scale factor
  gravity [on|off]      - Toggle gravity on/off (or just 'gravity' to toggle)
  full_orbits [on|off]  - Toggle drawing of full orbits
  fade_trails [on|off]  - Toggle trail fading
  draw_empty [on|off]   - Toggle drawing trails for empty bodies
  display_names [on|off] - Toggle name labels
  gravity_field [on|off] - Toggle gravity field visualization
  clear_trails          - Clear all body trails
  status                - Show current simulation status and settings
  distance <b1> <b2>    - Calculate distance between two bodies
  lagrange_points <b1> <b2> - Calculate Lagrange points between two bodies
  filter <type>         - Filter bodies by type (planet, moon, star, probe, all)

Python Access:
  You can access simulation variables directly:
    - bodies              - List of all bodies
    - timestep_seconds    - Current timestep
    - SCALE_DIST         - Current zoom/scale
    - focus_object       - Currently focused body
    - paused             - Pause state (True/False)
    - running            - Simulation running state
    - gravity_enabled    - Gravity state (True/False)
    - gravity_field      - Gravity field visualization (True/False)
    - FULL_ORBITS        - Draw full orbits
    - fade_trails        - Trail fading enabled
    - draw_trail_for_empty - Draw trails for empty bodies
    - display_names      - Render name labels

Examples:
  >>> Earth.pos
  >>> bodies[0].name
  >>> timestep 3600
  >>> focus Jupiter
  >>> gravity off
  >>> gravity on
  >>> paused = True
  >>> [b.name for b in bodies]
  >>> distance Earth Mars
  >>> lagrange_points Sun Earth
  >>> filter planet
  >>> status
"""
    print(help_text)


def list_bodies(bodies):
    """List all bodies in the simulation."""
    if not bodies:
        print("No bodies found.")
        return
    
    print(f"\nFound {len(bodies)} body(ies):")
    print("-" * 60)
    for i, body in enumerate(bodies):
        pos_str = f"({body.pos[0]:.2e}, {body.pos[1]:.2e}, {body.pos[2]:.2e})"
        print(f"{i}: {body.name:15} | Type: {body.type:10} | Pos: {pos_str}")
    print("-" * 60)


def find_body_by_name(bodies, name):
    """Find a body by name (case-insensitive, supports partial matching)."""
    name_lower = name.lower()
    
    # Try exact match first
    for b in bodies:
        if b.name.lower() == name_lower:
            return b
    
    # Try partial match
    matches = [b for b in bodies if name_lower in b.name.lower()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Multiple matches found for '{name}': {[b.name for b in matches]}")
        return None
    
    return None


def calculate_distance_3d(pos1, pos2):
    """Calculate 3D distance between two positions."""
    import numpy as np
    return np.linalg.norm(np.array(pos1) - np.array(pos2))


def calculate_lagrange_points(body1, body2):
    """Calculate and display Lagrange points between two bodies."""
    import numpy as np
    from constants import G, AU
    
    # Determine which is the primary (more massive) and secondary
    if body1.mass >= body2.mass:
        primary = body1
        secondary = body2
    else:
        primary = body2
        secondary = body1
    
    # Calculate distance between bodies
    r = np.array(secondary.pos) - np.array(primary.pos)
    r_mag = np.linalg.norm(r)
    
    if r_mag < 1e-6:
        print("Bodies are too close together for Lagrange point calculation.")
        return
    
    # Mass ratio
    mu = secondary.mass / (primary.mass + secondary.mass)
    
    print(f"\nLagrange Points for {primary.name} (primary) and {secondary.name} (secondary):")
    print(f"Mass ratio μ = {mu:.6f}")
    print(f"Separation: {r_mag:.2e} m ({r_mag/AU:.4f} AU)")
    print("-" * 70)
    
    # L1: Between the two bodies, closer to secondary
    # Approximate solution using iterative method
    alpha = (mu / (3 * (1 - mu)))**(1/3)
    L1_dist = r_mag * (1 - alpha + alpha**2/3 - alpha**3/9)
    L1_pos = primary.pos + (L1_dist / r_mag) * r
    
    print(f"L1 (between bodies, closer to {secondary.name}):")
    print(f"  Position: ({L1_pos[0]:.2e}, {L1_pos[1]:.2e}, {L1_pos[2]:.2e}) m")
    print(f"  Distance from {primary.name}: {L1_dist:.2e} m ({L1_dist/AU:.4f} AU)")
    print(f"  Distance from {secondary.name}: {r_mag - L1_dist:.2e} m ({(r_mag - L1_dist)/AU:.4f} AU)")
    
    # L2: Beyond secondary
    beta = (mu / (3 * (1 + mu)))**(1/3)
    L2_dist = r_mag * (1 + beta + beta**2/3 - beta**3/9)
    L2_pos = primary.pos + (L2_dist / r_mag) * r
    
    print(f"\nL2 (beyond {secondary.name}):")
    print(f"  Position: ({L2_pos[0]:.2e}, {L2_pos[1]:.2e}, {L2_pos[2]:.2e}) m")
    print(f"  Distance from {primary.name}: {L2_dist:.2e} m ({L2_dist/AU:.4f} AU)")
    print(f"  Distance from {secondary.name}: {L2_dist - r_mag:.2e} m ({(L2_dist - r_mag)/AU:.4f} AU)")
    
    # L3: Beyond primary (opposite side)
    gamma = (mu / (3 * (1 + mu)))**(1/3)
    L3_dist = r_mag * (1 - gamma - gamma**2/3 - gamma**3/9)
    L3_pos = primary.pos - (L3_dist / r_mag) * r
    
    print(f"\nL3 (beyond {primary.name}, opposite side):")
    print(f"  Position: ({L3_pos[0]:.2e}, {L3_pos[1]:.2e}, {L3_pos[2]:.2e}) m")
    print(f"  Distance from {primary.name}: {L3_dist:.2e} m ({L3_dist/AU:.4f} AU)")
    print(f"  Distance from {secondary.name}: {r_mag + L3_dist:.2e} m ({(r_mag + L3_dist)/AU:.4f} AU)")
    
    # L4 and L5: Equilateral triangle points (60 degrees ahead and behind)
    # Perpendicular vector to r
    r_unit = r / r_mag
    # Create a perpendicular vector (in the orbital plane)
    if abs(r_unit[2]) < 0.9:
        perp = np.cross(r_unit, np.array([0, 0, 1]))
    else:
        perp = np.cross(r_unit, np.array([1, 0, 0]))
    perp = perp / np.linalg.norm(perp)
    
    # Rotate r by 60 degrees
    cos60 = 0.5
    sin60 = np.sqrt(3) / 2
    L4_dir = cos60 * r_unit + sin60 * perp
    L5_dir = cos60 * r_unit - sin60 * perp
    
    L4_pos = primary.pos + r_mag * L4_dir
    L5_pos = primary.pos + r_mag * L5_dir
    
    print(f"\nL4 (60° ahead of {secondary.name}):")
    print(f"  Position: ({L4_pos[0]:.2e}, {L4_pos[1]:.2e}, {L4_pos[2]:.2e}) m")
    print(f"  Distance from {primary.name}: {r_mag:.2e} m ({r_mag/AU:.4f} AU)")
    print(f"  Distance from {secondary.name}: {r_mag:.2e} m ({r_mag/AU:.4f} AU)")
    
    print(f"\nL5 (60° behind {secondary.name}):")
    print(f"  Position: ({L5_pos[0]:.2e}, {L5_pos[1]:.2e}, {L5_pos[2]:.2e}) m")
    print(f"  Distance from {primary.name}: {r_mag:.2e} m ({r_mag/AU:.4f} AU)")
    print(f"  Distance from {secondary.name}: {r_mag:.2e} m ({r_mag/AU:.4f} AU)")
    print("-" * 70)


def show_status(context):
    """Display current simulation status and settings."""
    print("\n" + "=" * 70)
    print("SIMULATION STATUS")
    print("=" * 70)
    
    # Basic settings
    print(f"Running:           {context.get('running', 'N/A')}")
    print(f"Paused:            {context.get('paused', 'N/A')}")
    print(f"Gravity Enabled:   {context.get('gravity_enabled', 'N/A')}")
    print(f"Integration Method: {context.get('integration_method', 'N/A')}")
    
    # Display settings
    print(f"\nDisplay Settings:")
    print(f"  Zoom/Scale:      {context.get('SCALE_DIST', 'N/A'):.2e}")
    print(f"  Focus Object:    {context.get('focus_object', 'N/A').name if hasattr(context.get('focus_object', None), 'name') else 'N/A'}")
    print(f"  Full Orbits:     {context.get('FULL_ORBITS', 'N/A')}")
    print(f"  Fade Trails:     {context.get('fade_trails', 'N/A')}")
    print(f"  Draw Empty:       {context.get('draw_trail_for_empty', 'N/A')}")
    print(f"  Display Names:   {context.get('display_names', 'N/A')}")
    print(f"  Gravity Field:   {context.get('gravity_field', False)}")
    
    # Simulation settings
    print(f"\nSimulation Settings:")
    timestep = context.get('timestep_seconds', 0)
    if timestep:
        from constants import YEAR, MONTH, DAY, HOUR, MINUTE
        if timestep >= YEAR:
            print(f"  Timestep:        {timestep:.2e} s ({timestep/YEAR:.4f} years)")
        elif timestep >= DAY:
            print(f"  Timestep:        {timestep:.2e} s ({timestep/DAY:.4f} days)")
        elif timestep >= HOUR:
            print(f"  Timestep:        {timestep:.2e} s ({timestep/HOUR:.4f} hours)")
        elif timestep >= MINUTE:
            print(f"  Timestep:        {timestep:.2e} s ({timestep/MINUTE:.4f} minutes)")
        else:
            print(f"  Timestep:        {timestep:.2e} s")
    else:
        print(f"  Timestep:        {timestep}")
    
    # Body count
    bodies = context.get('bodies', [])
    print(f"\nBodies:            {len(bodies)}")
    if bodies:
        body_types = {}
        for body in bodies:
            body_type = body.type if body.type else 'unknown'
            body_types[body_type] = body_types.get(body_type, 0) + 1
        print(f"  By type:         {dict(body_types)}")
    
    print("=" * 70 + "\n")


def focus_body(context, body_name):
    """Focus the camera on a specific body by name."""
    bodies = context.get('bodies', [])
    body = None
    
    # Try exact match first
    for b in bodies:
        if b.name.lower() == body_name.lower():
            body = b
            break
    
    # Try partial match if exact match failed
    if body is None:
        matches = [b for b in bodies if body_name.lower() in b.name.lower()]
        if len(matches) == 1:
            body = matches[0]
        elif len(matches) > 1:
            print(f"Multiple matches found: {[b.name for b in matches]}")
            print("Please use a more specific name.")
            return
    
    if body:
        context['focus_object'] = body
        from display import clear_body_trails
        clear_body_trails()
        print(f"Focus changed to {body.name}")
    else:
        print(f"Body '{body_name}' not found. Use 'list_bodies' to see available bodies.")
