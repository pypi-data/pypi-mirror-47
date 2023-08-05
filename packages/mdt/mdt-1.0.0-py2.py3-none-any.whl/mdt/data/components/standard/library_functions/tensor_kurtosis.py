from mdt import LibraryFunctionTemplate

__author__ = 'Robbert Harms'
__date__ = '2018-10-11'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert.harms@maastrichtuniversity.nl'
__licence__ = 'LGPL v3'


class TensorApparentDiffusion(LibraryFunctionTemplate):
    """Calculates the apparent diffusion for the Tensor model.

    Args:
        theta: polar angle of the first vector
        phi: azimuth angle of the first vector
        psi: rotation around the first vector, used to generate the perpendicular vectors.
        d: first eigenvalue
        dperp0: second eigenvalue
        dperp1: third eigenvalue
    """
    dependencies = ['TensorSphericalToCartesian']
    return_type = 'mot_float_type'
    parameters = ['mot_float_type theta', 'mot_float_type phi', 'mot_float_type psi',
                  'mot_float_type d', 'mot_float_type dperp0', 'mot_float_type dperp1', 'float4 g']
    cl_code = '''
        float4 vec0, vec1, vec2;
        TensorSphericalToCartesian(theta, phi, psi, &vec0, &vec1, &vec2);

        return  d *      pown(dot(vec0, g), 2) +
                dperp0 * pown(dot(vec1, g), 2) +
                dperp1 * pown(dot(vec2, g), 2);
    '''


class KurtosisMultiplication(LibraryFunctionTemplate):
    """Performs the multiplication of the Kurtosis matrix with a vector.

    This performs the sum of n_i * n_j * n_k * n_l * W_ijkl.

    This requires the lower triangular matrix of the Kurtosis matrix W and a direction vector.

    Args:
        'W*' (double): the matrix elements.
        n (float4): the vector to evaluate the Kurtosis matrix against.

    Returns:
        double: the evaluated scalar.
    """
    return_type = 'double'
    parameters = ['mot_float_type W_0000', 'mot_float_type W_1111', 'mot_float_type W_2222',
                  'mot_float_type W_1000', 'mot_float_type W_2000', 'mot_float_type W_1110',
                  'mot_float_type W_2220', 'mot_float_type W_2111', 'mot_float_type W_2221',
                  'mot_float_type W_1100', 'mot_float_type W_2200', 'mot_float_type W_2211',
                  'mot_float_type W_2100', 'mot_float_type W_2110', 'mot_float_type W_2210',
                  'float4 n']
    cl_code = '''
        double kurtosis_sum = 0;

        kurtosis_sum += n.x * n.x * n.x * n.x * W_0000;
        kurtosis_sum += n.y * n.y * n.y * n.y * W_1111;
        kurtosis_sum += n.z * n.z * n.z * n.z * W_2222;

        kurtosis_sum += n.y * n.x * n.x * n.x * W_1000 * 4;
        kurtosis_sum += n.z * n.x * n.x * n.x * W_2000 * 4;
        kurtosis_sum += n.y * n.y * n.y * n.x * W_1110 * 4;
        kurtosis_sum += n.z * n.z * n.z * n.x * W_2220 * 4;
        kurtosis_sum += n.z * n.y * n.y * n.y * W_2111 * 4;
        kurtosis_sum += n.z * n.z * n.z * n.y * W_2221 * 4;

        kurtosis_sum += n.y * n.y * n.x * n.x * W_1100 * 6;
        kurtosis_sum += n.z * n.z * n.x * n.x * W_2200 * 6;
        kurtosis_sum += n.z * n.z * n.y * n.y * W_2211 * 6;

        kurtosis_sum += n.z * n.y * n.x * n.x * W_2100 * 12;
        kurtosis_sum += n.z * n.y * n.y * n.x * W_2110 * 12;
        kurtosis_sum += n.z * n.z * n.y * n.x * W_2210 * 12;

        return kurtosis_sum;
    '''
