import subprocess

def install_requirements(requirements_file):
    # Execute pip install command
    subprocess.check_call(['pip', 'install', '-r', requirements_file])

# Path to the requirements.txt file
requirements_file = 'requirements.txt'

# Install requirements
install_requirements(requirements_file)

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

def add_fielder_positions(ax, positions_and_names, fielder_color):
    for position, name in positions_and_names.items():
        color = 'blue' if 'Batsman' in name else fielder_color
        ax.scatter(position[0], position[1], c=color)
        ax.text(position[0], position[1] + 0.01, name, fontsize=8, ha='center', color=color, zorder=5)

def draw_fielding_lines(ax, positions_and_names):
    for position, name in positions_and_names.items():
        if 'Batsman' not in name:
            ax.plot([position[0], 0.500], [position[1], 0.615], color='white', linestyle='dashed', linewidth=0.2)

def draw_pitch(ax):
    pitch = patches.Rectangle((0.425, 0.35), 0.15, 0.3, facecolor='peru', alpha=1, zorder=3)
    ax.add_patch(pitch)

def add_stumps(ax, stump_color):
    stump_width = 0.002
    stump_height = 0.01

    # Draw batting stumps
    for x in [0.49, 0.50, 0.51]:
        ax.plot([x, x], [0.615, 0.615 + stump_height], color=stump_color, linewidth=1, zorder=4)

    # Draw bowling stumps
    for x in [0.49, 0.50, 0.51]:
        ax.plot([x, x], [0.385, 0.385 + stump_height], color=stump_color, linewidth=1, zorder=4)

    # Add label for stumps
    ax.text(0.50, 0.622 + stump_height, '(Batting Side)\nStump ', fontsize=8, color='white', ha='center')  # Batting stump label
    ax.text(0.50, 0.345 + stump_height, 'Stump \n (Bowling Side)', fontsize=8, color='white', ha='center')  # Bowling stump label


def add_bat(ax, bat_color):
    bat = patches.Rectangle((0.525, 0.605), 0.03, 0.004, angle=165, facecolor=bat_color, edgecolor='black', zorder=4)
    ax.add_patch(bat)

def draw_grease_rectangle(ax, x, y, width, height):
    grease_rectangle = patches.Rectangle((x, y), width, height, edgecolor='white', fill=False, zorder=5)
    ax.add_patch(grease_rectangle)

def draw_grease(ax):
    draw_grease_rectangle(ax, 0.45, 0.6, 0.1, 0.03)
    draw_grease_rectangle(ax, 0.45, 0.375, 0.1, 0.03)

def draw_wide_lines(ax):
    draw_grease_rectangle(ax, 0.465, 0.6, 0.07, 0.03)
    draw_grease_rectangle(ax, 0.465, 0.375, 0.07, 0.03)

def draw_cricket_pitch(ax, fielder_color, stump_color, bat_color, outfield_color, inner_circle_color, user_positions):
    # Call draw_pitch function once
    draw_pitch(ax)

    # Create the main cricket ground ellipse (outer boundary)
    out_field = patches.Ellipse((0.5, 0.5), 1, 0.8, facecolor=outfield_color, zorder=0)

    # Add the main cricket ground ellipse to the existing axis
    ax.add_patch(out_field)

    # Add the pitch ellipse (inner boundary representing the pitch)
    inner_circle = patches.Ellipse((0.5, 0.5), 0.6, 0.5, edgecolor='white', facecolor=inner_circle_color, fill=True,
                                   ls='-.', zorder=1)
    ax.add_patch(inner_circle)

    # Add the rectangular patch for one end of the pitch
    pitch = patches.Rectangle((0.425, 0.35), 0.15, 0.3, facecolor=outfield_color, alpha=1, zorder=0)
    ax.add_patch(pitch)

    # Scatter plot to represent player positions with labels
    positions_and_names = {
        (0.5, 0.22): 'Bowler',
        (0.5, 0.69): 'Keeper',
        (0.555, 0.595): 'Batsman',  # Batsman position
        (0.56, 0.375): 'NS \nBatsman'  # Non-striking Batsman position
    }

    # Add user-defined fielding positions
    positions_and_names.update(user_positions)

    add_fielder_positions(ax, positions_and_names, fielder_color)

    # Add stumps and draw lines
    add_stumps(ax, stump_color)

    # Add bat
    add_bat(ax, bat_color)

    # Draw fielding lines
    draw_fielding_lines(ax, positions_and_names)

    # Draw additional elements
    draw_grease(ax)
    draw_wide_lines(ax)

    # Add watermark
    watermark_text = 'Hari-BME'
    ax.annotate(watermark_text, xy=(0.5, 0.5), xycoords='axes fraction',
                fontsize=12, color='grey', alpha=0.5, rotation=45, ha='center', va='center')

    # Hide axis
    ax.axis('off')

def main():
    st.title('Cricket Pitch Visualization')

    # Add a sidebar for color selection and image saving options
    st.sidebar.header('Customization Options')

    # Add input widgets for color selection in the sidebar
    fielder_color = st.sidebar.color_picker("Select Fielder Color", "#1f77b4")
    stump_color = st.sidebar.color_picker("Select Stump Color", "#ff0000")
    bat_color = st.sidebar.color_picker("Select Bat Color", "#8b4513")
    outfield_color = st.sidebar.color_picker("Select Outfield Color", "#006400")
    inner_circle_color = st.sidebar.color_picker("Select Inner Circle Color", "#008000")  # Add color widget for inner circle

    # Add user-defined fielding positions
    st.sidebar.subheader('User-defined Fielding Positions')

    user_positions = {}
    for i in range(1, 10):
        position_name = st.sidebar.text_input(f'Fielder {i} Name', f'Fielder{i}')
        position_x = st.sidebar.slider(f'Fielder {i} X Position', 0.0, 1.0, 0.5, 0.01)
        position_y = st.sidebar.slider(f'Fielder {i} Y Position', 0.0, 1.0, 0.5, 0.01)

        user_positions[(position_x, position_y)] = position_name

    # Create a subplot with one axis and set the figure size
    fig, ax = plt.subplots(1, figsize=(8, 8))

    # Call draw_cricket_pitch with the existing axis and user-defined positions
    draw_cricket_pitch(ax, fielder_color, stump_color, bat_color, outfield_color, inner_circle_color, user_positions)

    # Display the plot using Streamlit
    st.pyplot(fig)

    # Add details about how the visualization works
    st.subheader('How it Works:')
    st.markdown(
        """
        This cricket pitch visualization shows the player positions, stumps, bat, and other elements on the cricket pitch.
        You can customize the colors of the fielder, stumps, bat, outfield, and inner circle using the sidebar widgets.
        """
    )

    # Save image options
    st.subheader('Save Image Options')
    image_format = st.selectbox('Select Image Format', ['PNG', 'JPEG'])
    image_dpi = st.slider('Select Image DPI', 50, 300, 100)
    image_size = st.slider('Select Image Size (in inches)', 5, 20, 8)


    if st.button('Save Image'):
    # Save the plot as an image
        img = io.BytesIO()

        # Choose the appropriate format based on the user's selection
        image_format = image_format.lower()
        plt.savefig(img, format=image_format, dpi=image_dpi, bbox_inches='tight')
        img.seek(0)

        # Display the saved image
        st.image(img, caption='Saved Image', use_column_width=True)

        # Create a download button for the saved image
        st.download_button(
            label="Download Image",
            data=img,
            file_name="cricket_pitch_image." + image_format,  # Append the selected format to the file name
            mime="image/" + image_format  # Set the MIME type based on the selected format
        )



if __name__ == '__main__':
    main()
