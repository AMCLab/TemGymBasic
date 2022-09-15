
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
import sympy as sp

import matplotlib.pyplot as plt

import matplotlib as mpl
from sympy.printing import latex
import numpy as np

mpl.rcParams['font.size'] = 20
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

def propagate(z):
    
    matrix = np.array([[1, z, 0, 0, 0],
                       [0, 1, 0, 0, 0],
                       [0, 0, 1, z, 0],
                       [0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 1]])
    
    return matrix
    
def tex2svg(name, formula, fontsize=12, dpi=500):
    """Render TeX formula to SVG.
    Args:
        formula (str): TeX formula.
        fontsize (int, optional): Font size.
        dpi (int, optional): DPI.
    Returns:
        str: SVG render.
    """

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, r"${}$".format(formula), fontsize=fontsize)

    fig.savefig(name, dpi=dpi, transparent=True, format='svg',
                bbox_inches='tight', pad_inches=0.0, frameon=False)
    plt.show()
    plt.close(fig)

lens = Lens(name = 'Lens', z = 1.0)
astig_lens = AstigmaticLens(name = 'Astigmatic Lens', z = 1.2)
quad = Quadrupole(name = 'Quadrupole', z = 0.9)
double_def = DoubleDeflector(name = 'Double Deflector', z_up = 0.70, z_low = 0.65)
deflector = Deflector(name = 'Deflector', z = 0.6, defx = 0, defy = 0)
biprism = Biprism(name = 'Biprism', z = 0.4)
aperture = Aperture(name = 'Aperture', z = 0.1, aperture_radius_inner = 0.05)

f, fx, fy, dx, dy, M_lens, M_prop, M_stig, M_def, M_doubledef, z_prop, up_defx, up_defy, low_defx, low_defy = sp.symbols('f f_x f_y d_x d_y M_lens, M_prop, M_stig, M_def M_doubledef z_prop, up_defx up_defy low_defx low_defy')

lens_matrix = sp.Matrix(lens.lens_matrix(f))
lens_matrix_eq = sp.Eq(M_lens, lens_matrix, evaluate = False)
latex_ = latex(lens_matrix_eq)
print(latex_)

stig_matrix = sp.Matrix(quad.lens_matrix(fx, fy))
stig_matrix_eq = sp.Eq(M_stig, stig_matrix, evaluate = False)
latex_ = latex(stig_matrix_eq)
print(latex_)

def_matrix = sp.Matrix(deflector.deflector_matrix(dx, dy))
def_matrix_eq = sp.Eq(M_def, def_matrix, evaluate = False)
latex_ = latex(def_matrix_eq)
print(latex_)

# double_def_prop_matrix = sp.Matrix(propagate(z_prop))
# double_def_up_matrix = sp.Matrix(double_def.deflector_matrix(up_defx, up_defy))
# double_def_low_matrix = sp.Matrix(double_def.deflector_matrix(low_defx, low_defy))
# double_def_matrix_eq = sp.Eq(M_doubledef, double_def_low_matrix, evaluate = False)
# latex___ = latex(double_def_up_matrix)
# latex__ = latex(double_def_prop_matrix)
# latex_ = latex(double_def_matrix_eq)
# print(latex_)
# print(latex__)
# print(latex___)

double_def_prop_matrix = sp.Matrix(propagate(z_prop))
double_def_matrix = sp.Matrix(double_def.deflector_matrix(up_defx, up_defy)*double_def_prop_matrix*double_def.deflector_matrix(low_defx, low_defy))
double_def_matrix_eq = sp.Eq(M_doubledef, double_def_matrix, evaluate = False)
latex_ = latex(double_def_matrix_eq)
print(latex_)
