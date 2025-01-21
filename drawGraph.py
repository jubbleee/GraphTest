import graph
from stiffnessMatrix import createGlobalMatrix, findDisplacements, findLength
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graphVisual

global graph1

def iterate():
    global figList
    global count
    figList = []
    count = 0
    fig = graph1.visualise()
    figList.append(fig)

    while True:
        globalMatrix = createGlobalMatrix(graph1)
        lengthStart = findLength(graph1)

        displacements = findDisplacements(graph1, globalMatrix)
        if displacements[0] == "Stop":
            return figList

        graph1.moveNodes(displacements)

        lengthEnd = findLength(graph1)

        graph1.weakenNodes( lengthStart, lengthEnd)
        fig = graph1.visualise()
        fig.show()
        figList.append(fig)

# Tkinter GUI Application
def display_plot(fig):
    global canvas

    # Destroy existing canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Embed the plot in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plotFrame)
    canvasWidget = canvas.get_tk_widget()
    canvasWidget.grid(row=0, column=0)
    canvas.draw()

def createButton():
    global graph1
    graph1 = graph.Graph()
    graph1.create(sliderSize.get(), sliderRandomness.get())
    print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections")

def editButton():
    editor = tk.Tk()
    graphEditor = graphVisual.GraphEditor(editor, graph1)
    editor.mainloop()

def goButton():
    figList = iterate()
    display_plot(figList[0])

def backward(event):
    global count
    if count == 0:
        tk.messagebox.showinfo("Error","No previous step")
    else:
        count-=1
        display_plot(figList[count])

def forward(event):
    global count
    if count == len(figList)-1:
        tk.messagebox.showinfo("Error","No further step")
    else:
        count+=1
        display_plot(figList[count])

def end():
    global count
    count = len(figList)-1
    display_plot(figList[count])



# Create the main tkinter application window
root = tk.Tk()
root.title("Network Visualizer")
root.geometry("854x480")

# Create a main frame to hold everything
mainFrame = ttk.Frame(root)
mainFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame for the plot
plotFrame = ttk.Frame(mainFrame, width=400, height=400, relief=tk.SUNKEN, borderwidth=2)
plotFrame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")
plotFrame.grid_propagate(False)  # Prevent the frame from resizing automatically

# Create the controls on the left side
controlFrame = ttk.Frame(mainFrame)
controlFrame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Add sliders and labels
# Network Size
labelSize = tk.Label(controlFrame, text="Network Height:")
labelSize.grid(row=1, column=0, pady=(10, 0), sticky="w")
sliderSize = tk.Scale(controlFrame, from_=3, to=20, orient="horizontal")
sliderSize.grid(row=2, column=0, pady=(0, 10), sticky="ew")

labelWidth = tk.Label(controlFrame, text="Network Width:")
labelWidth.grid(row=3, column=0, pady=(10, 0), sticky="w")
sliderWidth = tk.Scale(controlFrame, from_=2, to=20, orient="horizontal")
sliderWidth.grid(row=4, column=0, pady=(0, 10), sticky="ew")

# Randomness
label_randomness = tk.Label(controlFrame, text="Weighting Randomness:")
label_randomness.grid(row=5, column=0, pady=(10, 0), sticky="w")
sliderRandomness = tk.Scale(controlFrame, from_=1, to=10, orient="horizontal")
sliderRandomness.grid(row=6, column=0, pady=(0, 10), sticky="ew")

# Add a button to go to create graph
button = ttk.Button(controlFrame, text="Graph Create", command=createButton)
button.grid(row=7, column=0, pady=10, sticky="ew")

# Add a button to go to last fig
button = ttk.Button(controlFrame, text="Graph Editor", command=editButton)
button.grid(row=8, column=0, pady=10, sticky="ew")

# Add a button to refresh the plot
button = ttk.Button(controlFrame, text="Generate Plot", command=goButton)
button.grid(row=9, column=0, pady=10, sticky="ew")

# Add a button to go to last fig
button = ttk.Button(controlFrame, text="Result", command=end)
button.grid(row=11, column=0, pady=10, sticky="ew")

# Initialize canvas
canvas = None
figList = []
count = 0

# Resizing behavior
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.bind("<Right>", forward)
root.bind("<Left>", backward)

mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()





