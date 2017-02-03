#!/usr/bin/env python
# encoding: utf-8
"""
File: bibjson2tex.py
Author: Jon Husson
Description: Converts a bibjson (http://okfnlabs.org/bibjson/) specified file
    into LaTeX .bib file. Also provides cite.bbl and references.tex file to convert the documents
    within the bibjson file into a PDF for ease of previewing.
Assumes: Valid bibjson input. If no filepath is specified as the first argument,
    it is assumed that the bibjson file is saved as ./data/bibjson.
Creates: ./output/bibtk.bib, ./output/cite.bbl, ./output/references.tex
Usage: bibjson2tex.py [bibjson]
"""

import os, sys
import json
import string
import codecs
import numpy as np

# map of unicode characters to their LaTeX equivalents
REPLACEMENT_MAP = {
        u"Α" : "A",
        u"Β" : "B",
        u"Γ" : "$\Gamma$",
        u"Δ" : "$\Delta$",
        u"Ε" : "E",
        u"Ζ" : "Z",
        u"Η" : "H",
        u"Θ" : "$\Theta$",
        u"Ι" : "I",
        u"Κ" : "K",
        u"Λ" : "$\Lambda$",
        u"Μ" : "M",
        u"Ν" : "N",
        u"Ξ" : "$\Xi$",
        u"Ο" : "O",
        u"Π" : "$\Pi$",
        u"Ρ" : "P",
        u"Σ" : "$\Sigma$",
        u"Τ" : "T",
        u"Υ" : "$\Upsilon$",
        u"Φ" : "$\Phi$",
        u"Χ" : "X",
        u"Ψ" : "$\Psi$",
        u"Ω" : "$\Omega$",
        u"α" : "$\\alpha$",
        u"β" : "$\beta$",
        u"γ" : "$\\gamma$",
        u"δ" : "$\delta$",
        u"ε" : "$\epsilon$",
        u"ζ" : "$\zeta$",
        u"η" : "$\eta$",
        u"θ" : "$\\theta$",
        u"ι" : "$\iota$",
        u"κ" : "$\kappa$",
        u"λ" : "$\lambda$",
        u"μ" : "$\mu$",
        u"ν" : "$\\nu$",
        u"ξ" : "$\\xi$",
        u"ο" : "o",
        u"π" : "$\pi$",
        u"ρ" : "$\\rho$",
        u"σ" : "$\sigma$",
        u"τ" : "$\\tau$",
        u"υ" : "$\upsilon$",
        u"φ" : "$\phi$",
        u"χ" : "$\chi$",
        u"ψ" : "$\psi$",
        u"ω" : "$\omega$",
        "%" : "\%"
        }

def clean(input_string):
    """
    Clean a string -- replace all messy unicode with something reasonable, if possible.
    Also replace some unicode characters with the LaTeX eQuIvAlEnT
        (e.g.  δ -> $\delta$)

    Args:
        input_string (string): The text to clean up

    Returns: Cleaned string.
    """
    cleaned_string = u''
    cleaned_string = input_string.replace('&#x0301','') #ACUTE ACCENT MARK
    cleaned_string = cleaned_string.replace('&#x0308','') #UMLAUT
    cleaned_string = cleaned_string .replace('&#x2013;','-') #DASH
    cleaned_string = cleaned_string.replace('&','\&') #AMPERSAND
    cleaned_string = cleaned_string.replace('"','')
    cleaned_string = cleaned_string.replace('#','\#')
    cleaned_string = cleaned_string.replace('$', '\$')
    cleaned_string = cleaned_string.replace(u'\xe2\x80\x93', '-') #DASH
    cleaned_string = cleaned_string.replace(u'\ue5f8', '-') #DASH
    cleaned_string = cleaned_string.replace(u'\x96', '-') #DASH
    cleaned_string = cleaned_string.replace(u'\xc3\x81', "\\'A") #UPPER TILDA 'A'

    for uni, tex in REPLACEMENT_MAP.iteritems():
        cleaned_string = cleaned_string.replace(uni, tex)

    return cleaned_string

def main():
    if not os.path.isdir("./output/"):
        os.makedirs("./output/")

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = './data/bibjson'
    if not os.path.exists(input_path):
        print "Could not find bibjson file! Exiting."
        sys.exit(1)
    with open(input_path) as fid:
        bib = json.load(fid)

    #list for making bibdesk bibliography
    biblist=[]

    # header + footer for bbl bibliography
    hdr='\\begin{thebibliography}{1000}\n' +\
        '\\expandafter\\ifx\\csname url\\endcsname\\relax\n' +\
        '\\def\\url#1{\\texttt{#1}}\\fi\n' +\
        '\\expandafter\\ifx\\csname urlprefix\\endcsname\\relax\\def\\urlprefix{URL }\\fi\n' +\
        '\\providecommand{\\bibinfo}[2]{#2}\n' +\
        '\\providecommand{\\eprint}[2][]{\\url{#2}}\n'
    ftr='\\end{thebibliography}\n'

    # list for making bbl bibliography
    bibitems=[hdr]

    # loop through each bibitem

    for item in bib:
        # TODO: make sure vars are reset

        #IMPORTANT VARIABLES TO GATHER

        names=[]

        # document id
        docid=item['_gddid']

        # title
        title=item['title']

        # journal
        journal=item['journal']['name']

        # type of document
        typ=item['type']

        # volume number
        if 'volume' in item.keys():
            volume=item['volume']
        else:
            volume=''

        # number issue
        if 'number' in item.keys():
            number=item['number']
        else:
            number=''

        # pages
        if 'pages' in item.keys():
            pages=item['pages']
        else:
            pages=''

        # publication year
        if 'year' in item.keys():
            year=item['year']
        else:
            year=''

        # authors, with formatting fixes
        if 'author' in item.keys():
            for name in item['author']:
                names.append(clean(name['name']))
        else:
            names=''

        # publisher, with formatting fixes
        if 'publisher' in item.keys():
            publisher = clean(item['publisher'])
        else:
            publisher=''

        # url link
        if 'link' in item.keys():
            if 'url' in item['link'][0]:
                link=item['link'][0]['url']
            else:
                link=''
        else:
            link=''

        # clean up the text fields
        title = clean(title)
        if title.isupper():
            title=string.capwords(title)

        journal = clean(journal)
        if journal.isupper():
            journal=string.capwords(journal)

        for i,a in enumerate(names):
            if a.isupper():
                names[i] = string.capwords(names[i])

        if publisher!='USGS': # Assume all non-USGS documents are articles
            bibtemp='@' + typ + '{' + docid + ',\n' + \
                    'title={{' + title + '}},\n'  + \
                    'author={' + ' and '.join(names) + '},\n' + \
                    'journal={' + journal +'},\n'+\
                    'volume={' + volume + '},\n'+\
                    'year={' + year +'},\n'+\
                    'number={' + str(number) + '},\n'+\
                    'pages={' + pages + '}\n}'
        else: # assume that all USGS documents are tech reports
            bibtemp='@techreport{' + docid + ',\n' + \
                'title={{' + title + '}},\n'  + \
                'author={' + ' and '.join(names) + '},\n' + \
                'year={' + year +'},\n'+\
                'institution={' + publisher + '},\n'+\
                'booktitle={' + publisher + ', ' + journal + '}\n}'

        # grow the bibliography list
        biblist.append(bibtemp)

        #### initiatize variables for bbl bibliography
        cite_tmp='\\bibitem{'+docid+'}\n'
        name_tmp=[]
        title_tmp=''
        journal_tmp=''
        volume_tmp=''
        pages_tmp=''
        inst_tmp=''

        #### format author names for bbl
        if names !=[''] and names!='' and names:
            for n in names:
                if n!='':
                    # formatting if author written as 'Shaw, C.A.'
                    if ',' in n and n[-1]!=',':
                        tmp=n.split(',')
                        tmp[-1]=tmp[-1].replace(' ','')
                        name_tmp.append('\\bibinfo{author}{' + tmp[0] + ', ' + tmp[-1][0] + '.}, ')
                    # formatting if author written as 'Charles Shaw'
                    else:
                        tmp=n.split(' ')
                        name_tmp.append('\\bibinfo{author}{' + tmp[-1] + ', ' + tmp[0][0] + '.}, ')

            # no comma needed after last author
            name_tmp[-1]=name_tmp[-1][0:-2] + '\n'

            # if more than one author, separate last author from rest with ampersand
            if len(name_tmp)>1:
                name_tmp[-2]=name_tmp[-2][0:-2] + ' \& '

            # join formatted authors into one string
            name_tmp = ''.join(name_tmp)
        else: #if no authors found, define as empty string
            name_tmp=''

        #### format title for bbl


        if link == '': # if no link included, create normal title
            # some titles do not have periods or question marks at the end
            if title[-1] != '.' and title[-1] != '?':
                title_tmp = '\\newblock \\bibinfo{title}{' + title + '.}\n'
            # others do
            else:
                title_tmp = '\\newblock \\bibinfo{title}{' + title + '}\n'
        elif link != '': # if link is included, make the title a link to the document.
            # some titles do not have periods or question marks at the end
            if title[-1]!='.'  and  title[-1] != '?':
                title_tmp = '\\newblock \\bibinfo{title}{\\href{' + link + '}{{\color{blue}' + title + '.}}}\n'
            # others do
            else:
                title_tmp = '\\newblock \\bibinfo{title}{\\href{' + link + '}{{\color{blue}' + title + '}}}\n'

        #### formating journal name, volume, pages if valid article
        if publisher != 'USGS':
            if journal != '':
                journal_tmp = '\\newblock \\emph{\\bibinfo{journal}{' + journal + '}}\n'
            if volume != '':
                volume_tmp = '\\textbf{\\bibinfo{volume}{'+volume +'}}\n'
            if pages !='' and volume_tmp!='': # if both pages and volume are present
                volume_tmp = volume_tmp[0:-1] + ', '
                pages_tmp = '\\bibinfo{pages}{' + pages + '}\n'
            elif pages!='' and volume_tmp=='': # if both pages are present, but not volume
                #requires slight change to journal name
                journal_tmp = '\\newblock \\emph{\\bibinfo{journal}{' + journal + ', }}\n'
                pages_tmp = '\\bibinfo{pages}{' + pages + '}\n'
        else: # if USGS is publisher, format as technical report
            journal_tmp=''
            volume_tmp=''
            pages_tmp=''
            inst_tmp='\\newblock \\bibinfo{type}{Tech. Rep.}, \\bibinfo{institution}{' + publisher + '} '

        #### formatting the year
        if year != '':
            year_tmp = '(\\bibinfo{year}{' + year +'})\n'

        # list for bbl
        bibitems.append(''.join([cite_tmp,name_tmp,title_tmp,journal_tmp,volume_tmp,pages_tmp,inst_tmp,year_tmp,'\n']))

    # add footer at very bottom
    bibitems.append(ftr)

    # print the bibtex string
    with codecs.open('./output/bibtk.bib', 'wb', 'utf-8') as f1:
        f1.write('\n'.join(biblist))

    # print the bbl string
    with codecs.open('./output/cite.bbl', 'wb', 'utf-8') as f2:
        f2.write(''.join(bibitems))

    # make a simple tex file to input bbl
    references='\\documentclass[12pt]{article}\n' +\
        '\\topmargin 0.0cm\n' +\
        '\\oddsidemargin 0.2cm\n' +\
        '\\textwidth 16cm\n' +\
        '\\textheight 21cm\n' +\
        '\\footskip 1.0cm\n' +\
        '\\usepackage[utf8x]{inputenc}\n'+\
        '\\usepackage{hyperref}\n'+\
        '\\hypersetup{colorlinks=false,pdfborder={0 0 0}}\n'+\
        '\\usepackage[usenames]{color}\n'+\
        '\\begin{document}\n' +\
        '\\input{cite.bbl}\n'+\
        '\\end{document}\n'
    with open('./output/references.tex', 'wb') as f3:
        f3.write(references)
        
    #SUMMARIZE PUBLISHERS AND JOURNALS IN THIS BIBJSON
    all_publishers=np.array([clean(a['publisher']) for a in bib])
    all_journals=all_journals=[tuple((clean(a['journal']['name']),clean(a['publisher']))) for a in bib]
    
    #UNIQUE PUBLISHERS AND NUMBER OF OCCURENCES
    u,counts=np.unique(all_publishers,return_counts=True)
    
    #MAKE A STRUCTURED ARRAY
    pub_table=np.zeros(len(u),dtype={'names':['name','count'],'formats':[u.dtype,'i4']})
    pub_table['name']=u
    pub_table['count']=counts
    
    #SORT BY NUMBER OF OCCURENCES
    pub_table=np.flipud(np.sort(pub_table,order='count'))
    
    #COUNT NUMBER OCCURENCES OF JOURNAL-PUBLISHER TUPLES
    count_map = {}
    for t in all_journals:
        count_map[t] = count_map.get(t, 0)  +1
        
    #MAKE A STRUCTURED ARRAY
    journal_table=np.zeros(len(count_map),dtype={'names':['name','pub','count'],'formats':[np.array([a[0] for a in count_map.keys()]).dtype,np.array([a[1] for a in count_map.keys()]).dtype,'i4']})
    
    for i,j in enumerate(count_map): 
        journal_table['name'][i]=j[0]
        journal_table['pub'][i]=j[1]
        journal_table['count'][i]=count_map[j]
    
    #SORT BY NUMBER OF OCCURENCES
    journal_table=np.flipud(np.sort(journal_table,order='count'))
    
    #INITIATE A LATEX TABLE FOR PUBLISHERS SUMMARY
    latex_pub='\\begin{center} \n' +\
                '\\begin{longtable}{|l|r|} \\hline \n' +\
                '\\multicolumn{2}{|c|}{\\textbf{Publisher Totals}}\\\ \hline\n' +\
                'name&number references\\\ \hline\n'
    
    #LOOP THROUGH PUBLISHER SUMMARY AND APPEND TO LATEX STRING AS NEW ROW
    for p in pub_table:
        latex_pub=latex_pub+ p['name']+'&'+str(p['count'])+'\\\ \n'
    
    #END THE PUBLISHER TABLE
    latex_pub=latex_pub+'\hline\end{longtable}\n'+\
                '\end{center}'
    
    #INITIATE A LATEX TABLE FOR JOURNALS SUMMARY
    latex_journal='\\newpage'+\
                '\\begin{landscape}'+\
                '\\begin{center} \n' +\
                '\\begin{longtable}{|l|l|r|} \\hline \n' +\
                '\\multicolumn{3}{|c|}{\\textbf{Journal Totals}}\\\ \hline\n'+\
                'name&publisher&number references\\\ \hline\n'
    
    #LOOP THROUGH JOURNALS SUMMARY AND APPEND TO LATEX STRING AS NEW ROW(S)
    for j in journal_table:
        #SET MAXIMUM WORD NUMBER PER ROW SO LATEX DOES NOT POOP ITSELF
        words = j['name'].split()
        #CHUNKED TITLE; LIST OF <= 5 WORD N-GRAMS
        subs = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
        
        #LOOP THROUGH CHUNKS AND APPEND TO STRING
        for i in range(len(subs)):
            #FIRST CHUNK GETS THE JOURNAL TOTAL
            if i==0:
                latex_journal=latex_journal+ subs[i]+'&'+j['pub']+'&'+str(j['count'])+'\\\ \n'
            #ALL SUBSEQUENT CHUNKS GET INDENTED
            else:
                latex_journal=latex_journal+'\\hspace{5mm}' + subs[i]+'&&\\\ \n'
    
    #END THE JOURNAL TABLE
    latex_journal=latex_journal+'\\hline\\end{longtable}\n'+\
                '\\end{center}\n'+\
                '\\end{landscape}'
            
    #PREAMBLE FOR BOTH TABLES
    preamble='\\documentclass[12pt]{article}\n'+\
                '\\usepackage{longtable}\n'+\
                '\\usepackage[utf8x]{inputenc}\n'+\
                '\\usepackage{pdflscape}\n'+\
                '\\begin{document}\n'
              
    #CONCATENATE THE PREAMBLE, BOTH TABLES, AND END THE LATEX DOCUMENT
    table=preamble+latex_pub+latex_journal+'\n\\end{document}'
    
    #PRINT THE LATEX TABLES
    with codecs.open('./output/table.tex', 'wb', 'utf-8') as f4:
        f4.write(table)
    
if __name__ == '__main__':
    main()
