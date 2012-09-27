from xdb.models import Browser,Suite,Test,Vector

__author__ = 'eal'

def gen_vertical_table(browsers,vectors):
    """
    generating a vertical browser / vector result matrix in latex
    """
    header="""
\documentclass{llncs}
\usepackage{llncsdoc}
\usepackage[latin1]{inputenc}
\usepackage{url}
\usepackage{verbatim}
\usepackage{multirow}
\usepackage{rotating}
\usepackage[table]{xcolor}
\\bibliographystyle{unsrt}

\\begin{document}\n
"""
    footer="\n\end{document}"
    result=""
    result+=header

    result+="\\begin{tabular}{|c"
    for b in browsers:
        result+="|c"
    result+="|}\n\hline\n"
    result+="\multicolumn{1}{|c|}{\n\\begin{sideways}\n"
    result+="""Vector / Browser \,
\end{sideways}}"""
    for b in browsers:
        result+="""& 
\multicolumn{1}{c|}{
\\begin{sideways}\n"""
        result+=b.desc
        result+=""" \,
\end{sideways}}"""
    result+="""\\\\\hline\n"""
    for v in vectors:
        result+=""+str(v.id)
        for b in browsers:
            t=Test.objects.filter(browser=b,vector=v)
            if t:
                t=t[0]
                if t.result:
                    result+=" & \cellcolor{black}\\textcolor{white}{1} "
                else:
                    result+=" & 0 "
            else:
                result+=" & 0 "
        result+="\\\\\hline\n"
    result+="\end{tabular}"
    result+=footer
    return result

def gen_horizontal_table(browsers,vectors):
    result = ""
    header="""
\documentclass{llncs}
\usepackage{llncsdoc}
\usepackage[latin1]{inputenc}
\usepackage{url}
\usepackage{verbatim}
\usepackage{multirow}
\usepackage{rotating}
\usepackage[table]{xcolor}
\\bibliographystyle{unsrt}

\\begin{document}\n
"""
    footer="\n\end{document}"
    result+=header
    result+="\\begin{tabular}{|c"
    for v in vectors:
        result+="|c"
    result+="|}\n\hline\n"
    result+="\multicolumn{1}{|c|}{"

    return result