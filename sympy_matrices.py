
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
from main import run_pyqt
import sympy as sp
from IPython.lib.latextools import latex_to_png
from IPython.display import Image, display
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib as mpl
from sympy.printing import latex
mpl.rcParams.update(mpl.rcParamsDefault)
# sp.init_printing(use_latex='mathjax')

def tex2svg(formula, fontsize=12, dpi=300):
    """Render TeX formula to SVG.
    Args:
        formula (str): TeX formula.
        fontsize (int, optional): Font size.
        dpi (int, optional): DPI.
    Returns:
        str: SVG render.
    """

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

    output = BytesIO()
    fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                bbox_inches='tight', pad_inches=0.0, frameon=False)
    plt.close(fig)

    output.seek(0)
    return output.read()

lens = Lens(name = 'Lens', z = 1.0)
astig_lens = AstigmaticLens(name = 'Astigmatic Lens', z = 1.2)
quad = Quadrupole(name = 'Quadrupole', z = 0.9)
double_def = DoubleDeflector(name = 'Double Deflector', z_up = 0.70, z_low = 0.65)
deflector = Deflector(name = 'Deflector', z = 0.6, defx = 0, defy = 0)
biprism = Biprism(name = 'Biprism', z = 0.4)
aperture = Aperture(name = 'Aperture', z = 0.1, aperture_radius_inner = 0.05)

f, fx, fy, dx, dy, M_l, M_al, M_q, M_d = sp.symbols('f f_x f_y d_x d_y M_l, M_al, M_q, M_d')
lens_matrix = sp.Matrix(lens.lens_matrix(f))
lens_matrix_eq = sp.Eq(M_l, lens_matrix, evaluate = False)
#latex_lens = latex(lens_matrix_eq)
latex_lens = r'M_{l} = \left[\begin{matrix}1 & 0 & 0 & 0 & 0\\- \frac{1}{f} & 1 & 0 & 0 & 0\\0 & 0 & 1 & 0 & 0\\0 & 0 & - \frac{1}{f} & 1 & 0\\0 & 0 & 0 & 0 & 1\end{matrix}\right]'
data = tex2svg(latex_lens)
display(Image(data=data))