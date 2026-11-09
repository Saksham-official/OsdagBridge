"""
styles.py — Centralized Formatting & Style System for OsdagBridge Reports
========================================================================
Single source of truth for:
  • Color palettes (Osdag branding, IITB, status indicators)
  • Page geometry and layout boundaries
  • Table styling (padding, rules, row stretch, buffers)
  • Typography and document classes
  • Chart generation aesthetics
"""

from dataclasses import dataclass


# ── 1. Color Palette (Single Source of Truth) ─────────────────────────────────
class ColorPalette:
    """Official Osdag & IIT Bombay branding and engineering status colors."""
    OSDAG_GREEN = "#91B014"
    IITB_BLUE = "#1565C0"
    DARK_GRAY = "#333333"
    LIGHT_GRAY = "#F8F9FA"
    ROW_BG = "#F5F5F5"
    BORDER_GRAY = "#D3D3D3"

    # Status / Chart colors
    PASS_GREEN = "#2E7D32"
    FAIL_RED = "#D32F2F"
    WARNING_AMBER = "#F57C00"
    NEUTRAL_GRAY = "#555555"

    # BOQ Element Colors
    STEEL_GIRDER = "#1565C0"
    STEEL_BRACING = "#1E88E5"
    STEEL_DIAPHRAGM = "#42A5F5"
    CONCRETE_DECK = "#43A047"
    REBAR_STEEL = "#E53935"


# ── 2. Page Geometry & Margin Configuration ───────────────────────────────────
@dataclass(frozen=True)
class PageGeometry:
    """
    Task 2: Layout & Footer Overlap Fixes.
    Explicit geometry ensuring tables never bleed into the footer margin.
    """
    paper_size: str = "a4paper"
    top_mm: int = 25
    bottom_mm: int = 32
    left_mm: int = 22
    right_mm: int = 22
    headheight_pt: int = 18
    headsep_mm: int = 8
    footskip_mm: int = 14

    def to_latex(self) -> str:
        return (
            r"\usepackage["
            + f"{self.paper_size}, "
            + f"top={self.top_mm}mm, "
            + f"bottom={self.bottom_mm}mm, "
            + f"left={self.left_mm}mm, "
            + f"right={self.right_mm}mm, "
            + f"headheight={self.headheight_pt}pt, "
            + f"headsep={self.headsep_mm}mm, "
            + f"footskip={self.footskip_mm}mm"
            + r"]{geometry}"
        )


# ── 3. Table Layout & Cell Padding Rules ─────────────────────────────────────
@dataclass(frozen=True)
class TableStyle:
    tabcolsep_pt: float = 5.0
    arraystretch: float = 1.10
    arrayrulewidth_pt: float = 0.5
    extrarowheight_pt: float = 0.5
    lt_pre_pt: float = 2.0
    lt_post_pt: float = 6.0
    needspace_lines: int = 7

    def to_latex(self) -> str:
        return (
            r"% Table layout and spacing (Centralized Style System)" + "\n"
            + rf"\setlength{{\tabcolsep}}{{{self.tabcolsep_pt}pt}}" + "\n"
            + rf"\renewcommand{{\arraystretch}}{{{self.arraystretch:.2f}}}" + "\n"
            + rf"\setlength{{\LTpre}}{{{self.lt_pre_pt}pt}}" + "\n"
            + rf"\setlength{{\LTpost}}{{{self.lt_post_pt}pt}}" + "\n"
            + rf"\setlength{{\arrayrulewidth}}{{{self.arrayrulewidth_pt}pt}}" + "\n"
            + rf"\setlength{{\extrarowheight}}{{{self.extrarowheight_pt}pt}}" + "\n\n"
            + r"% Buffer threshold: prevent orphan tables and footer bleed" + "\n"
            + rf"\BeforeBeginEnvironment{{table}}{{\needspace{{{self.needspace_lines}\baselineskip}}}}" + "\n"
            + rf"\BeforeBeginEnvironment{{longtable}}{{\needspace{{{self.needspace_lines}\baselineskip}}}}"
        )


# ── 4. Typography & Document Settings ────────────────────────────────────────
@dataclass(frozen=True)
class TypographyConfig:
    doc_class: str = "report"
    font_size_pt: int = 12
    line_spacing: float = 1.15

    def to_latex(self) -> str:
        return (
            rf"\documentclass[{self.font_size_pt}pt,a4paper]{{{self.doc_class}}}" + "\n"
            + rf"\setstretch{{{self.line_spacing:.2f}}}"
        )


# ── 5. Chart Visual Configurations ───────────────────────────────────────────
class ChartTheme:
    DPI = 250
    FIGURE_WIDTH = 1600
    FIGURE_HEIGHT_UR = 920
    FIGURE_HEIGHT_BOQ = 780
    FONT_FAMILY = "arial.ttf"
    FONT_BOLD = "arialbd.ttf"
    THRESHOLD_COLOR = ColorPalette.FAIL_RED
    PASS_COLOR = ColorPalette.PASS_GREEN
    GRID_COLOR = "#EEEEEE"


# ── Global Default Instances ─────────────────────────────────────────────────
DEFAULT_GEOMETRY = PageGeometry()
DEFAULT_TABLE_STYLE = TableStyle()
DEFAULT_TYPOGRAPHY = TypographyConfig()


def get_preamble(
    project_name: str,
    job_number: str,
    report_date: str,
    report_version: str = "Rev 0",
    geometry: PageGeometry = DEFAULT_GEOMETRY,
    table_style: TableStyle = DEFAULT_TABLE_STYLE,
    typography: TypographyConfig = DEFAULT_TYPOGRAPHY
) -> str:
    """
    Centralized preamble generator consuming single-source styling attributes.
    """
    from osdagbridge.core.reports.report_utils import _tex
    pn = _tex(project_name)
    jn = _tex(job_number)
    rd = _tex(report_date)
    rv = _tex(report_version)

    preamble_blocks = [
        typography.to_latex(),
        "",
        "% Packages",
        geometry.to_latex(),
        r"\usepackage{graphicx}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\usepackage{booktabs}",
        r"\usepackage{array}",
        r"\usepackage{tabularx}",
        r"\usepackage{float}",
        r"\usepackage{fancyhdr}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\usepackage{xcolor}",
        r"\usepackage{setspace}",
        r"\usepackage{enumitem}",
        r"\usepackage{caption}",
        "",
        r"\captionsetup{",
        r"    labelfont=bf,",
        r"    justification=raggedright,",
        r"    singlelinecheck=false,",
        r"    format=plain",
        r"}",
        r"\usepackage{subcaption}",
        r"\usepackage{multirow}",
        r"\usepackage{colortbl}",
        r"\usepackage{longtable}",
        r"\setlength{\LTleft}{\fill}",
        r"\setlength{\LTright}{\fill}",
        r"\usepackage{titlesec}",
        r"\usepackage{titletoc}",
        r"\usepackage{lastpage}",
        r"\usepackage{makecell}",
        r"\usepackage{etoolbox}",
        r"\usepackage{needspace}",
        "",
        r"\numberwithin{table}{chapter}",
        r"\numberwithin{figure}{chapter}",
        "",
        table_style.to_latex(),
        "",
        rf"\definecolor{{osdagGreen}}{{HTML}}{{{ColorPalette.OSDAG_GREEN.lstrip('#')}}}",
        rf"\definecolor{{iitbBlue}}{{HTML}}{{{ColorPalette.IITB_BLUE.lstrip('#')}}}",
        rf"\definecolor{{passGreen}}{{HTML}}{{{ColorPalette.PASS_GREEN.lstrip('#')}}}",
        rf"\definecolor{{failRed}}{{HTML}}{{{ColorPalette.FAIL_RED.lstrip('#')}}}",
        "",
        r"\fancypagestyle{main}{",
        r"  \fancyhf{}",
        rf"  \fancyhead[L]{{{pn} $|$ {jn}}}",
        rf"  \fancyhead[R]{{{rd} $|$ {rv}}}",
        r"  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}",
        r"  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}",
        r"  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{2pt}}",
        r"  \renewcommand{\footrule}{%",
        r"    \ifbool{hasSDonPage}{%",
        r"      \vspace{-12pt}%",
        r"      \hbox to \headwidth{\textcolor{black}{\footnotesize\textit{* Software default value}}\hfil}%",
        r"      \vspace{2pt}%",
        r"    }{%",
        r"      \vspace{-4pt}%",
        r"    }%",
        r"    \color{osdagGreen}\hrule width\headwidth height 1pt \vspace{4pt}%",
        r"  }",
        r"}",
        "",
        r"\fancypagestyle{plain}{",
        r"  \fancyhf{}",
        rf"  \fancyhead[L]{{{pn} $|$ {jn}}}",
        rf"  \fancyhead[R]{{{rd} $|$ {rv}}}",
        r"  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}",
        r"  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}",
        r"  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{2pt}}",
        r"  \renewcommand{\footrule}{%",
        r"    \ifbool{hasSDonPage}{%",
        r"      \vspace{-12pt}%",
        r"      \hbox to \headwidth{\textcolor{black}{\footnotesize\textit{* Software default value}}\hfil}%",
        r"      \vspace{2pt}%",
        r"    }{%",
        r"      \vspace{-4pt}%",
        r"    }%",
        r"    \color{osdagGreen}\hrule width\headwidth height 1pt \vspace{4pt}%",
        r"  }",
        r"}",
        "",
        r"\fancypagestyle{firstpage}{",
        r"  \fancyhf{}",
        r"  \renewcommand{\headrulewidth}{0pt}",
        r"  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}",
        r"  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}",
        r"  \renewcommand{\footrule}{\vspace{-8pt}\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{6pt}}",
        r"}",
        "",
        r"\pagestyle{main}",
        rf"\setstretch{{{typography.line_spacing:.2f}}}",
        "",
        r"% Custom Commands",
        r"\newcommand{\placeholder}[1]{\textit{\textless #1\textgreater}}",
        r"\newcommand{\todo}[1]{\colorbox{yellow}{TODO: #1}}",
        r"\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}",
        r"\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}",
        r"\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}",
        "",
        r"% Software-default asterisk",
        r"\newcommand{\sdstar}{\textsuperscript{*}}",
        r"\newbool{hasSDonPage}",
        r"\boolfalse{hasSDonPage}",
        r"\newcommand{\markSD}{\global\booltrue{hasSDonPage}}",
        r"\renewcommand{\sdstar}{\textsuperscript{*}\markSD{}}",
        r"\AddToHook{shipout/before}{\global\boolfalse{hasSDonPage}}",
        "",
        r"\title{\Large\textbf{OsdagBridge} \\ \normalsize Open Source Software for Steel Girder Bridge Design \\ \vspace{2cm} \large Design Report}",
        r"\author{}",
        r"\date{}",
        "",
        r"\begin{document}"
    ]

    return "\n".join(preamble_blocks)
