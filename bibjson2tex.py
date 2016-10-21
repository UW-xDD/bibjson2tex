# -*- coding: utf-8 -*-
"""
Created on Mon May 30 09:47:43 2016

@author: jhusson
"""
################ IMPORT MODULES AND DEFINE FUNCTIONS
import json
import string
import codecs
import os
from csv import reader

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
        u"ω" : "$\omega$"
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

#    if '$' in title:
#        title = title.split('.')
#        title=title[0]
#        title=title.replace('$','')

    return cleaned_string


#EXCLUSION OF BAD DOCUMENTS - INDICES, ABSTRACTS, BIBLIOGRAPHIES
bad_docs=[]
#with open('/Users/jhusson/Box Sync/postdoc/deepdive/stroms/bad_docs/bad_docs.csv','r') as fid:
#    bd = reader(fid)
#    for r in bd:
#        bad_docs.append(r[0])
#
#bad_docs=bad_docs[1:]
#bad_docs = tuple([str(a) for a in bad_docs])

if not os.path.isdir("./output/"):
    os.makedirs("./output/")

#LOAD IN BIBJSON FILE
#/Users/jhusson/Box Sync/postdoc/deepdive/stroms/bib/data/bibjson
#/Users/jhusson/Box Sync/postdoc/deepdive/stroms/bib/data/final_bib

with open('./data/bibjson') as fid:
    bib=json.load(fid)


#SOME USEFUL LISTS TO GROW
weird_titles=[]
no_year=[]

#LIST FOR MAKING BIBDESK BIBLIOGRAPHY
biblist=[]

#HEADER FOR BBL BIBLIOGRAPHY
hdr='\\begin{thebibliography}{1000}\n' +\
    '\\expandafter\\ifx\\csname url\\endcsname\\relax\n' +\
    '\\def\\url#1{\\texttt{#1}}\\fi\n' +\
    '\\expandafter\\ifx\\csname urlprefix\\endcsname\\relax\\def\\urlprefix{URL }\\fi\n' +\
    '\\providecommand{\\bibinfo}[2]{#2}\n' +\
    '\\providecommand{\\eprint}[2][]{\\url{#2}}\n'

#FOOTER FOR BBL BIBLIOGRAPHY
ftr='\\end{thebibliography}\n'

#LIST FOR MAKING BBL BIBLIOGRAPHY
bibitems=[hdr]

#LOOP THROUGH EACH BIBITEM
for item in bib:
    # TODO: make sure vars are reset

    #IMPORTANT VARIABLES TO GATHER
    names=[]

    #DOCUMENT ID
    docid=item['_gddid']

    #TITLE
    title=item['title']

    #JOURNAL
    journal=item['journal']['name']

    #TYPE OF DOCUMENT
    typ=item['type']

    #VOLUME NUMBER
    if 'volume' in item.keys():
        volume=item['volume']
    else:
        volume=''

    #NUMBER ISSUE
    if 'number' in item.keys():
        number=item['number']
    else:
        number=''

    #PAGES
    if 'pages' in item.keys():
        pages=item['pages']
    else:
        pages=''

    #PUBLICATION YEAR
    if 'year' in item.keys():
        year=item['year']
    else:
        year=''

    #AUTHORS, WITH FORMATTING FIXES
    if 'author' in item.keys():
        for name in item['author']:
            names.append(clean(name['name']))
    else:
        names=''

    #PUBLISHER, WITH FORMATTING FIXES
    if 'publisher' in item.keys():
        publisher = clean(item['publisher'])
    else:
        publisher=''

    #URL LINK
    if 'link' in item.keys():
        if 'url' in item['link'][0]:
            link=item['link'][0]['url']
        else:
            link=''
    else:
        link=''

    #LIST OF DOCUMENTS WITHOUT YEARS
    if year=='':
        no_year.append(docid)

    ######## SOME HACKY SOLUTIONS AND A PILE OF EDGE CASES

    #### TITLE FIXES
    #QUOTATION MARKS
    title = clean(title)

    #### JOURNAL NAME
    journal = clean(journal)

    #### ALL CAPITAL FIXES FOR TITLE, JOURNAL AND AUTHORS
    if title.isupper():
        title=string.capwords(title)

    if journal.isupper():
        journal=string.capwords(journal)

    for i,a in enumerate(names):
        if a.isupper():
            names[i] = string.capwords(names[i])

    #### FORMAT FOR BIBDESK/BIBTEX
    #IF THE TYPE IS TRULY 'ARTICLE'
    if publisher!='USGS':
        bibtemp='@' + typ + '{' + docid + ',\n' + \
                'title={{' + title + '}},\n'  + \
                'author={' + ' and '.join(names) + '},\n' + \
                'journal={' + journal +'},\n'+\
                'volume={' + volume + '},\n'+\
                'year={' + year +'},\n'+\
                'number={' + str(number) + '},\n'+\
                'pages={' + pages + '}\n}'

    #IF ITS ACTUALLY A TECHNICAL REPORT
    else:
        bibtemp='@techreport{' + docid + ',\n' + \
            'title={{' + title + '}},\n'  + \
            'author={' + ' and '.join(names) + '},\n' + \
            'year={' + year +'},\n'+\
            'institution={' + publisher + '},\n'+\
            'booktitle={' + publisher + ', ' + journal + '}\n}'


    #GROW THE BIBLIOGRAPHY LIST (ONLY IF NOT FLAGGED FOR BADNESS)
    if docid not in bad_docs:
        #### LIST FOR BIBDESK/BIBTEX
        biblist.append(bibtemp)

        #### INITIATIZE VARIABLES FOR BBL BIBLIOGRAPHY
        cite_tmp='\\bibitem{'+docid+'}\n'
        name_tmp=[]
        title_tmp=''
        journal_tmp=''
        volume_tmp=''
        pages_tmp=''
        inst_tmp=''

        #### FORMAT AUTHOR NAMES FOR BBL
        if names !=[''] and names!='' and names:
            for n in names:
                if n!='':
                    #FORMATTING IF AUTHOR WRITTEN AS 'SHAW, C.A.'
                    if ',' in n and n[-1]!=',':
                        tmp=n.split(',')
                        tmp[-1]=tmp[-1].replace(' ','')
                        name_tmp.append('\\bibinfo{author}{' + tmp[0] + ', ' + tmp[-1][0] + '.}, ')

                    #FORMATTING IF AUTHOR WRITTEN AS 'CHARLES SHAW'
                    else:
                        tmp=n.split(' ')
                        name_tmp.append('\\bibinfo{author}{' + tmp[-1] + ', ' + tmp[0][0] + '.}, ')

            #NO COMMA NEEDED AFTER LAST AUTHOR
            name_tmp[-1]=name_tmp[-1][0:-2] + '\n'

            #IF MORE THAN ONE AUTHOR, SEPARATE LAST AUTHOR FROM REST WITH AMPERSAND
            if len(name_tmp)>1:
                name_tmp[-2]=name_tmp[-2][0:-2] + ' \& '

            #JOIN FORMATTED AUTHORS INTO ONE STRING
            name_tmp = ''.join(name_tmp)

        #IF NO AUTHORS FOUND, DEFINE AS EMPTY STRING
        else:
            name_tmp=''

        #### FORMAT TITLE FOR BBL
        if title != '' and link=='':
            #SOME TITLES DO NOT HAVE PERIODS OR QUESTION MARKS AT THE END
            if title[-1]!='.' and  title[-1]!='?':
                title_tmp = '\\newblock \\bibinfo{title}{' + title + '.}\n'

            #OTHERS DO
            else:
                title_tmp = '\\newblock \\bibinfo{title}{' + title + '}\n'

        if title != '' and link!='':
            #SOME TITLES DO NOT HAVE PERIODS OR QUESTION MARKS AT THE END
            if title[-1]!='.' and  title[-1]!='?':
                title_tmp = '\\newblock \\bibinfo{title}{\\href{' + link + '}{{\color{blue}' + title + '.}}}\n'

            #OTHERS DO
            else:
                title_tmp = '\\newblock \\bibinfo{title}{\\href{' + link + '}{{\color{blue}' + title + '}}}\n'


        #### FORMATING JOURNAL NAME, VOLUME, PAGES IF VALID ARTICLE
        if publisher!='USGS':
            if journal !='':
                journal_tmp = '\\newblock \\emph{\\bibinfo{journal}{' + journal + '}}\n'

            if volume!='':
                volume_tmp = '\\textbf{\\bibinfo{volume}{'+volume +'}}\n'

            #IF BOTH PAGES AND VOLUME ARE PRESENT
            if pages !='' and volume_tmp!='':
                volume_tmp = volume_tmp[0:-1] + ', '
                pages_tmp = '\\bibinfo{pages}{' + pages + '}\n'

            #IF BOTH PAGES ARE PRESENT, BUT NOT VOLUME
            elif pages!='' and volume_tmp=='':
                #REQUIRES SLIGHT CHANGE TO JOURNAL NAME
                journal_tmp = '\\newblock \\emph{\\bibinfo{journal}{' + journal + ', }}\n'
                pages_tmp = '\\bibinfo{pages}{' + pages + '}\n'

        #IF USGS IS PUBLISHER, FORMAT AS TECHNICAL REPORT
        else:
            journal_tmp=''
            volume_tmp=''
            pages_tmp=''
            inst_tmp='\\newblock \\bibinfo{type}{Tech. Rep.}, \\bibinfo{institution}{' + publisher + '} '

        #### FORMATTING THE YEAR
        if year != '':
            year_tmp = '(\\bibinfo{year}{' + year +'})\n'

        #LIST FOR BBL
        bibitems.append(''.join([cite_tmp,name_tmp,title_tmp,journal_tmp,volume_tmp,pages_tmp,inst_tmp,year_tmp,'\n']))

#ADD FOOTER AT VERY BOTTOM
bibitems.append(ftr)

#PRINT THE BIBTEX STRING
with codecs.open('./output/bibtk.bib', 'wb', 'utf-8') as f1:
    f1.write('\n'.join(biblist))

#PRINT THE BBL STRING
with codecs.open('./output/cite.bbl', 'wb', 'utf-8') as f2:
    f2.write(''.join(bibitems))

#MAKE A SIMPLE TEX FILE TO INPUT BBL
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

