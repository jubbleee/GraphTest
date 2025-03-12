Fatigue Cracking Random Spring Model

The project is run through main.py, which generates the tKinter window for user interaction
Within this window, settings for the graph generation are presented:
    selecting desired a size (height and width) and randomness (position and weighting) must be done before creating graph
    pressing graph create button prompts the user with vertical or horizontal graph structure
    vertical aligns members of the graph parallel with the force whereas horizontal perpendicular
    once selected, connections may be removed in the popup graph menu via left click and nodes moved by dragging with right click
    it is advised that nodes are moved before connections removed to prevent a logical editing glitch

    this window may be closed when finished

    pressing generate will simulate the load across the network until failure, creating figures at each breakdown of a connection
    the original figure will load into the tKinter window when processing is finished and results can be navigated through with arrow keys
    the result button takes the user to the last figure in the sequence and the collapse of the network
    each figure may be zoomed in to using the scroll wheel for closer analysis of teh structure
    outputs for each figures count is displayed in the console and will require counting for identification

    the user can either close the program or generate a new graph with new settings depending on their needs.