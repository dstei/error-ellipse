import numpy as np
from scipy.stats import chi2, multivariate_normal
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def get_error_ellipse_parameters(cov, confidence=None, sigma=None):
    """Returns parameters of an ellipse which contains a specified
    amount of normally-distributed 2D data, where the data is
    characterised by its covariance matrix.
    
    Parameters
    ----------
    cov : array_like
        Input covariance matrix of shape (2,2)
    confidence : float
        Fraction of data points within ellipse. 0 < confidence < 1.
        If confidence is not given, it is calculated according to sigma.
    sigma : float
        Length of axes of the ellipse in standard deviations. If 
        confidence is also given, sigma is ignored.
    
    Returns
    -------
    semi_major : float
        Length of major semiaxis of ellipse.
    semi_minor : float
        Length of minor semiaxis of ellipse.
    angle : float
        Rotation angle of ellipse in radian.
    confidence : float
        Fraction of data expected to lie within the ellipse.
    sigma : float
        Length of major and minor semiaxes in standard deviations.
    """
    cov = np.array(cov)
    if(cov.shape != (2,2)):
        raise ValueError("The covariance matrix needs to be of shape (2,2)")
    if(confidence == None and sigma == None):
        raise RuntimeError("One of confidence or sigma is needed as argument")
    if(confidence and sigma):
        print("Argument sigma is ignored as confidence is also provided!")
    
    if(confidence == None):
        if(sigma < 0):
            raise ValueError("Sigma needs to be positive")
        confidence = chi2.cdf(sigma, 2)
    if(sigma == None):
        if(confidence > 1 or confidence < 0):
            raise ValueError("Ensure that confidence lies between 0 and 1")
        sigma = chi2.ppf(confidence, 2)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    
    maxindex = np.argmax(eigenvalues)
    vx, vy = eigenvectors[:, maxindex]
    angle = np.arctan2(vy, vx)
    semi_minor, semi_major = np.sqrt(np.sort(eigenvalues) * sigma)
    print("With sigma = {:.2f}, {:.1f}% of data points lie within ellipse.".format(sigma, confidence * 100))

    return semi_major, semi_minor, angle, confidence, sigma

if(__name__ == "__main__"):
    mean_x, mean_y = 5, -2
    covariance = [[1, -2.04], [-2.04, 5.16]]

    rv = multivariate_normal([mean_x, mean_y], covariance)
    data_points = rv.rvs(size = 500)

    fig = plt.figure()
    ax = fig.gca()
    plt.scatter(data_points[:,0], data_points[:,1], alpha = .5)

    confidence = 0.95
    semi_major, semi_minor, angle, sigma, confidence\
        = get_error_ellipse_parameters(covariance, confidence = confidence)
    ax.add_patch(Ellipse((mean_x, mean_y), 2*semi_major, 2*semi_minor, 180*angle/np.pi, facecolor = 'none', edgecolor='red'))

    sigma = 1
    semi_major, semi_minor, angle, sigma, confidence\
        = get_error_ellipse_parameters(covariance, sigma = sigma)
    ax.add_patch(Ellipse((mean_x, mean_y), 2*semi_major, 2*semi_minor, 180*angle/np.pi, facecolor = 'none', edgecolor='yellow'))
    fig.savefig('plot.png')    
    plt.show()
