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
    prevCons = len(graph1.connections)
    figNum = 0
    while True:
        figNum+=1
        globalMatrix = createGlobalMatrix(graph1)
        lengthStart = findLength(graph1)

        displacements = findDisplacements(graph1, globalMatrix)
        if displacements[0] == "Stop":
            print("Stop")
            return figList

        graph1.moveNodes(displacements)

        lengthEnd = findLength(graph1)

        graph1.weakenNodes( lengthStart, lengthEnd)

        if len(graph1.connections) < prevCons:
            fig = graph1.visualise()
            fig.show()
            figList.append(fig)
            prevCons = len(graph1.connections)
            print(figNum)
            #for con in graph1.connections:
            #    con.weight = 1

def displayPlot(fig):
    global canvas, ax

    # Delete existing canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plotFrame)
    canvasWidget = canvas.get_tk_widget()
    canvasWidget.grid(row=0, column=0)

    # Connect mouse scroll event
    canvasWidget.bind("<Button-4>", zoom)  # For Linux
    canvasWidget.bind("<Button-5>", zoom)  # For Linux
    canvasWidget.bind("<MouseWheel>", zoom)  # For Windows and Mac

    canvas.draw()


def zoom(event):
    scale_factor = 1.05  # More subtle zoom
    ax = canvas.figure.axes[0]  # Get the main axis

    # Get current axis limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Convert mouse position from canvas coordinates to data coordinates
    xdata = ax.transData.inverted().transform((event.x, event.y))[0]
    ydata = ax.transData.inverted().transform((event.x, event.y))[1]

    # Adjust limits based on scroll direction
    if event.delta > 0:  # Scroll up (Zoom in)
        new_xlim = [xdata + (x - xdata) / scale_factor for x in xlim]
        new_ylim = [ydata + (y - ydata) / scale_factor for y in ylim]
    else:  # Scroll down (Zoom out)
        new_xlim = [xdata + (x - xdata) * scale_factor for x in xlim]
        new_ylim = [ydata + (y - ydata) * scale_factor for y in ylim]

    # Apply new limits
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    # Redraw the canvas
    canvas.draw()

def createButton():
    # Create the main window
    global createRoot
    createRoot = tk.Toplevel(root)
    createRoot.title("Tkinter Button Example")
    createRoot.geometry("300x200")

    # Create buttons
    button1 = tk.Button(createRoot, text="Horizontal", command=onButton1Click)
    button1.pack(pady=10)

    button2 = tk.Button(createRoot, text="Vertical", command=onButton2Click)
    button2.pack(pady=10)

def onButton1Click():
    global graph1
    graph1 = graph.Graph()
    graph1.create(sliderSize.get(), sliderWidth.get(), sliderRandomness.get(),sliderNodeRandomness.get(),1)
    print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections")
    createRoot.destroy()
    editButton()

def onButton2Click():
    global graph1
    graph1 = graph.Graph()
    graph1.create(sliderSize.get(), sliderWidth.get(), sliderRandomness.get(),sliderNodeRandomness.get(),2)
    print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections")
    createRoot.destroy()
    editButton()


def editButton():
    editor = tk.Tk()
    graphEditor = graphVisual.graph1Editor(editor, graph1)
    editor.mainloop()

def goButton():
    figList = iterate()
    displayPlot(figList[0])

def backward(event):
    global count
    if count == 0:
        tk.messagebox.showinfo("Error","No previous step")
    else:
        count-=1
        displayPlot(figList[count])

def forward(event):
    global count
    if count == len(figList)-1:
        tk.messagebox.showinfo("Error","No further step")
    else:
        count+=1
        displayPlot(figList[count])

def end():
    global count
    count = len(figList)-1
    displayPlot(figList[count])



#tkinter window
root = tk.Tk()
root.title("Network Visualizer")
root.geometry("854x480")

#main frame
mainFrame = ttk.Frame(root)
mainFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

#output frame
plotFrame = ttk.Frame(mainFrame, width=400, height=400, relief=tk.SUNKEN, borderwidth=2)
plotFrame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")
plotFrame.grid_propagate(False)  # Prevent the frame from resizing automatically

#left control panel
controlFrame = ttk.Frame(mainFrame)
controlFrame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

#graph size
labelSize = tk.Label(controlFrame, text="Network Height:")
labelSize.grid(row=1, column=0, pady=(10, 0), sticky="w")
sliderSize = tk.Scale(controlFrame, from_=3, to=20, resolution=2, orient="horizontal")
sliderSize.grid(row=2, column=0, pady=(0, 10), sticky="ew")


labelSizeW = tk.Label(controlFrame, text="Network Width:")
labelSizeW.grid(row=3, column=0, pady=(10, 0), sticky="w")
sliderWidth = tk.Scale(controlFrame, from_=3, to=20, resolution=2, orient="horizontal")
sliderWidth.grid(row=4, column=0, pady=(0, 10), sticky="ew")

#randomness slider
labelRandomness = tk.Label(controlFrame, text="Weighting Randomness:")
labelRandomness.grid(row=5, column=0, pady=(10, 0), sticky="w")
sliderRandomness = tk.Scale(controlFrame, from_=1, to=10, orient="horizontal")
sliderRandomness.grid(row=6, column=0, pady=(0, 10), sticky="ew")

labelNodeRandomness = tk.Label(controlFrame, text="Position Randomness:")
labelNodeRandomness.grid(row=7, column=0, pady=(10, 0), sticky="w")
sliderNodeRandomness = tk.Scale(controlFrame, from_=1, to=10, orient="horizontal")
sliderNodeRandomness.grid(row=8, column=0, pady=(0, 10), sticky="ew")

#create graph button
button = ttk.Button(controlFrame, text="Graph Create", command=createButton)
button.grid(row=9, column=0, pady=10, sticky="ew")

#generate button
button = ttk.Button(controlFrame, text="Generate Plot", command=goButton)
button.grid(row=11, column=0, pady=10, sticky="ew")

#skip to end button
button = ttk.Button(controlFrame, text="Result", command=end)
button.grid(row=13, column=0, pady=10, sticky="ew")

#create canvas to display result
canvas = None
figList = []
count = 0

#window resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#keybinds to flick through result
root.bind("<Right>", forward)
root.bind("<Left>", backward)

mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)

#run application
root.mainloop()





