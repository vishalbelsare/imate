# =======
# Imports
# =======

import numpy
import scipy

# ==========================
# Lanczos Tridiagonalization
# ==========================

def LanczosTridiagonalization(A,w,m,Tolerance=1e-8):
    """
    Tridiagonalizes matrix ``A`` to ``T`` using the start vector ``w``. ``m`` is the Lanczos
    degree, which will be the size of square matrix ``T``.

    .. note::

        * ``A`` should be symmetric and positive-definite matrix size ``n*n``.
        * ``T`` will be symmetric and positve-definite matrix of size ``(m+1,m+1)``.

    :param A: Input matrix of the size ``n*n``. Matrix should be positive-definite and symmetric.
    :type A: ndarray

    :param w: Start vector for the Lanczos tri-diagonalization. Column vector of size ``n``.
        It could be generated randomly. Often it is generated by the Rademacher distribution with entries ``+1`` and ``-1``.
    :type w: array

    :param m: Lanczos degree, which is the number of Lanczos iterations.
    :type m: int

    :param Tolerance: The tolerance of the residial error of the Lanczos iteration.
    :type Tolerance: float

    :return: Symmetric positive-definite matric ``T`` of the size ``(m+1)*(m+1)``.
    :rtype: ndarray
    """

    # Normalize random vector
    Norm = numpy.linalg.norm(w)
    v = w/Norm

    beta = 0
    n = A.shape[0]
    V = numpy.zeros((n,m+1))
    T = numpy.zeros((m+1,m+1))
    V[:,0] = v
    v_old = v

    wn = 0.0

    # Loop through Lanczos degrees
    for j in range(m):

        # Compute A*v depending if A is sparse or dense
        if scipy.sparse.isspmatrix(A):
            w = A.dot(v)
        else:
            w = numpy.dot(A,v)

        w = w - beta*v_old
        alpha = numpy.dot(w,v)
        wn += alpha**2
        T[j,j] = alpha
        w = w - alpha*v

        t1 = numpy.matmul(V[:,:j+1].T,w)
        w = w - numpy.matmul(V[:,:j+1],t1)
        beta = numpy.linalg.norm(w)**2

        # Exit criterion
        if beta*(j+1) < Tolerance:
            break

        wn += 2.0*beta
        beta = numpy.sqrt(beta)
        v_old = v
        v = w/beta
        V[:,j+1] = v
        T[j,j+1] = beta
        T[j+1,j] = beta

    return T

# ============================
# Lanczos Tridiagonalization 2
# ============================

def LanczosTridiagonalization2(A,v,m,Tolerance=1e-8):
    """
    Tridiagonalizes matrix ``A`` to ``T`` using the start vector ``v``. ``m`` is the Lanczos
    degree, which will be the size of square matrix ``T``.

    .. note::

        * ``A`` should be symmetric and positive-definite matrix size ``n*n``.
        * ``T`` will be symmetric and positve-definite matrix of size ``(m+1,m+1)``.

    Reference
        *Templates for solution of Algebraic Eigenvalue Problems*, James Demmel, p.57

    :param A: Input matrix of the size ``n*n``. Matrix should be positive-definite and symmetric.
    :type A: ndarray

    :param v: Start vector for the Lanczos tri-diagonalization. Column vector of size ``n``.
        It could be generated randomly. Often it is generated by the Rademacher distribution with entries ``+1`` and ``-1``.
    :type v: array

    :param m: Lanczos degree, which is the number of Lanczos iterations.
    :type m: int

    :param Tolerance: The tolerance of the residial error of the Lanczos iteration.
    :type Tolerance: float

    :return: Symmetric positive-definite matric ``T`` of the size ``(m+1)*(m+1)``.
    :rtype: ndarray
    """

    beta = numpy.zeros(m+1)
    alpha = numpy.zeros(m)
    T = numpy.zeros((m,m))

    n = v.size
    V = numpy.zeros((n,m))

    r = numpy.copy(v)
    beta[0] = numpy.linalg.norm(r)

    # In the following, beta[j] means beta[j-1] in the Demmel text
    for j in range(m):

        V[:,j] = r / beta[j]

        # Matrix-vector multiplication
        if scipy.sparse.isspmatrix(A):
            r = A.dot(V[:,j])
        else:
            r = numpy.dot(A,V[:,j])

        if j > 0:
            r = r - V[:,j-1]*beta[j]

        alpha[j] = numpy.dot(V[:,j],r)

        r = r - V[:,j]*alpha[j]

        beta[j+1] = numpy.linalg.norm(r)

        # Exit if beta got very small
        if beta[j+1]*(j+1) < Tolerance:
            return T[:j+1,:j+1]

        T[j,j] = alpha[j]
        if j < m-1:
            T[j,j+1] = beta[j+1]
            T[j+1,j] = beta[j+1]

    return T

# ====================================
# Golub Kahn Lanczos Bidiagonalization
# ====================================

def GolubKahnLanczosBidiagonalization(A,w,m,Tolerance=1e-8):
    """
    Inputs:
        A: symmetric matrix, n*n
        w: a random vector, n*1
        m: Lanczos degree of bidoagonalization, scalar.

    Output:
        B: symmetric matrix, upper bidiagonal, (m+1)*(m+1)

    .. note::

        * ``A`` should be symmetric and positive-definite matrix size ``n*n``.
        * ``B`` will be symmetric and positve-definite matrix of size ``(m+1,m+1)``.


    Bidiagonalizes matrix ``A`` to ``B`` using the start vector ``w``. ``m`` is the Lanczos
    degree, which will be the size of square matrix ``B``.

    Reference
        * NetLib `Algorithm 6.27 <http://www.netlib.org/utk/people/JackDongarra/etemplates/node198.html>`_
        * Matrix Computations, Golub, p. 495
        * Templates for Solution of Algebraic Eigenvalue Problem, Demmel, p. 143

    Issues:
        When matrix ``A`` is very close to the identity matrix, the Golub-Kahn bidoagonalization method can not 
        find :math:`\\beta`, as :math:`\\beta` becomes zero. If ``A`` is not exactly identity, you may descrease the Tolerance
        to a very small number. However, if ``A`` is almost identity matrix, descreasing tolerance will not 
        help, and this function cannot be used.

    :param A: Input matrix of the size ``n*n``. Matrix should be positive-definite and symmetric.
    :type A: ndarray

    :param w: Start vector for the Lanczos tri-diagonalization. Column vector of size ``n``.
        It could be generated randomly. Often it is generated by the Rademacher distribution with entries ``+1`` and ``-1``.
    :type w: array

    :param m: Lanczos degree, which is the number of Lanczos iterations.
    :type m: int

    :param Tolerance: The tolerance of the residial error of the Lanczos iteration.
    :type Tolerance: float

    :return: Symmetric positive-definite matric ``B`` of the size ``(m+1)*(m+1)``.
    :rtype: ndarray
    """

    # Normalize random vector
    Norm = numpy.linalg.norm(w)
    v = w/Norm

    beta = numpy.zeros(m+1)
    alpha = numpy.zeros(m)
    B = numpy.zeros((m,m))

    # u = numpy.zeros(w.size)
    # beta[0] = 1
    # p = numpy.copy(v)

    # for k in range(m):

    #     v_old = numpy.copy(v)
    #     u_old = numpy.copy(u)

    #     v = p / beta[k]

    #     r = A.dot(v_old) - beta[k]*u_old

    #     alpha[k] = numpy.linalg.norm(r)

    #     u = r/alpha[k]
    #     p = A.T.dot(u) - alpha[k]*v
    #     beta[k+1] = numpy.linalg.norm(p)

    #     if beta[k+1] < Tolerance:
    #         return B[:k,:k]
    #     
    #     # Update B
    #     B[k,k] = alpha[k]

    #     if k < m-1:
    #         B[k,k+1] = beta[k+1]

    # return B

    beta[0] = 0

    v_old = numpy.copy(v)

    for k in range(m):

        if k == 0:
            u_new = A.dot(v_old)
        else:
            u_new = A.dot(v_old) - beta[k]*u_old

        alpha[k] = numpy.linalg.norm(u_new)
        u_new = u_new / alpha[k]

        v_new = A.T.dot(u_new) - alpha[k]*v_old
        beta[k+1] = numpy.linalg.norm(v_new)

        # Exit criterion
        if beta[k+1] < Tolerance:
            if k == 0:
                # raise ValueError('Premature exit at k = 0. beta[0:2] = %0.16f, %0.16f. This happens when A is close to identity. To resolve issue, decrease Tolerance: %f'%(beta[0],beta[1],Tolerance))
                print('Premature exit in Golub-Kahn-Lanczos bi-diagonalization. alpha: %e, beta: %e'%(alpha[0],beta[1]))
                B = numpy.array([[alpha[0]]])
                return B
            return B[:k,:k]

        v_new = v_new / beta[k+1]

        # Store to the output matrix
        B[k,k] = alpha[k]
        if k < m-1:
            B[k,k+1] = beta[k+1]

        # Update for new iteration
        v_old = numpy.copy(v_new)
        u_old = numpy.copy(u_new)

    return B