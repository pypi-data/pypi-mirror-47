# TimeSeriesVisualization
Visualization of Time-Series with the Matrix Profile and Multidimensional Scaling - a Python Implementation.

## Introduction
Multidimensional scaling is an algorithm that projects a set of objects represented by their distance matrix into a lesser dimensional space, such that the pairwise distance is preserved as much as possible. If we project onto a 1-dimensional or a 2-dimensional space, we can even plot the resultant projections, and visually understand the similarity between these objects.  
At a first glance, this seems applicable to time-series as well, where we want to capture similar regions across the entire time-series.  
However, since we do not know apriori where our regions of interest are, we can simply select all subsequences of a given length from the original time-series.  
Let's try this out!


## References
<b>Matrix Profile III: The Matrix Profile Allows Visualization of Salient Subsequences in Massive Time Series</b>.    
Chin-Chia Michael Yeh, Helga Van Herle, and Eamonn Keogh. IEEE ICDM 2016.
