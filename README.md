# error-ellipse
![Example plot with data and error ellipses](plot.png?raw=true)

A covariance matrix completely determines the statistics of two normally-distributed variables. The script `error_ellipse.py` provides a function using the covariance matrix to calculate major and minor axes of an error ellipse and the rotation angle of that ellipse. Inputs determining the size of the ellipse are: either the confidence as the fraction of data to lie within the ellipse, or sigma as the size of the ellipse in terms of the standard deviations. The above example calculates two ellipses, one with a confidence of 95%, and one with a sigma of 1.

## The math behind it
An ellipse is determined by the elliptical equation,

<img src="https://render.githubusercontent.com/render/math?math=(\frac{x}{\sigma_x})^2 %2B (\frac{y}{\sigma_y})^2 = s">,

or, more generally for correlated data with a covariance matrix having off-diagonal elements,

<img src="https://render.githubusercontent.com/render/math?math=(x, y)C^{-1} (x\atop y) = s">

with the covariance matrix C and a scaling parameter s (s is the square of sigma from above).

The scaling parameter s is chi-square distributed (sum of two Gaussian variables). This distribution can be used to obtain a scaling factor leading to a certain specified amount of data lying within the ellipse.
For a more detailed explanation, see for example [visiondummy's article](https://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/).

## Required
- For the function: `numpy`, `chi2` from `scipy.stats`.
- Additionally for the example plot: `matplotlib.pyplot`, `Ellipse` from `matplotlib.patches`, `multivariate_normal` from `scipy.stats`.
