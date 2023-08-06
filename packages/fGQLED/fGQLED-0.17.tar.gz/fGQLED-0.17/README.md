# READER:
    Function which reads out different files. 
## Arguments
    Takes everything in **kwargs.
   * 'filename': Filename + Path. Necessary. [String or Chararray]
   * 'Delimiter': Input for the delimitation. e.g. ', ', '\t ', or other types. Standard is ' '. [Single Character]
   * 'allowedChars': Set the allowed characters for the first character in a line. Can be used if line begins with a prefix or with a number. Standard are the numbers 0-10. [List]
   * 'skipLines': Number of lines to be skipped in the file. Useful if the text document starts with lines containing allowed characters but no data. [int]
   * 'flatten': Check if the resulting array has not the same number of arguments on each line. Select length of line which should pass (all other won't). [int]
   * 'datatype': datatype of read file. 'complex', 'float'
## Output
    File is read and returned as an array of values.
    First index is line number and second index is the position on line.
    
# COLORS
    Function for colors
## Arguments
    Takes Literals as arguments
  * N: Number of cmap points
  * cmap_name: Name of the colormap
## Output
    Returns colormaps in array of RGB colors. First index is the color, and the second index selects the spectral component in R, G, B, alpha
   
# Figurefunctions
    Functions to format the figure.
## Arguments
    Takes literals as arguments
   * ax: Axis of figure to be formated. Necessary
   * projection: '2d', '3d' or 'contour' plot. Standard:  '2d' [string or chararray]
   * labels: Dictionary with labels. keys of the dictionary: 'xlabel', 'ylabel', 'zlabel'. If one of those labels is not set, will be set to empty. Standard: {'xlabel': '', 'ylabel': '', 'zlabel': ''} [Dict]
   * fontsize: Fontsize of the axis labels. Standard: 14 [int]
   * ticksize: Fontsize of the tick labels. Standard: 14 [int]
   * ticksepeartionx: Set the spacing between the x-ticks. e.g. 2 will select every second tick to be labeled. Standard: 2 [int] 
   * ticksepeartiony: Set the spacing between the y-ticks. e.g. 2 will select every second tick to be labeled. Standard: 2 [int] 
   * tickoffsetx: offsets the tick-selection in x-direction.  Standard: 0 [int, in 0 to tickseparationx]
   * tickoffsety: offsets the tick-selection in y-direction.  Standard: 0 [int, in 0 to tickseparationy]
## Output
    Axis is processed and returned. 
# Plotter
    Function for Plotting. 
## Arguments
    Takes kwargs as arguments
   * 'SweepType': '1D': Only one x and y, 'Multiple': Overlay multiple x and y tuples, '2D': Plots a contourf plot of the x, y and z
   * 'scale': 'lin' or 'log'
   * 'Constrain': Argument to constrain the axes, dictionary.
        * 'Bool': False or True: disables or enables the function
        * 'xlim_min/max': Min/max of x-axis. [int, float]
        * 'ylim_min/max': Min/max of y-axis. [int, float]
   * ticksepeartionx: Set the spacing between the x-ticks. e.g. 2 will select every second tick to be labeled. Standard: 2 [int] 
   * ticksepeartiony: Set the spacing between the y-ticks. e.g. 2 will select every second tick to be labeled. Standard: 2 [int] 
   * tickoffsetx: offsets the tick-selection in x-direction.  Standard: 0 [int, in 0 to tickseparationx]
   * tickoffsety: offsets the tick-selection in y-direction.  Standard: 0 [int, in 0 to tickseparationy]
   * 'legend': Bool, shows legend
   * 'show': Bool, Show image or not. Std is show.