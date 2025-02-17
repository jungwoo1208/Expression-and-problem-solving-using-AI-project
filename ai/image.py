import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_yolov8_structure():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw backbone
    backbone = Rectangle((0.1, 0.6), 0.3, 0.3, edgecolor='blue', facecolor='lightblue')
    ax.add_patch(backbone)
    ax.text(0.25, 0.75, 'Backbone\n(CSPDarknet)', horizontalalignment='center', verticalalignment='center')

    # Draw neck
    neck = Rectangle((0.45, 0.6), 0.3, 0.3, edgecolor='green', facecolor='lightgreen')
    ax.add_patch(neck)
    ax.text(0.6, 0.75, 'Neck\n(FPN + PANet)', horizontalalignment='center', verticalalignment='center')

    # Draw head
    head = Rectangle((0.8, 0.6), 0.15, 0.3, edgecolor='red', facecolor='salmon')
    ax.add_patch(head)
    ax.text(0.875, 0.75, 'Head\n(Output)', horizontalalignment='center', verticalalignment='center')

    # Draw input
    input_layer = Rectangle((0.05, 0.45), 0.9, 0.1, edgecolor='black', facecolor='white')
    ax.add_patch(input_layer)
    ax.text(0.5, 0.5, 'Input Image', horizontalalignment='center', verticalalignment='center')

    # Draw arrows
    ax.arrow(0.2, 0.55, 0, 0.05, head_width=0.02, head_length=0.02, fc='black', ec='black')
    ax.arrow(0.55, 0.55, 0, 0.05, head_width=0.02, head_length=0.02, fc='black', ec='black')
    ax.arrow(0.85, 0.55, 0, 0.05, head_width=0.02, head_length=0.02, fc='black', ec='black')

    # Set limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('YOLOv8 Model Structure')

    plt.show()

draw_yolov8_structure()
